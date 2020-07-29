import os
from http.cookiejar import CookieJar
from urllib.parse import urlparse

from fake_useragent import UserAgent
from spider_app import settings as project_settings


class CookieJarMiddleware:
    def __init__(self, settings):
        pass

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        cookie_jar = request.meta.setdefault('cookie_jar', CookieJar())
        cookie_jar.extract_cookies(request, request)

        request.meta['cookie_jar'] = cookie_jar
        request.meta['dont_merge_cookies'] = True


class UserAgentMiddleware:
    def __init__(self,  settings):
        self.ua = UserAgent(path=os.path.join(project_settings.PROJECT_ROOT, 'data', 'ua-0.1.11.json'))

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        request.headers.setdefault('Host', urlparse(request.url).hostname)
        request.headers.setdefault('User-Agent', self.ua.random)
