import scrapy

import os
from dotenv import load_dotenv


class LinkedinSpider(scrapy.Spider):
    name = 'linkedin'

    def start_requests(self):
        url = "https://www.linkedin.com"
        email = os.getenv('USERNAME')
        password = os.getenv('PASSWORD')

        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for item in range(1):
            yield {
                'test': 'test '
            }



