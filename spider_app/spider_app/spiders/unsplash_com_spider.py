import json
import os
from datetime import datetime

import scrapy

from spider_app import settings
from spider_app.spiders import BaseSpider


class ImageSpiderSpider(BaseSpider):
    name = 'unsplash_spider'
    allowed_domains = ['unsplash.com']
    start_url = 'https://www.reshot.com/search/{keyword}'

    keywords = (
        'baby',
        # 'children',
        # 'middle%20aged%20man',
        # 'middle%20aged%20woman',
        # 'old%20man',
        # 'old%20woman',
    )
    base_next_page = 'https://unsplash.com/napi/search/photos?query={keyword}&xp=&per_page=20&page={page}'

    storage_path = os.path.join(settings.BASE_STORAGE, name)

    def __init__(self, keywords=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if keywords:
            self.keywords = keywords.split(',')
            self.keywords = [keyword.replace(' ', '%20') for keyword in self.keywords]

    def start_requests(self):
        for keyword in self.keywords:
            url = self.start_url.format(keyword=keyword)
            next_page = self.base_next_page.format(keyword=keyword, page=1)
            yield scrapy.Request(
                url=next_page,
                method='GET',
                callback=self.parse,
                headers={
                    'Referer': url,
                    'Content-Type': 'application/json'
                },
                meta={'keyword': keyword, 'page': 1, 'url': url}
            )
    
    def parse(self, response):
        keyword = response.meta['keyword']
        page = response.meta['page']
        url = response.meta['url']
        
        try:
            data = json.loads(response.body)
        except:
            data = {}
         
        total_pages = data.get('total_pages', 0)
        for img in data.get('results', []):
            img_url = img.get('urls', {}).get('full')
            if img_url is None:
                continue
            filename = img.get('id') or datetime.now().timestamp()
            yield scrapy.Request(
                url=img_url,
                method='GET',
                callback=self.download_attach_file,
                headers={
                    'Referer': url
                },
                meta={'keyword': keyword, 'filename': filename}
            )

        # go to next page
        page += 1
        if page > total_pages:
            return
        next_page = self.base_next_page.format(keyword=keyword, page=page)
        yield scrapy.Request(
                url=next_page,
                method='GET',
                callback=self.parse,
                headers={
                    'Referer': url,
                    'Content-Type': 'application/json'
                },
                meta={'keyword': keyword, 'page': page, 'url': url}
            )
