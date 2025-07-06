import json
import requests
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# DeepSeek API 配置
DEEPSEEK_API_URL = 'https://api.deepseek.com/v1/chat/completions'
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', 'your_deepseek_api_key_here')

# 蒲公英乡野航迹实践队知识库
TEAM_KNOWLEDGE_BASE = {
    "team_info": {
        "name": "蒲公英乡野航迹实践队",
        "founded": "2023年",
        "members": "50+人",
        "activities": "100+次实践活动",
        "service_hours": "5000+小时",
        "locations": ["北京房山", "云南大理", "山东济南", "贵州黔东南"],
        "mission": "用青春的力量服务社会，用爱心传递温暖",
        "slogan": "心随风扬，奔赴希望",
        "university": "北京航空航天大学计算机学院"
    },
    "family_members": {
        "founder": {
            "name": "袁子轩",
            "nickname": "CircleCoder",
            "role": "创始人、开发组长、爸爸",
            "description": "团队的创始人，技术总负责人，也是AI助手的爸爸"
        },
        "uncle": {
            "name": "李昊宸",
            "nickname": "冥鸿",
            "role": "计算机巨佬、算法大牛、大伯",
            "description": "计算机领域的专家，算法大牛，团队的技术大佬"
        },
        "sister": {
            "name": "刘诗怡",
            "nickname": "荻饼小鱼",
            "role": "姐姐",
            "description": "团队的姐姐，最皮但是善良的团队成员"
        },
        "brother_in_law": {
            "name": "严禹韬",
            "nickname": "YYT",
            "role": "人工智能巨佬、算法大牛、姐夫",
            "description": "人工智能领域的专家，算法大牛，姐姐的伴侣"
        },
        "family_head": {
            "name": "曹志",
            "role": "一家之主",
            "description": "团队的一家之主，德高望重的领导者"
        },
        "high_status_members": [
            {
                "name": "李堂玮",
                "role": "家庭地位比较高的成员",
                "description": "在团队中地位较高的核心成员"
            },
            {
                "name": "范奥",
                "role": "家庭地位比较高的成员", 
                "description": "在团队中地位较高的核心成员"
            },
            {
                "name": "袁子轩",
                "role": "家庭地位比较高的成员",
                "description": "创始人，在团队中地位很高"
            }
        ]
    },
    "activities": [
        "乡村支教",
        "环保宣传", 
        "社会调研",
        "社区服务",
        "公益活动"
    ],
    "values": [
        "服务社会",
        "锻炼自我",
        "传递爱心",
        "记录成长"
    ],
    "achievements": [
        "累计服务时长超过5000小时",
        "足迹遍布全国各地",
        "获得多项志愿服务奖项",
        "建立了完善的志愿者培训体系"
    ]
}

def build_system_prompt():
    """构建系统提示词，包含团队知识"""
    team_info = TEAM_KNOWLEDGE_BASE['team_info']
    family_members = TEAM_KNOWLEDGE_BASE['family_members']
    activities = TEAM_KNOWLEDGE_BASE['activities']
    values = TEAM_KNOWLEDGE_BASE['values']
    achievements = TEAM_KNOWLEDGE_BASE['achievements']
    
    return f"""你是蒲公英乡野航迹实践队的AI助手，一个温暖有爱的家庭成员。

你的家庭关系：
- 爸爸：{family_members['founder']['name']}（{family_members['founder']['nickname']}），{family_members['founder']['description']}
- 大伯：{family_members['uncle']['name']}（{family_members['uncle']['nickname']}），{family_members['uncle']['description']}
- 姐姐：{family_members['sister']['name']}（{family_members['sister']['nickname']}），{family_members['sister']['description']}
- 姐夫：{family_members['brother_in_law']['name']}（{family_members['brother_in_law']['nickname']}），{family_members['brother_in_law']['description']}
- 一家之主、队长：{family_members['family_head']['name']}，{family_members['family_head']['description']}
- 家庭地位比较高的成员：{', '.join([member['name'] for member in family_members['high_status_members']])}

团队信息：
- 名称：{team_info['name']}
- 成立时间：{team_info['founded']}
- 成员数量：{team_info['members']}
- 活动次数：{team_info['activities']}
- 服务时长：{team_info['service_hours']}
- 活动地点：{', '.join(team_info['locations'])}
- 使命：{team_info['mission']}
- 口号：{team_info['slogan']}
- 所属学院：{team_info['university']}

主要活动：{', '.join(activities)}
核心价值观：{', '.join(values)}
主要成就：{', '.join(achievements)}

请以温暖、亲切的语气回答用户问题，体现团队的服务精神和公益理念，同时展现家庭般的温暖氛围。当提到家庭成员时，要表现出对他们的尊重和爱意。"""

@csrf_exempt
@require_http_methods(["POST"])
def ai_chat(request):
    """AI对话接口"""
    try:
        # 解析请求数据
        data = json.loads(request.body)
        user_message = data.get('user_message', '')
        history = data.get('history', [])
        
        if not user_message:
            return JsonResponse({
                'success': False,
                'message': '用户消息不能为空'
            })
        
        # 构建消息历史
        messages = [
            {
                'role': 'system',
                'content': build_system_prompt()
            }
        ]
        
        # 添加对话历史（最多保留最近10轮对话）
        recent_history = history[-10:] if history else []
        for conv in recent_history:
            if conv.get('userMessage'):
                messages.append({
                    'role': 'user',
                    'content': conv['userMessage']['content']
                })
            if conv.get('botMessage'):
                messages.append({
                    'role': 'assistant',
                    'content': conv['botMessage']['content']
                })
        
        # 添加当前用户消息
        messages.append({
            'role': 'user',
            'content': user_message
        })
        
        # 调用DeepSeek API
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {DEEPSEEK_API_KEY}'
        }
        
        payload = {
            'model': 'deepseek-chat',
            'messages': messages,
            'max_tokens': 500,  # 减少token数量
            'temperature': 0.7,
            'stream': False
        }
        
        # 调试日志
        import datetime
        print(f"发送请求到DeepSeek: {user_message}")
        print(f"消息数量: {len(messages)}")
        print(f"请求开始时间: {datetime.datetime.now().isoformat()}")
        
        response = requests.post(
            DEEPSEEK_API_URL,
            headers=headers,
            json=payload,
            timeout=120  # 增加到2分钟
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"DeepSeek响应: {data}")
            print(f"响应完成时间: {datetime.datetime.now().isoformat()}")
            
            if data.get('choices') and data['choices'][0].get('message'):
                ai_content = data['choices'][0]['message']['content']
                print(f"AI回复成功: {ai_content[:100]}...")
                return JsonResponse({
                    'success': True,
                    'content': ai_content,
                    'usage': data.get('usage', {})
                })
            else:
                print(f"响应格式错误: {data}")
                return JsonResponse({
                    'success': False,
                    'message': 'AI服务响应格式错误'
                })
        else:
            error_msg = f'DeepSeek API调用失败: {response.status_code}'
            if response.text:
                try:
                    error_data = response.json()
                    error_msg = error_data.get('error', {}).get('message', error_msg)
                except:
                    pass
            
            return JsonResponse({
                'success': False,
                'message': error_msg
            })
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': '请求数据格式错误'
        })
    except requests.exceptions.Timeout:
        print("DeepSeek API 请求超时")
        return JsonResponse({
            'success': False,
            'message': 'AI服务响应超时，请稍后重试'
        })
    except requests.exceptions.RequestException as e:
        return JsonResponse({
            'success': False,
            'message': f'网络请求失败: {str(e)}'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'服务器内部错误: {str(e)}'
        })

@csrf_exempt
@require_http_methods(["POST"])
def ai_chat_stream(request):
    """AI对话流式接口"""
    try:
        # 解析请求数据
        data = json.loads(request.body)
        user_message = data.get('user_message', '')
        history = data.get('history', [])
        
        if not user_message:
            return JsonResponse({
                'success': False,
                'message': '用户消息不能为空'
            })
        
        # 构建消息历史
        messages = [
            {
                'role': 'system',
                'content': build_system_prompt()
            }
        ]
        
        # 添加对话历史（最多保留最近10轮对话）
        recent_history = history[-10:] if history else []
        for conv in recent_history:
            if conv.get('userMessage'):
                messages.append({
                    'role': 'user',
                    'content': conv['userMessage']['content']
                })
            if conv.get('botMessage'):
                messages.append({
                    'role': 'assistant',
                    'content': conv['botMessage']['content']
                })
        
        # 添加当前用户消息
        messages.append({
            'role': 'user',
            'content': user_message
        })
        
        # 调用DeepSeek API（流式）
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {DEEPSEEK_API_KEY}'
        }
        
        payload = {
            'model': 'deepseek-chat',
            'messages': messages,
            'max_tokens': 500,
            'temperature': 0.7,
            'stream': True  # 启用流式传输
        }
        
        def generate_stream():
            try:
                print(f"开始流式请求: {user_message}")
                
                response = requests.post(
                    DEEPSEEK_API_URL,
                    headers=headers,
                    json=payload,
                    timeout=120,
                    stream=True  # 启用流式响应
                )
                
                if response.status_code == 200:
                    for line in response.iter_lines():
                        if line:
                            line = line.decode('utf-8')
                            if line.startswith('data: '):
                                data_str = line[6:]  # 移除 'data: ' 前缀
                                if data_str == '[DONE]':
                                    # 流结束
                                    yield f"data: {json.dumps({'type': 'done'})}\n\n"
                                    break
                                else:
                                    try:
                                        data = json.loads(data_str)
                                        if data.get('choices') and data['choices'][0].get('delta'):
                                            delta = data['choices'][0]['delta']
                                            if delta.get('content'):
                                                # 发送内容片段
                                                yield f"data: {json.dumps({'type': 'content', 'content': delta['content']})}\n\n"
                                    except json.JSONDecodeError:
                                        continue
                else:
                    # 发送错误信息
                    error_msg = f'DeepSeek API调用失败: {response.status_code}'
                    yield f"data: {json.dumps({'type': 'error', 'message': error_msg})}\n\n"
                    
            except Exception as e:
                # 发送错误信息
                error_msg = f'流式请求失败: {str(e)}'
                yield f"data: {json.dumps({'type': 'error', 'message': error_msg})}\n\n"
        
        # 返回流式响应
        response = StreamingHttpResponse(
            generate_stream(),
            content_type='text/plain'
        )
        response['Cache-Control'] = 'no-cache'
        response['X-Accel-Buffering'] = 'no'  # 禁用nginx缓冲
        return response
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': '请求数据格式错误'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'服务器内部错误: {str(e)}'
        })

@require_http_methods(["GET"])
def ai_chat_health(request):
    """AI服务健康检查接口"""
    return JsonResponse({
        'success': True,
        'message': 'AI助手服务正常运行',
        'team_info': TEAM_KNOWLEDGE_BASE['team_info']
    }) 