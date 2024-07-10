# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MenorprecoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    price = scrapy.Field()
    product = scrapy.Field()
    description = scrapy.Field()
    distance = scrapy.Field()
    period = scrapy.Field()


