from django.db import models

from hippo_api.utils.models import BaseModel
# Create your models here.
class Hosts(BaseModel):
    hostname = models.CharField(max_length=32, verbose_name="主机名")
    ip_addr = models.CharField(max_length=32, verbose_name="ip地址")
    port = models.IntegerField(verbose_name="ssh端口")
    desc = models.CharField(max_length=255, verbose_name="描述信息")

    category = models.ForeignKey('HostCategory', on_delete=models.CASCADE)

    class Meta:
        db_table = 't_hippo_hosts'
        verbose_name= '主机表'
        verbose_name_plural = verbose_name


class HostCategory(BaseModel):
    name = models.CharField(max_length=32, verbose_name="主机类型")

    class Meta:
        db_table = 't_hippo_hostcategory'
