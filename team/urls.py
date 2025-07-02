from django.urls import path
from myapp import views as TeamViews

urlpatterns = [
    path('api/register/', TeamViews.register),
    path('api/login/', TeamViews.login),
    path('my/update/avatar', TeamViews.update_avatar),
    path('my/update/pwd', TeamViews.update_password),
    path('my/update/user_info', TeamViews.update_user_info),
]
