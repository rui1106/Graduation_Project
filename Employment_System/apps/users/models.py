
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from apps.jobs.models import JobInfo


class User(AbstractUser):
    phone = models.CharField(max_length=11, unique=True, null=False, verbose_name='手机号')
    is_admin = models.IntegerField(default=0, verbose_name="是否为管理员")
    collection = models.ManyToManyField(JobInfo, through="Collection_job")
    ImgUrl = models.CharField(default="", max_length=500, verbose_name="图片url")

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'

    def __str__(self):
        return self.username


class Collection_job(models.Model):
    jobs = models.ForeignKey(JobInfo, on_delete=models.CASCADE, related_name='a')
    users = models.ForeignKey(User, on_delete=models.CASCADE, related_name='b')

    class Meta:
        db_table = 'tb_collection'
        verbose_name = "关注"

