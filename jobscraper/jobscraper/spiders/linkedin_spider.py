import scrapy
from scrapy_splash import SplashRequest
import os
from dotenv import load_dotenv


class LinkedinSpider(scrapy.Spider):
    name = 'linkedin'

    def start_requests(self):
        url = "https://www.linkedin.com"
        email = os.getenv('USERNAME')
        password = os.getenv('PASSWORD')
        script = f"""
            function main(splash)
                local url = splash.args.url
                assert(splash:go(url))
                assert(splash:wait(10))

                splash:set_viewport_full()

                local search_input = splash:select('input[name=session_key]')   
                search_input:send_text("{email}")
                local search_input = splash:select('input[name=session_password]')
                search_input:send_text("{password}")
                assert(splash:wait(5))
                local submit_button = splash:select('button[class="sign-in-form__submit-button"]')
                submit_button:click()

                assert(splash:wait(10))

                return {{
                    html = splash:html(),
                    png = splash:png(),
                }}
            end
            """
        yield SplashRequest(url=url, callback=self.parse)

    def parse(self, response):
        for item in range(1):
            yield {
                'test': 'test '
            }
