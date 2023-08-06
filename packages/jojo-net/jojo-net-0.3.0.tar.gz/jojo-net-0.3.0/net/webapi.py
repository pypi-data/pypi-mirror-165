import requests

from .http import UserAgent
from .util import StrUtil


# 取得headers中指定name的值
def headers_get(headers, name, sub_name=None):
    """ 取得headers中的名为name的字段的值, sub_name是子字段 """
    name = name.lower()
    for key in headers:
        if key.lower() == name:
            val = headers[key]
            vals = val.split(';')
            if sub_name is None:
                if len(vals) > 0:
                    return vals[0].strip()
            else:
                for item in vals:
                    if item.find('=') > 0:
                        s1, s2 = StrUtil.split2(item, '=')
                        if s1.lower() == sub_name.lower():
                            return s2


# WebAPI
class WebAPI:
    class API:
        def __init__(self, method, url, name, **kwargs):
            self.method = str(method).upper()  # HTTP method, such as 'GET', 'POST', 'DELETE', 'PUT'
            self.url = url        # the URL
            self.name = name      # function name
            self.kwargs = kwargs  # key-value arguments of the function
            self.headers = {}     # headers for request

        def call(self, **kwargs):
            """ call the api """
            req_headers = {"User-Agent": UserAgent.default}
            if isinstance(self.headers, dict):
                for key in self.headers:
                    req_headers[key] = self.headers[key]

            if self.method in ['GET', 'DELETE', 'HEAD']:
                params = kwargs
                post_data = {}
            else:
                params = {}
                post_data = kwargs

            response = requests.request(self.method, self.url, data=post_data, params=params, headers=req_headers)

            if response.status_code == 200:
                content_type = headers_get(response.headers, 'content-type')
                if isinstance(content_type, str):
                    if content_type.find('json') >= 0:
                        return response.json()
                return response.text
            else:
                raise ValueError('response code %s' % response.status_code)

    def __init__(self):
        self._apis = []

    def add_func(self, method, url, func_name, **kwargs):
        """
        Add a API function

        :param method:  HTTP method, such as 'GET', 'POST', 'DELETE', 'PUT'
        :param url:     url
        :param func_name:  function name
        :param kwargs:     key-value arguments of the function
        :return:  None
        """
        api = WebAPI.API(method, url, func_name, **kwargs)
        self._apis.append(api)

    def find_func(self, func_name):
        """
        Find a function
        :param func_name: function name
        :return: return WebAPI.API object if success. raise Exception if not found
        """
        for api in self._apis:
            if api.name == func_name:
                return api

    def call(self, func_name, **kwargs):
        """
        Call a function

        :param func_name:  function name
        :param kwargs:  key-value arguments of the function
        :return:  return the result of the function. raise exception if error occurs
        """
        api = self.find_func(func_name)
        if api:
            return api.call(**kwargs)
        else:
            raise NotImplemented('function %s not implemented' % func_name)

    def help(self, func_name=None):
        """ get help of API function"""
        result = {}
        for api in self._apis:
            if func_name is None or api.name == func_name:
                result[api.name] = api.kwargs
        return result

