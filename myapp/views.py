# Create your views here.
import json
import os
from dotenv import load_dotenv
from myapp.models import UserManager
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
def register(request):
    response = {'error_num': 0}
    data = json.loads(request.body)
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')

    if UserManager.objects.filter(username=username).exists():
        return JsonResponse({'error_num': 1, 'msg': '用户名已被占用'})

    if UserManager.objects.filter(email=email).exists():
        return JsonResponse({'error_num': 1, 'msg': '邮箱已被注册'})

    try:
        UserManager.objects.create(
            username=username,
            password=password,
            email=email
        )
        response['msg'] = '添加成功'
    except Exception as e:
        response.update({'error_num': 1, 'msg': str(e)})
    return JsonResponse(response)

@csrf_exempt
def login(request):
    response = {'error_num': 0}
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    print(username, password)
    try:
        object = UserManager.objects.get(username=username, password=password)
        response['user'] = {'username': object.username,
                            'nickname': object.nickname,
                            'email': object.email,
                            'avatar': object.avatar,
                            'password': object.password,
                            'work': object.work,
                            'photo': object.photo,
                            'signature': object.signature,
                            'permission': object.permission,
                            'introduction': object.introduction}
        response['msg'] = '登录成功'
    except Exception as e:
        response.update({'error_num': 1, 'msg': '用户名或密码错误'})
    print(response)
    return JsonResponse(response)

@csrf_exempt
def update_avatar(request):
    if request.method == 'PATCH':
        try:
            data = json.loads(request.body) # 确保前端发送的是 JSON 数据
            avatar_data = data.get('avatar')
            username = data.get('username')
            print(username)
            if not avatar_data:
                return JsonResponse({'error': 'No avatar data provided'}, status=400)

            header, encoded = avatar_data.split(',', 1)
            file_ext = header.split('/')[1].split(';')[0]
            binary_data = base64.b64decode(encoded)
            filename = f"avatars/{uuid.uuid4()}.{file_ext}"
            bucket.put_object(filename, binary_data)
            avatar_url = f'https://{OSS_BUCKET_NAME}.{OSS_ENDPOINT}/{filename}'
            # 在数据库对应的字段中保存图片 URL
            print('保存中')
            print('用户名：', username, '头像：', avatar_url)
            UserManager.objects.filter(username=username).update(avatar=avatar_url)
            print('保存成功')
            return JsonResponse({'avatar_url': avatar_url, 'code': 0}, status=200)
        except Exception as e:
            print('错误：',e)
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def update_password(request):
    if request.method == 'PATCH':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            old_password = data.get('old_pwd')
            new_password = data.get('new_pwd')

            user = UserManager.objects.get(username=username)
            if user.password != old_password:
                return JsonResponse({ 'msg': '原密码错误','code': 1}, status=400)

            user.password = new_password
            user.save()
            return JsonResponse({'msg': '密码修改成功', 'code':0}, status=200)

        except UserManager.DoesNotExist:
            return JsonResponse({ 'msg': '用户不存在','code':1}, status=404)
        except Exception as e:
            return JsonResponse({ 'msg': str(e),'code':1}, status=500)
    else:
        return JsonResponse({'msg': '方法不允许','code':1}, status=405)

@csrf_exempt
def update_user_info(request):
    if request.method == 'PATCH':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            nickname = data.get('nickname')
            email = data.get('email')
            # 更新用户信息
            UserManager.objects.filter(username=username).update(nickname=nickname, email=email)
            return JsonResponse({'msg': '用户信息更新成功', 'code': 0}, status=200)
        except Exception as e:
            return JsonResponse({'msg': str(e), 'code': 1}, status=500)
    else:
        return JsonResponse({'msg': '方法不允许', 'code': 1}, status=405)


