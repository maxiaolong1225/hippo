from django.db import models

from hippo_api.libs.ssh import SSH
from hippo_api.utils.models import BaseModel
# Create your models here.


class Hosts(BaseModel):
    hostname = models.CharField(max_length=32, verbose_name="主机名")
    ip_addr = models.CharField(max_length=32, verbose_name="ip地址")
    port = models.IntegerField(verbose_name="ssh端口")
    desc = models.CharField(max_length=255, verbose_name="描述信息")
    username = models.CharField(max_length=50,verbose_name="登录用户名")

    category = models.ForeignKey('HostCategory', on_delete=models.CASCADE,
                                 related_name='hc',null=True,
                                 blank=True,verbose_name="主机类别")

    def __str__(self):
        return self.hostname+":"+self.ip_addr

    def get_ssh(self, pkey=None):
        return SSH(host=self.ip_addr,port=self.port,username=self.username,pkey=pkey)

    class Meta:
        db_table = 't_hippo_hosts'
        verbose_name= '主机表'
        verbose_name_plural = verbose_name


class HostCategory(BaseModel):
    name = models.CharField(max_length=32, verbose_name="主机类型")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 't_hippo_hostcategory'


class PkeyModel(BaseModel):
    key = models.CharField(max_length=50,unique=True)
    value = models.TextField()
    desc = models.CharField(max_length=255,null=True)

    def __repr__(self):
        return '<Pkey %r>' % self.key

    class Meta:
        db_table='t_hippo_host_secretkey'