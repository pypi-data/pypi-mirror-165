from django.conf import settings
from django.db import models

# @register_snippet
class SshHost(models.Model):
    """SSH服务器信息"""
    title = models.CharField(max_length=64,
                             null=True,
                             blank=True,
                             default=None,
                             verbose_name="备注")
    host = models.CharField(max_length=64, verbose_name="主机名")
    port = models.IntegerField(default=22, verbose_name="端口")
    user = models.CharField(max_length=32, verbose_name="用户名")
    password = models.CharField(max_length=32, verbose_name="密码")
    private_key = models.TextField(null=True,
                                   blank=True,
                                   default=None,
                                   verbose_name="私钥")
    tag = models.CharField(max_length=16,
                           null=True,
                           blank=True,
                           default=None,
                           verbose_name="标签分类")
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.title} : ssh {self.user}@{self.host} -p {self.password}"

    class Meta(object):
        # 定义表名
        # db_table = "department"
        # 定义在管理后台显示的名称
        verbose_name = 'SSH主机'
        verbose_name_plural = verbose_name
        
    
        
      

class PortForward(models.Model):
    """
    端口转发
    """
    PROTOCOL_TYPE = (("tcp", "tcp"), ("udp", "udp"))
    title = models.CharField(max_length=64,
                             null=True,
                             blank=True,
                             default="[new]",
                             verbose_name="备注")
    lhost = models.CharField(max_length=64,
                             default='0.0.0.0',
                             verbose_name="本机IP")
    lport = models.IntegerField(blank=False, null=False, verbose_name="本机端口")
    rhost = models.CharField(max_length=32,
                             blank=False,
                             null=False,
                             verbose_name="远程IP")
    rport = models.IntegerField(blank=False, null=False, verbose_name="远程端口")
    proto = models.CharField(max_length=32,
                             choices=PROTOCOL_TYPE,
                             default="tcp",
                             verbose_name="网络协议类型",
                             null=True,
                             blank=True)
    via_ssh = models.ForeignKey(to=SshHost,
                                on_delete=models.DO_NOTHING,
                                verbose_name="通过ssh隧道")
    enabled = models.BooleanField(default=True, verbose_name="启用")
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return f"{self.title} {self.proto}://{self.lhost}:{self.lport}/{self.rhost}:{self.rport}"

    class Meta(object):
        # 定义表名
        # db_table = "department"
        # 定义在管理后台显示的名称
        verbose_name = '端口转发'
        verbose_name_plural = verbose_name