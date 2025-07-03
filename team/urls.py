from django.urls import path
from myapp import views as TeamViews

urlpatterns = [
    path('api/register/', TeamViews.register),
    path('api/login/', TeamViews.login),
    path('my/update/avatar', TeamViews.update_avatar),
    path('my/update/photo', TeamViews.update_photo),
    path('my/update/pwd', TeamViews.update_password),
    path('my/update/user_info', TeamViews.update_user_info),
    path('api/team/members/', TeamViews.get_team_members),
]
