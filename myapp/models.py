from django.db import models

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
    title = models.CharField(max_length=64)
    content = models.CharField(max_length=8192)
    author = models.CharField(max_length=64)
    time = models.CharField(max_length=64)
    # 封面图片、标签、阅读量、点赞量、评论量
    cover = models.CharField(max_length=128)
    tag = models.CharField(max_length=64)
    read = models.IntegerField(default=0)
    like = models.IntegerField(default=0)
    comment = models.IntegerField(default=0)

