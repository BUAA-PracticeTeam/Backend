from django.urls import path
from myapp.views import user as user
from myapp.views import article as article
from myapp.views import chat as chat

urlpatterns = [
    path('api/register/', user.register),
    path('api/login/', user.login),
    path('my/update/avatar', user.update_avatar),
    path('my/update/photo', user.update_photo),
    path('my/update/pwd', user.update_password),
    path('my/update/user_info', user.update_user_info),
    path('api/team/members/', user.get_team_members),
    
    # 文章相关接口
    path('my/article/list', article.get_article_list),
    path('my/article/info', article.get_article_detail),
    path('my/article/add', article.add_article),
    path('my/article/edit', article.edit_article),
    path('my/article/delete', article.delete_article),
    path('my/article/like', article.like_article),
    path('my/article/mylist', article.get_my_article_list),
    
    # AI助手相关接口
    path('api/ai_chat/', chat.ai_chat),
    path('api/ai_chat/health/', chat.ai_chat_health),
]
