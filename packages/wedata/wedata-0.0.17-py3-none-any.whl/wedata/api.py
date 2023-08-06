from .checker import Checker
from .client import RemoteClient
from .client_local import LocalClient

__all__ = ['login', 'query', 'extract', 'get_client']


def get_client(mode: str = 'local'):
    if mode == 'remote':
        client = RemoteClient.instance()
    else:
        client = LocalClient.instance()
    return client


# 为了兼容，保留接口
def login(username, password):
    """通过username和password登陆，设置token"""
    client = RemoteClient.instance()
    client.login(username, password)


def query(param):
    """查询接口"""
    client = RemoteClient.instance()
    Checker.check_params(param)
    d = client.query(param)
    return d


def extract(param):
    """提取接口"""
    client = RemoteClient.instance()
    Checker.check_params(param)
    d = client.extract(param)
    return d
