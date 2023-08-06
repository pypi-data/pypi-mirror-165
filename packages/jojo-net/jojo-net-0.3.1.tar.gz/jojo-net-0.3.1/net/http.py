from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen
import json


__version__ = "0.5"
__author__ = "JoStudio"


# UserAgent
class UserAgent:
    chrome = 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36'
    default = 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36'


# Http V0.5
class Http:
    """
    Http Class

    """
    @staticmethod
    def get(url, params=None, headers=None):
        """ send a GET request"""
        return Http().request(url, params, headers=headers)

    @staticmethod
    def post(url, data=None, headers=None):
        """ send a POST request"""
        return Http().request(url, data, headers=headers, method='POST')

    @staticmethod
    def delete(url, params=None, headers=None):
        """ send a DELETE request"""
        return Http().request(url, params, headers=headers, method='DELETE')

    @staticmethod
    def head(url, params=None, headers=None):
        """ send a HEAD request"""
        return Http().request(url, params, headers=headers, method='HEAD')

    @staticmethod
    def put(url, data=None, headers=None):
        """ send a get request"""
        return Http().request(url, data, headers=headers, method='PUT')

    def __init__(self):
        self.req = None
        self.response = None
        self._content = None

    @staticmethod
    def _compose_get_url(url, params):
        """ compose HTTP GET url"""
        if isinstance(params, dict):
            if url.find('?') < 0:
                url += '?'
            else:
                if not url.endswith('&'):
                    url += '&'
            for name in params:
                url += quote(name) + '=' + quote(params[name])
        elif isinstance(params, list) or isinstance(params, tuple):
            for index, val in enumerate(params):
                url = url.replace('{%s}' % index, quote(str(val)))
        elif isinstance(params, str):
            url = url.replace('{0}', quote(params))
        elif params is None:
            pass
        else:
            raise ValueError('invalid params type %s' % params)

        return url

    def request(self, url, data=None, headers=None, method='GET'):
        r"""Sends a request.

            :param url: URL for the new :class:`Request` object.
            :param data: (optional) Dictionary, list of tuples or bytes to send
                in the query string for the :class:`Request`.
            :param headers: Optional headers of the request.
            :param method: Optional method of the request, 'GET', 'POST', 'PUT', 'DELETE', 'HEAD'.
            :return: return self
            """
        self.req = None
        self.response = None
        self._content = None
        # noinspection PyBroadException
        if method in ['GET', 'HEAD', 'DELETE']:
            url = Http._compose_get_url(url, data)
            data = None
        headers = {} if headers is None else headers
        req_headers = {"User-Agent": UserAgent.default}
        if isinstance(headers, dict):
            for key in headers:
                req_headers[key] = headers[key]
        self.req = Request(url, data=data, headers=headers, method="GET")
        self.response = urlopen(self.req)
        return self

    def save_to_file(self, filename):
        """ save response to file """
        filename = str(filename)
        if filename.rfind('.') < 0:
            filename += self._get_file_ext()
        f = open(filename, 'wb')
        f.write(self.response.read())
        f.close()
        return filename

    def _get_file_ext(self):
        fmt = self.response.headers.get_content_type()
        if isinstance(fmt, str):
            if fmt.find('/') >= 0:
                fmt = fmt[fmt.find('/') + 1:]
                return '.' + fmt
        return ''

    def header(self, name, sub_name=None):
        if self.response:
            name = name.lower()
            for key in self.response.headers:
                if key.lower() == name:
                    val = self.response.headers[key]
                    vals = val.split(';')
                    if sub_name is None:
                        if len(vals) > 0:
                            return vals[0].strip()
                    else:
                        for item in vals:
                            pos = item.find('=')
                            if pos > 0:
                                name = item[:pos]
                                value = item[pos+1:]
                                if name.lower() == sub_name.lower():
                                    return value

    @property
    def content_type(self):
        if self.response:
            return self.response.headers.get_content_type()

    @property
    def status_code(self):
        if self.response:
            return self.response.status
        return 0

    @property
    def text(self):
        """ get the text of response """
        if self.response:
            charset = self.header('Content-Type', 'charset')
            charset = 'utf-8' if not charset else charset
            return str(self.response.read(), encoding=charset)

    @property
    def content(self):
        """ get the bytes of response"""
        if not self._content:
            if self.response:
                self._content = self.response.read()
        return self._content

    def json(self, **kwargs):
        """ get the json data of response """
        return json.loads(self.text, **kwargs)


