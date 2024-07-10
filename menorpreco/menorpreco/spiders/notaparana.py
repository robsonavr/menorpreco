from typing import Iterable
import scrapy
from scrapy_playwright.page import PageMethod
from menorpreco.items import MenorprecoItem
import time


class NotaparanaSpider(scrapy.Spider):
    name = "notaparana"
    allowed_domains = ["menorpreco.notaparana.pr.gov.br"]
    basket = ['sabao po omo']
    custom_settings = {
        "REQUEST_FINGERPRINTER_IMPLEMENTATION": "2.7",
        'DOWNLOAD_DELAY': 10, # seconds of delay
        'RANDOMIZE_DOWNLOAD_DELAY': True
    }


    def start_requests(self):
        start_url = f"https://menorpreco.notaparana.pr.gov.br/app?termo={self.basket[0]}&local=6gkzqf9vb"
        yield scrapy.Request(start_url, meta=dict(
            playwright =  True,
            playwright_include_page = True,
            playwright_page_methods = [
                PageMethod("wait_for_selector", "button"),
                PageMethod("click", "button.button.mat-button"),
                PageMethod("wait_for_selector", "div.list-item"),
                PageMethod("click", "div.desc-categoria") if PageMethod("isVisible", "div.desc-categoria") else None
            ]),
        errback = self.errback
            )
        

    async def parse(self, response):
        page = response.meta["playwright_page"]
        await page.close()

        Item_menorpreco = MenorprecoItem()

        for item in response.css('div.list-item'):
            Item_menorpreco['price'] = item.css('span.preco::text').get()
            Item_menorpreco['product'] = item.css('span.product::text').get()
            Item_menorpreco['description'], Item_menorpreco['distance'] , Item_menorpreco['period'] = item.css('span.desc::text').getall()

            yield Item_menorpreco

        for basket_item in self.basket[1:]:
            start_url = f"https://menorpreco.notaparana.pr.gov.br/app?termo={basket_item}&local=6gkzqf9vb"
            yield scrapy.Request(start_url, meta=dict(
                playwright =  True,
                playwright_include_page = True,
                playwright_page_methods = [
                    PageMethod("wait_for_selector", "button"),
                    PageMethod("click", "button.button.mat-button"),
                    PageMethod("wait_for_selector", "div.list-item"),
                ]),
            errback = self.errback
                )


    async def errback(self, failure):
        page = failure.request.meta['playwright_page']
        await page.close()

