import codefast as cf
from redis import StrictRedis

from authc.core import authc


def get_redis_lab():
    # use tcp forward service to speed up redis connection
    a = authc()
    host, port, password = a.get('redis_host'), 35132, a.get('main_redis_pass')
    return StrictRedis(host=host, port=port, password=password)


def get_redis():
    a = authc()
    host, port, password = a.get('redis_host'), a.get('redis_port'), a.get(
        'redis_pass')
    return StrictRedis(host=host, port=port, password=password)


def get_redis_cn():
    return get_redis()


def scf():
    """ Redis based on tencent scf
    """
    class ScfRedis(object):
        def __init__(self) -> None:
            self.url = ('aHR0cHM6Ly9zZXJ2aWNlLW81MXdqaHpkLTEzMDM5ODgwNDEuYmouYXBpZ'
                        '3cudGVuY2VudGNzLmNvbS9yZWRpcwo=')
            self.url = cf.b64decode(self.url)
            self.headers = {'Content-Type': 'application/json'}

        def get(self, key: str) -> str:
            try:
                return cf.net.post(self.url, json={'key': key}).json()['data']['value']
            except Exception as e:
                return ''

        def set(self, key: str, value: str) -> None:
            return cf.net.post(self.url, json={'key': key, 'value': value})
    return ScfRedis()
