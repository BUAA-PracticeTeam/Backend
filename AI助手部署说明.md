# AI助手后端部署说明

## 概述

本文档说明如何在Django后端部署AI助手功能，集成DeepSeek大模型和蒲公英乡野航迹实践队知识库。

## 1. 环境准备

### 1.1 安装依赖
```bash
pip install -r requirements.txt
```

### 1.2 配置环境变量
复制 `env.example` 为 `.env` 并配置：
```bash
cp env.example .env
```

编辑 `.env` 文件，设置以下关键配置：
```env
# DeepSeek API 密钥（必需）
DEEPSEEK_API_KEY=your_actual_deepseek_api_key

# 其他配置...
```

## 2. 获取DeepSeek API密钥

1. 访问 [DeepSeek Platform](https://platform.deepseek.com/)
2. 注册/登录账号
3. 在控制台创建API密钥
4. 将密钥配置到 `.env` 文件中

## 3. 启动服务

### 3.1 开发环境
```bash
python manage.py runserver
```

### 3.2 生产环境
```bash
python manage.py collectstatic
python manage.py migrate
gunicorn team.wsgi:application
```

## 4. 接口测试

### 4.1 健康检查
```bash
curl http://127.0.0.1:8000/api/ai_chat/health/
```

### 4.2 AI对话测试
```bash
curl -X POST http://127.0.0.1:8000/api/ai_chat/ \
  -H "Content-Type: application/json" \
  -d '{"user_message": "你好，我想了解你们团队"}'
```

## 5. 功能特性

### 5.1 团队知识库
- ✅ 团队基本信息（名称、成立时间、规模等）
- ✅ 主要活动类型（乡村支教、环保宣传等）
- ✅ 团队价值观和使命
- ✅ 实践足迹和成就

### 5.2 AI对话能力
- ✅ 基于DeepSeek大模型
- ✅ 支持多轮对话上下文
- ✅ 智能回复和错误处理
- ✅ 团队知识融合

### 5.3 安全特性
- ✅ CSRF保护
- ✅ 请求频率限制（可配置）
- ✅ 错误日志记录
- ✅ API密钥安全存储

## 6. 配置说明

### 6.1 知识库配置
在 `myapp/views/chat.py` 中的 `TEAM_KNOWLEDGE_BASE` 可以修改团队信息：

```python
TEAM_KNOWLEDGE_BASE = {
    "team_info": {
        "name": "蒲公英乡野航迹实践队",
        # ... 其他信息
    },
    # ... 其他配置
}
```

### 6.2 AI模型配置
可以调整以下参数：
```python
payload = {
    'model': 'deepseek-chat',  # 模型名称
    'max_tokens': 1000,        # 最大回复长度
    'temperature': 0.7,        # 创造性（0-1）
    'stream': False           # 是否流式响应
}
```

## 7. 故障排除

### 7.1 API密钥错误
- 检查 `.env` 文件中的 `DEEPSEEK_API_KEY` 是否正确
- 确认API密钥是否有效且有足够余额

### 7.2 网络连接问题
- 检查服务器网络连接
- 确认DeepSeek API服务是否正常

### 7.3 CORS错误
- 检查 `CORS_ALLOWED_ORIGINS` 配置
- 确认前端域名是否在允许列表中

## 8. 监控和日志

### 8.1 查看日志
```bash
# Django日志
tail -f logs/django.log

# 系统日志
journalctl -u your-django-service
```

### 8.2 性能监控
- 监控API响应时间
- 跟踪API调用次数和费用
- 监控服务器资源使用

## 9. 扩展功能

### 9.1 添加更多知识
可以在 `TEAM_KNOWLEDGE_BASE` 中添加：
- 团队成员信息
- 活动照片和视频
- 媒体报道和奖项
- 合作伙伴信息

### 9.2 实现RAG检索
- 集成向量数据库（如Chroma、Pinecone）
- 实现语义搜索
- 动态知识库更新

### 9.3 用户认证
- 添加用户登录验证
- 实现对话历史存储
- 个性化回复功能

## 10. 联系支持

如有问题，请联系开发团队或查看项目文档。 