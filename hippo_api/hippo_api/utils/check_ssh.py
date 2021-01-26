from hippo_api.libs.ssh import SSH


def valid_ssh(host,port,username,password):
    """
    检查ssh是否能ping通
    :param host: ip地址
    :param port:ssh端口
    :param username:用户名
    :param password: 密码
    :return:
    """
    ssh = SSH(host=host,port=port,username=username,password=password)
    try:
        ssh.ping()
    except Exception as e:
        return False

    return True