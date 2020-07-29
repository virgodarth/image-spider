import magic
import scrapy
import os
import pathlib

from abc import ABC


class BaseSpider(scrapy.Spider, ABC):
    name = None
    parser = None
    storage_path = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mime = magic.Magic(mime=True)

    def download_attach_file(self, response):
        filename = response.meta.get('filename')
        tagname = response.meta.get('tagname').replace('%20', '_')
        
        buffer = response.body
        try:
            _, ext = self.mime.from_buffer(buffer).rsplit('/', 1)
        except ValueError:
            return
        filename += f'.{ext}'
        
        absolute_path = os.path.join(self.storage_path, tagname)
        pathlib.Path(absolute_path).mkdir(parents=True, exist_ok=True)
        
        # save orignal image
        org_fullpath = os.path.join(absolute_path, filename)
        with open(org_fullpath, 'wb') as fo:
            fo.write(buffer)
