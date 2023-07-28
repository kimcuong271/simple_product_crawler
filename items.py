# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductbotItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #  {"product_id":product_id,
    #                "product_name":product_name,
    #                "descrition":description,
    #                "steps":steps}
    product_id = scrapy.Field()
    product_name  = scrapy.Field()
    descrition  = scrapy.Field()
    steps  = scrapy.Field()