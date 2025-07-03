from django.db import models
from django.utils import timezone

class UserManager(models.Model):
    username = models.CharField(max_length=64)
    nickname = models.CharField(max_length=64,default='')
    password = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    # 个性签名、头像、个人简介、精选照片
    work = models.CharField(max_length=128, default='')
    signature = models.CharField(max_length=128, default='')
    avatar = models.CharField(max_length=128, default='')
    introduction = models.CharField(max_length=1024, default='')
    photo = models.CharField(max_length=128, default='')
    permission = models.IntegerField(default=0)

class Articles(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(
        'UserManager', on_delete=models.SET_NULL, 
        null=True, blank=True, related_name='articles')
    # 封面图片、标签、阅读量、点赞量
    cover = models.CharField(max_length=128)
    tag = models.CharField(max_length=64)
    read = models.IntegerField(default=0)
    like = models.IntegerField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    state = models.CharField(
        max_length=20, choices=[
            ('已发布', '已发布'), ('草稿', '草稿')], default='草稿')

