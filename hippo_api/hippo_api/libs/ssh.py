from paramiko.client import SSHClient, AutoAddPolicy
from paramiko.config import SSH_PORT
from paramiko.rsakey import RSAKey
from paramiko.ssh_exception import AuthenticationException
from io import StringIO


class SSH:
    def __init__(self, host, port=SSH_PORT, username='root', pkey=None, password=None, connect_timeout=15):
        if pkey is None and password is None:
            raise Exception('私钥或者密码必须有一个不为空')
        self.client = None
        self.arguments = {
            'hostname': host,  # 主机的ip地址
            'port': port,  #ssh链接端口  默认22端口
            'username': username,  #连接主机的用户名，
            'password': password,  #链接密码
            'pkey': RSAKey.from_private_key(StringIO(pkey)) if isinstance(pkey, str) else pkey,
            # 'pkey': pkey,  pkey为私钥文件信息，    # 1 密码链接， 2 公私钥链接(免密链接)
            'timeout': connect_timeout,
        }

    @staticmethod
    def generate_key():  # 生成公私钥键值对
        key_obj = StringIO()
        key = RSAKey.generate(2048)
        key.write_private_key(key_obj)
        return key_obj.getvalue(), 'ssh-rsa ' + key.get_base64()
        # 私钥字符串  和  公钥字符串

    # 将公钥上传到对应主机
    def add_public_key(self, public_key):
        # 600 是
        command = f'mkdir -p -m 700 ~/.ssh && \
        echo {public_key!r} >> ~/.ssh/authorized_keys && \
        chmod 600 ~/.ssh/authorized_keys'
        print("self.client asfafasfasfas",self.client, "self=",self)
        code, out = self.exec_command(command)
        if code != 0:
            raise Exception(f'添加公钥失败: {out}')

    # 检测连接并获取连接
    def ping(self):
        with self:
            return True

    # 直接获取连接
    def get_client(self):
        if self.client is not None:
            return self.client
        try:
            self.client = SSHClient()
            self.client.set_missing_host_key_policy(AutoAddPolicy)  #指纹记录

            self.client.connect(**self.arguments)  # 通过参数建立链接，如果链接不上，直接抛错误
        except Exception as e:
            return None
        return self.client

    # 指定上文文件的路径
    # 给远程服务器上传我当前服务器的文件，用这个方法
    def put_file(self, local_path, remote_path):
        with self as cli:  # cli
            sftp = cli.open_sftp()  #sftp的一个连接模式，  ssh  sftp上传下载文件
            sftp.put(local_path, remote_path)
            sftp.close()

    def exec_command(self, command, timeout=1800, environment=None):
        command = 'set -e\n' + command
        # f'set -e mkdir -p -m 700 ~/.ssh && \
        #         echo {public_key!r} >> ~/.ssh/authorized_keys && \
        #         chmod 600 ~/.ssh/authorized_keys'
        with self as cli:  # __enter__方法，并将该方法的返回值给 as 后面的变量
            # cli -- self.client
            chan = cli.get_transport().open_session()
            chan.settimeout(timeout)
            #
            chan.set_combine_stderr(True)  # 正确和错误输出都在一个管道里面输出出来
            # if environment:
            #     str_env = ' '.join(f"{k}='{v}'" for k, v in environment.items())
            #     command = f'export {str_env} && {command}'
            chan.exec_command(command)
            stdout = chan.makefile("rb", -1)
            return chan.recv_exit_status(), self._decode(stdout.read())
            # chan.recv_exit_status()   0 -- 指令执行成功  1 -- 失败
            #

    # 上传文件，根据文件对象(文件句柄或类文件句柄)上传到指定目录下
    def put_file_by_fl(self, fl, remote_path, callback=None):
        with self as cli:
            sftp = cli.open_sftp()
            sftp.putfo(fl, remote_path, callback=callback)

    # 从远程主机下载文件到本地
    def download_file(self, local_path, remote_path):
        with self as cli:
            sftp = cli.open_sftp()
            sftp.get(remote_path, local_path)

    # 获取指定目录路径下的文件和文件夹列表详细信息,结果为列表，列表里面的每一项是from paramiko.sftp_attr import SFTPAttributes  类的对象，通过对象.属性可以获取对应的数据，比如获取修改时间用对象.st_mtime
    def list_dir_attr(self, path):
        with self as cli:
            sftp = cli.open_sftp()
            return sftp.listdir_attr(path)

    # 根据指定路径删除对应文件,没有对应文件会报错，有返回None
    def remove_file(self, path):
        with self as cli:
            sftp = cli.open_sftp()
            sftp.remove(path)

    # 删除远程主机上的目录
    def remove_dir(self, target_path):
        with self as cli:
            sftp = cli.open_sftp()
            sftp.rmdir(target_path)

    # 获取文件详情
    def file_stat(self, remote_path):
        with self as cli:
            sftp = cli.open_sftp()
            return sftp.stat(remote_path)

    # 编码方法
    def _decode(self, out: bytes):
        try:
            return out.decode()
        except UnicodeDecodeError:
            return out.decode('GBK')

    # with self: 先执行__enter__方法
    def __enter__(self):
        if self.client is not None:
            raise RuntimeError('已经建立连接了！！！')
        return self.get_client()
    # with self:语句体内容结束后执行如下方法 先执行__enter__方法
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()
        self.client = None

