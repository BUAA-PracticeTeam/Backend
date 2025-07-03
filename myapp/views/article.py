import json
import os
from dotenv import load_dotenv
from myapp.models import Articles, UserManager
import base64
import uuid
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import oss2

load_dotenv()
OSS_ACCESS_KEY_ID = os.getenv('OSS_ACCESS_KEY_ID')
OSS_ACCESS_KEY_SECRET = os.getenv('OSS_ACCESS_KEY_SECRET')
OSS_ENDPOINT = os.getenv('OSS_ENDPOINT')
OSS_BUCKET_NAME = os.getenv('OSS_BUCKET_NAME')
# 初始化 OSS 客户端
auth = oss2.Auth(OSS_ACCESS_KEY_ID, OSS_ACCESS_KEY_SECRET)
bucket = oss2.Bucket(auth, OSS_ENDPOINT, OSS_BUCKET_NAME)

@csrf_exempt
def get_article_list(request):
    """获取文章列表（支持分页、筛选）"""
    if request.method == 'GET':
        try:
            # 获取查询参数
            pagenum = int(request.GET.get('pagenum', 1))
            pagesize = int(request.GET.get('pagesize', 10))
            state = request.GET.get('state', '')
            cate_id = request.GET.get('cate_id', '')
            
            # 构建查询条件
            queryset = Articles.objects.all()
            
            if state:
                queryset = queryset.filter(state=state)
            if cate_id:
                queryset = queryset.filter(tag=cate_id)  # 假设cate_id对应tag字段
            
            # 计算总数
            total = queryset.count()
            
            # 分页
            start = (pagenum - 1) * pagesize
            end = start + pagesize
            articles = queryset.order_by('-pub_date')[start:end]
            
            # 构建返回数据
            data = []
            for article in articles:
                article_data = {
                    'id': article.id,
                    'title': article.title,
                    'cover': article.cover,
                    'tag': article.tag,
                    'read': article.read,
                    'like': article.like,
                    'pub_date': article.pub_date.isoformat(),
                    'state': article.state,
                    'author': {
                        'id': article.author.id if article.author else None,
                        'nickname': article.author.nickname if article.author else '未知作者'
                    } if article.author else None
                }
                data.append(article_data)
            
            return JsonResponse({
                'error_num': 0,
                'msg': 'success',
                'data': data,
                'total': total
            })
        except Exception as e:
            return JsonResponse({
                'error_num': 1,
                'msg': f'获取文章列表失败: {str(e)}'
            })

@csrf_exempt
def get_article_detail(request):
    """获取单篇文章详情"""
    if request.method == 'GET':
        try:
            article_id = request.GET.get('id')
            if not article_id:
                return JsonResponse({
                    'error_num': 1,
                    'msg': '文章ID不能为空'
                })
            
            article = Articles.objects.get(id=article_id)
            
            # 增加阅读量
            article.read += 1
            article.save()
            
            data = {
                'id': article.id,
                'title': article.title,
                'content': article.content,
                'cover': article.cover,
                'tag': article.tag,
                'read': article.read,
                'like': article.like,
                'pub_date': article.pub_date.isoformat(),
                'update_date': article.update_date.isoformat(),
                'state': article.state,
                'author': {
                    'id': article.author.id if article.author else None,
                    'nickname': article.author.nickname if article.author else '未知作者',
                    'avatar': article.author.avatar if article.author else ''
                } if article.author else None
            }
            
            return JsonResponse({
                'error_num': 0,
                'msg': 'success',
                'data': data
            })
        except Articles.DoesNotExist:
            return JsonResponse({
                'error_num': 1,
                'msg': '文章不存在'
            })
        except Exception as e:
            return JsonResponse({
                'error_num': 1,
                'msg': f'获取文章详情失败: {str(e)}'
            })

@csrf_exempt
def add_article(request):
    """发布新文章"""
    if request.method == 'POST':
        try:
            # 获取表单数据
            title = request.POST.get('title')
            content = request.POST.get('content')
            state = request.POST.get('state', '草稿')
            tag = request.POST.get('tag', '')
            
            # 处理封面图片上传
            cover_img = request.FILES.get('cover_img')
            cover_url = ''
            
            if cover_img:
                # 上传到OSS
                file_ext = cover_img.name.split('.')[-1]
                filename = f"article_covers/{uuid.uuid4()}.{file_ext}"
                bucket.put_object(filename, cover_img.read())
                cover_url = f'https://{OSS_BUCKET_NAME}.{OSS_ENDPOINT}/{filename}'
            
            # 创建文章（这里需要根据实际登录用户设置author）
            # 暂时设置为None，后续可以通过session/token获取当前用户
            article = Articles.objects.create(
                title=title,
                content=content,
                cover=cover_url,
                tag=tag,
                state=state,
                author=None  # 需要根据实际登录用户设置
            )
            
            return JsonResponse({
                'error_num': 0,
                'msg': '发布成功',
                'data': {'id': article.id}
            })
        except Exception as e:
            return JsonResponse({
                'error_num': 1,
                'msg': f'发布失败: {str(e)}'
            })

@csrf_exempt
def edit_article(request):
    """编辑文章"""
    if request.method == 'PUT':
        try:
            # 解析PUT请求的数据
            data = json.loads(request.body)
            article_id = data.get('id')
            
            if not article_id:
                return JsonResponse({
                    'error_num': 1,
                    'msg': '文章ID不能为空'
                })
            
            article = Articles.objects.get(id=article_id)
            
            # 更新字段
            if 'title' in data:
                article.title = data['title']
            if 'content' in data:
                article.content = data['content']
            if 'state' in data:
                article.state = data['state']
            if 'tag' in data:
                article.tag = data['tag']
            
            # 处理封面图片（如果有的话）
            cover_img = request.FILES.get('cover_img')
            if cover_img:
                file_ext = cover_img.name.split('.')[-1]
                filename = f"article_covers/{uuid.uuid4()}.{file_ext}"
                bucket.put_object(filename, cover_img.read())
                article.cover = f'https://{OSS_BUCKET_NAME}.{OSS_ENDPOINT}/{filename}'
            
            article.save()
            
            return JsonResponse({
                'error_num': 0,
                'msg': '编辑成功'
            })
        except Articles.DoesNotExist:
            return JsonResponse({
                'error_num': 1,
                'msg': '文章不存在'
            })
        except Exception as e:
            return JsonResponse({
                'error_num': 1,
                'msg': f'编辑失败: {str(e)}'
            })

@csrf_exempt
def delete_article(request):
    """删除文章"""
    if request.method == 'DELETE':
        try:
            article_id = request.GET.get('id')
            
            if not article_id:
                return JsonResponse({
                    'error_num': 1,
                    'msg': '文章ID不能为空'
                })
            
            article = Articles.objects.get(id=article_id)
            article.delete()
            
            return JsonResponse({
                'error_num': 0,
                'msg': '删除成功'
            })
        except Articles.DoesNotExist:
            return JsonResponse({
                'error_num': 1,
                'msg': '文章不存在'
            })
        except Exception as e:
            return JsonResponse({
                'error_num': 1,
                'msg': f'删除失败: {str(e)}'
            })

@csrf_exempt
def like_article(request):
    """点赞文章"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            article_id = data.get('id')
            
            if not article_id:
                return JsonResponse({
                    'error_num': 1,
                    'msg': '文章ID不能为空'
                })
            
            article = Articles.objects.get(id=article_id)
            article.like += 1
            article.save()
            
            return JsonResponse({
                'error_num': 0,
                'msg': '点赞成功',
                'data': {'like_count': article.like}
            })
        except Articles.DoesNotExist:
            return JsonResponse({
                'error_num': 1,
                'msg': '文章不存在'
            })
        except Exception as e:
            return JsonResponse({
                'error_num': 1,
                'msg': f'点赞失败: {str(e)}'
            })
