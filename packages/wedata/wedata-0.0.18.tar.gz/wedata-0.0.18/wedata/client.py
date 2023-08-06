import json
import threading
from io import StringIO

import requests
import pandas as pd

from .config import Config
from .checker import Checker


class BaseClient(object):
    _threading_local = threading.local()

    def __init__(self):
        self._instance = None

    @classmethod
    def instance(cls):
        _instance = getattr(cls._threading_local, '_instance', None)
        if _instance is None:
            _instance = cls()
            cls._threading_local._instance = _instance
        return _instance

    def query(self, param: dict):
        raise NotImplementedError

    def extract(self, param: dict):
        raise NotImplementedError


class BaseRemoteClient(BaseClient):
    _threading_local = threading.local()

    def __init__(self):
        super().__init__()
        self.host = Config.host
        self.port = Config.port
        self._refresh_token = None
        self._access_token = None
        self._instance = None
        self.root_url = f'http://{self.host}:{self.port}/api/v1'

    def _post_with_token(self, url, param):
        headers = {
            "Authorization": f'Bearer {self._access_token}'
        }
        r = requests.post(url, json=param, headers=headers)
        return r

    def _login(self, username, password, refresh=True):
        url = f'{self.root_url}/security/login'
        if refresh:
            body = {
                "username": username,
                "password": password,
                "provider": 'db',
                "refresh": True
            }
        else:
            body = {
                "username": username,
                "password": password,
                "provider": 'db'
            }
        headers = {
            "Content-Type": "application/json"
        }
        r = requests.post(url, data=json.dumps(body), headers=headers)
        return r

    def _refresh(self, refresh_token):
        url = f"{self.root_url}/security/refresh"
        headers = {
            "Authorization": f'Bearer {refresh_token}'
        }
        r = requests.post(url, headers=headers)
        return r

    def login(self, username, password):
        try:
            r = self._login(username, password, refresh=False)
        except Exception as e:
            raise Exception(f"网络连接失败")
        if r.status_code == 200:
            # login succeed
            result = r.json()
            self._access_token = result['access_token']
        elif r.status_code == 401:
            result = r.json()
            raise Exception(f"登陆失败, 返回码: {r.status_code}, 返回值:{result['message']}")
        else:
            raise Exception(f"Connection failed")

    def post_with_token(self, url, param):
        if self._access_token is None:
            raise Exception("Login required")
        try:
            r = self._post_with_token(url, param)
        except Exception as e:
            raise Exception(f"网络连接失败")
        if r.status_code == 200:
            return r
        elif r.status_code == 401:
            result = r.json()
            raise Exception(f"登陆失败, 返回码: {r.status_code}, 返回信息: {result['message']}")
        elif r.status_code == 400:
            result = r.json()
            raise Exception(f"参数错误, 返回码: {r.status_code}, 返回信息: {result['message']}")
        elif r.status_code == 413:
            result = r.json()
            raise Exception(f"登陆失败, 返回码: {r.status_code}, 返回信息: {result['message']}")
        elif r.status_code == 500:
            raise Exception(f"未知错误, 请联系管理员")
        else:
            raise Exception(f"网络连接失败")


class RemoteClient(BaseRemoteClient):

    def __init__(self):
        super().__init__()

    def _response_to_dataframe(self, resp: requests.Response) -> pd.DataFrame:
        if resp.headers["Content-Type"] == "application/json; charset=utf-8":
            result = resp.json()
            df = pd.DataFrame.from_records(result['data'])
        elif resp.headers["Content-Type"] == "text/tsv; charset=utf-8":
            tsv_string_io = StringIO(resp.text)
            df = pd.read_csv(tsv_string_io, sep='\t', na_values='\\N')
        else:
            df = pd.DataFrame()
        return df

    def query_sheet(self, param) -> pd.DataFrame:
        q = {k: v for k, v in param.items() if k not in ["domain", "phylum", "class"]}
        url = f'{self.root_url}/{param.get("domain")}/{param.get("phylum")}/{param.get("class")}'
        resp = self.post_with_token(url, q)
        df = self._response_to_dataframe(resp)
        return df

    def query_descriptor(self, param) -> pd.DataFrame:
        url = f'{self.root_url}/{param.get("domain")}/{param.get("phylum")}/{param.get("class")}'
        resp = self.post_with_token(url, param)

        d = pd.DataFrame.from_records(resp.json()['data'])
        return d

    def query(self, param) -> pd.DataFrame:
        if param["domain"] == "sheet":
            res = self.query_sheet(param)
        elif param["domain"] == "descriptor":
            res = self.query_descriptor(param)
        else:
            raise Exception("Params error, invalid domain")
        return res

    def extract_sheet(self, param) -> pd.DataFrame:
        url = f'{self.root_url}/{param.get("domain")}/{param.get("phylum")}/extract'
        q = param
        resp = self.post_with_token(url, q)
        df = pd.DataFrame.from_records(resp.json()['data'])
        return df

    def extract_descriptor(self, param) -> pd.DataFrame:
        url = f'{self.root_url}/{param.get("domain")}/{param.get("phylum")}/extract'
        q = param
        resp = self.post_with_token(url, q)
        if param["class"].find("synthesis") > 0:
            return resp.json()['data']
        else:
            df = pd.DataFrame.from_records(resp.json()['data'])
            return df

    def extract_feature_synthesis(self, param):
        url = f'{self.root_url}/{param.get("domain")}/{param.get("phylum")}/feature_synthesis'
        q = param
        resp = self.post_with_token(url, q)
        res = dict()
        for k, v in resp.json()["data"].items():
            res[k] = pd.DataFrame.from_records(v)
        return res

    def extract(self, param):
        if param["domain"] == "sheet":
            res = self.extract_sheet(param)
        elif param["domain"] == "descriptor":
            res = self.extract_descriptor(param)
        else:
            raise Exception("Params error, invalid domain")
        return res
