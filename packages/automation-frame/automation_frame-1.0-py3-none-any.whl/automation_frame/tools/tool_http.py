"""
-*- coding:utf-8 -*-
@Time  :2021/10/27 12:55 上午
@Author:zjcao
@Email :zjcaod@isoftstone.com
@File  :tool_http.py
"""
import sys

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
log = get_logger("Http")


class Http:

    def __init__(self, timeout=60):
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        requests.DEFAULT_RETRIES = 5
        self.timeout = timeout
        self.headers = {"Connection": "close"}

    def get(self, url="", params=None, headers=None):
        if headers:
            self.headers.update(headers)
        log.info(f"Url=={url}")
        log.info(f"Method==GET")
        log.info(f"Headers=={self.headers}")
        log.info(f"Params=={params}")
        resp = requests.get(url=url, params=params, headers=self.headers, timeout=self.timeout, verify=False)
        time_consuming, time_total = self.response_time(resp)
        log.info(f"Response:status_code={resp.status_code}, text={resp.text}, time_consuming={time_consuming}, time_total={time_total}")
        return resp

    def post(self, url="", data=None, params=None, headers=None,files=None):
        if headers:
            self.headers.update(headers)
        log.info(f"Url=={url}")
        log.info(f"Method==POST")
        log.info(f"Headers=={self.headers}")
        log.info(f"Data=={data}")
        log.info(f"Params=={params}")
        resp = requests.post(url=url, data=data, params=params, headers=self.headers,files=files, timeout=self.timeout, verify=False)
        time_consuming, time_total = self.response_time(resp)
        size = sys.getsizeof(resp.text)
        log.info(f'响应内容{size}字节,单位bytes')
        if size < 100000:
            log.info(f"Response:status_code={resp.status_code}, text={resp.text}, time_consuming={time_consuming}, time_total={time_total}")
        else:
            log.info(f'响应内容已超过100000字节,本次请求响应日志未打印')
        return resp

    def put(self, url="", data=None, headers=None,files=None):
        if headers:
            self.headers.update(headers)
        log.info(f"Url=={url}")
        log.info(f"Method==PUT")
        log.info(f"Headers=={self.headers}")
        log.info(f"Data=={data}")
        resp = requests.put(url=url, data=data, headers=self.headers,files=files, timeout=self.timeout, verify=False)
        time_consuming, time_total = self.response_time(resp)
        log.info(f"Response:status_code={resp.status_code}, text={resp.text}, time_consuming={time_consuming}, time_total={time_total}")
        return resp

    def delete(self, url="", data=None, headers=None):
        self.headers.update(headers)
        log.info(f"Url=={url}")
        log.info(f"Method==DELETE")
        log.info(f"Headers=={self.headers}")
        log.info(f"Data=={data}")
        resp = requests.delete(url=url, data=data, headers=self.headers, timeout=self.timeout, verify=False)
        time_consuming, time_total = self.response_time(resp)
        log.info(f"Response:status_code={resp.status_code}, text={resp.text}, time_consuming={time_consuming}, time_total={time_total}")
        return resp

    def patch(self, url="", data=None, headers=None):
        self.headers.update(headers)
        log.info(f"Url=={url}")
        log.info(f"Method==PATCH")
        log.info(f"Headers=={self.headers}")
        log.info(f"Data=={data}")
        resp = requests.patch(url=url, data=data, headers=self.headers, timeout=self.timeout, verify=False)
        time_consuming, time_total = self.response_time(resp)
        log.info(f"Response:status_code={resp.status_code}, text={resp.text}, time_consuming={time_consuming}, time_total={time_total}")
        return resp

    def response_time(self, response):
        # time_consuming为响应时间，单位为毫秒
        time_consuming = response.elapsed.microseconds / 1000
        # time_total为响应时间，单位为秒
        time_total = response.elapsed.total_seconds()
        return time_consuming, time_total

if __name__ == '__main__':
    Http().get('https://www.baidu.com/')