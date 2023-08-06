import hashlib
import json
import time
import requests
import random
import string


def rand_str(length: int) -> str:
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))


def cal_signature(
        customer_id,
        time_now,
        access_id,
        access_key_secret,
        nonce,
        request_id,
        http_body) -> str:
    sha256 = hashlib.sha256()
    sha256.update(
        (
                customer_id +
                access_id +
                access_key_secret +
                time_now +
                nonce +
                request_id +
                http_body).encode('utf-8'))
    return sha256.hexdigest()


class Param(object):
    def __init__(self):
        self.project_id: str = ""
        self.customer_id: str = ""
        self.retry_times: int = 0
        self.schema: str = "http"
        self.headers: dict = {}
        self.ak: str = ""
        self.sk: str = ""
        self.rec_url: str = ""
        self.write_url: str = ""


class Client:
    def __init__(self, param: Param):
        self._param = param

    def write_user(
            self,
            stage: str,
            param: list):
        url = f"{self._param.write_url}data/openapi/write/{self._param.project_id}/user/{stage}"
        return self.api_request(url, param)

    def write_item(
            self,
            stage: str,
            param: list):
        url = f"{self._param.write_url}data/openapi/write/{self._param.project_id}/item/{stage}"
        return self.api_request(url, param)

    def write_action(
            self,
            stage: str,
            param: list):
        url = f"{self._param.write_url}data/openapi/write/{self._param.project_id}/action/{stage}"
        return self.api_request(url, param)

    def rec(self, param: dict):
        url = f"{self._param.rec_url}{self._param.project_id}"
        return self.api_request(url, param)

    def api_request(self, url, param):
        time_now = str(int(time.time()))
        nonce = rand_str(8)
        request_id = rand_str(16)
        signature = cal_signature(
            self._param.customer_id,
            time_now,
            self._param.ak,
            self._param.sk,
            nonce,
            request_id,
            json.dumps(param).replace(' ', ''))
        headers = {
            "content-type": "application/json",
            "Customer-Id": self._param.customer_id,
            "Access-Id": self._param.ak,
            "Time": time_now,
            "Nonce": nonce,
            "Request-Id": request_id,
            "Signature": signature
        }
        return requests.post(
            url=url,
            headers=headers,
            data=json.dumps(param).replace(
                ' ',
                ''))


class ClientBuilder(object):
    def __init__(self):
        self._param = Param()

    def customer_id(self, customer_id: str):
        self._param.customer_id = customer_id
        return self

    def project_id(self, project_id: str):
        self._param.project_id = project_id
        return self

    def token(self, token: str):
        self._param.token = token
        return self

    def schema(self, schema: str):
        self._param.schema = schema
        return self

    def hosts(self, hosts: list):
        self._param.hosts = hosts
        return self

    def headers(self, headers: dict):
        self._param.headers = headers
        return self

    def ak(self, ak: str):
        self._param.ak = ak
        return self

    def sk(self, sk: str):
        self._param.sk = sk
        return self

    def rec_url(self, rec_url: str):
        self._param.rec_url = rec_url
        return self

    def write_url(self, write_url: str):
        self._param.write_url = write_url
        return self

    def build(self) -> Client:
        return Client(self._param)
