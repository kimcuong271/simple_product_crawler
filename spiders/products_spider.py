from pathlib import Path
import scrapy
import re
import pandas as pd
import time
import json
from productbot.items import ProductbotItem
class ProductSpider(scrapy.Spider):
    name = "PL"
    start_urls = ['https://phuclong.com.vn/category','https://phuclong.com.vn/category/thuc-uong','https://phuclong.com.vn/category/snacks','https://phuclong.com.vn/category/bakery']

    def parse(self,response):
        if response.url == 'https://phuclong.com.vn/category':
            for url in response.xpath('//a[@class="btn btn-primary"]/@href').extract():
                #time.sleep(1)
                yield scrapy.Request(url=url,callback=self.parse_cate)
        else:
            yield scrapy.Request(url=response.url,callback=self.get_product_order_page)
    
    def parse_cate(self,respone):
        for product in respone.xpath('//a[@class="item-wrapper"]/@href').extract():
            if product not in ['https://order.phuclong.com.vn/']:
                print(product)
                yield scrapy.Request(url=product,callback=self.get_data)

    def get_data(self,response):
        if response.status == 200:
            product_id = response.url.split('/')[-1]
            product_name = response.xpath('//h2[@class="item-info__name"]/text()').get()
            description = response.xpath('//div/ul/li[contains(text(),"Mô tả")]/text()').get()
            steps = len(response.xpath('//ul[@class="breadcrumb"]/li'))
            item = ProductbotItem()
            item["product_id"] = product_id
            item["product_name"] = product_name
            item["descrition"] = description
            item["steps"] = steps
            #print(item)
            return(item)
        else:
            print(response.text)
            
    def get_product_order_page(self,response):
        for item in response.xpath('//div[@class="item-info"]'):
            product_id = item.xpath('.//button/@data-id').get()
            product_name = item.xpath('.//div[@class="item-name"]/text()').get()
            description = item.xpath('.//div[@class="item-desc"]/text()').get().replace('\n', '').strip()
            steps = 2
            item = ProductbotItem()
            item["product_id"] = product_id
            item["product_name"] = product_name
            item["descrition"] = description
            item["steps"] = steps
            yield item
    # def start_requests(self):
    #     start_url = 'https://phuclong.com.vn/category'
    #     cate_urls = yield scrapy.Request(url=start_url,callback=self.get_url)
    #     # = .xpath('//a[@class="btn btn-primary"]/@href').extract()
    #     #remove order 
    #     cate_urls.remove('https://order.phuclong.com.vn/')
    #     product_list = []
    #     for cate in cate_urls:
    #         resp = scrapy.Request(url=cate)
    #         product_urls = resp.xpath('//a[@class="item-wrapper"]/@href').extract()
    #         for product in product_urls:
    #             tmp = scrapy.Request(url=product,callback=self.get_data)
    #             product_list.append(tmp)
    #     df = pd.DataFrame(product_list,columns=['product_id','product_name','description','step'])
    #     df.to_csv('output.csv',index=False)
    # def get_url(self,repsonse):
    #     urls = repsonse.xpath('//a[@class="btn btn-primary"]/@href').extract()
    #     return urls
    # def get_data(self,response):
        product_id = response.url.split('/')[-1]
        product_name = re.findall(r'<li>(.*?)</li>',response.xpath('//li[@class="active"]').get())
        description = re.findall(r'<li>(.*?)</li>',response.xpath('//div/ul/li[contains(text(),"Mô tả")]').get())
        steps = len(response.xpath('//ul[@class="breadcrumb"]/li'))
        return [product_id,product_name,description,steps]