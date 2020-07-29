import json
import os
from datetime import datetime

import scrapy

from spider_app import settings
from spider_app.spiders import BaseSpider


class ImageSpiderSpider(BaseSpider):
    name = 'unsplash_spider'
    allowed_domains = ['unsplash.com']
    start_url = 'https://www.reshot.com/search/{tagname}'

    tags = (
        'baby'
        'children',
        'middle%20aged%20man',
        'middle%20aged%20woman'
        'old%20man',
        'old%20woman'
    )
    base_next_page = 'https://unsplash.com/napi/search/photos?query={tagname}&xp=&per_page=20&page={page}'

    storage_path = os.path.join(settings.BASE_STORAGE, name)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    def start_requests(self):
        for tag in self.tags:
            url = self.start_url.format(tagname=tag)
            next_page = self.base_next_page.format(tagname=tag, page=1)
            yield scrapy.Request(
                url=next_page,
                method='GET',
                callback=self.parse,
                headers={
                    'Referer': url,
                    'Content-Type': 'application/json'
                },
                meta={'tagname': tag, 'page': 1, 'url': url}
            )
    
    def parse(self, response):
        tagname = response.meta['tagname']
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
                meta={'tagname': tagname, 'filename': filename}
            )

        # go to next page
        page += 1
        if page > total_pages:
            return
        next_page = self.base_next_page.format(tagname=tagname, page=page)
        yield scrapy.Request(
                url=next_page,
                method='GET',
                callback=self.parse,
                headers={
                    'Referer': url,
                    'Content-Type': 'application/json'
                },
                meta={'tagname': tagname, 'page': page, 'url': url}
            )
