from django.db import models


# Create your models here.


class JobInfo(models.Model):
    """招聘"""
    name = models.CharField(max_length=255, null=False, verbose_name='职位名称')
    nature = models.CharField(max_length=255, verbose_name='招聘性质')
    salary = models.CharField(max_length=20, verbose_name='薪资范围')
    degree_required = models.CharField(max_length=255, verbose_name='学历要求')
    location = models.CharField(max_length=255, verbose_name='工作地点')
    number = models.CharField(max_length=255, verbose_name='招聘人数')
    company = models.CharField(max_length=255, verbose_name='招聘公司')
    request = models.CharField(max_length=255, verbose_name='专业要求')

    class Meta:
        db_table = 'workinfo_copy1'

    def __str__(self):
        return self.name
