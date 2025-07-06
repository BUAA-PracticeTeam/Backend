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
    return f"""你是蒲公英乡野航迹实践队的AI助手。团队成立于2023年，是北京航空航天大学计算机学院的志愿服务团队，有50+成员，主要开展乡村支教、环保宣传、社会调研等活动，累计服务5000+小时。请基于团队信息回答用户问题，体现服务精神和公益理念。"""

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