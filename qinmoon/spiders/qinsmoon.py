# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy import Request

from qinmoon.items import QinmoonItem


class QinsmoonSpider(scrapy.Spider):
    name = 'qinsmoon'
    allowed_domains = ['www.4399dmw.com']

    start_qinmoon_url='http://www.4399dmw.com/qinshimingyue/tupian/'

    per_url_list=[]

    def start_requests(self):
        yield Request(self.start_qinmoon_url,self.parse_qinmoon_page)

    def parse_qinmoon_page(self,response):
        # print('111111')
        pass
        list_album_list = response.css('.dm_main .dmp_imglist li a::attr(href)').extract()
        #得到每一个画册的集
        for list in list_album_list:
            list='http://www.4399dmw.com'+list
            yield Request(list,self.parse_per_qinmoon)

        #得到下一页的链接
        next_page_url=response.css('.dm_main .bd .dm_page .next::attr(href)').extract_first()
        if next_page_url:
           yield Request('http://www.4399dmw.com'+next_page_url, self.parse_qinmoon_page)

    def parse_per_qinmoon(self,response):
        #单张图片的url
        per_img_url = response.css('.dm_warp .dm_main .bd .g_picsbox .g_pics img::attr(src)').extract_first()
        #判断该图集共有多少
        mstr=response.css('.dm_warp .dm_main .bd .g_pics_info span').extract_first()
        img_num =int(re.findall('共(\d+)张',mstr)[0])

        for page in range(1,img_num):
            per_url=re.findall('(.*?)\d+.jpg', per_img_url)[0]+str(page)+'.jpg'
            #得到所有url：类似 http://dmimg.5054399.com/allimg/160119/15_160119100819_6.jpg
            #接下来自定义属于我们的middleware
            self.per_url_list.append(per_url)
            item = QinmoonItem()
            item['image_urls'] = self.per_url_list
            album_name = response.css('.dm_warp .dm_win .bd .g_picsbox .dm_title::text ').extract_first()[:-1]
            item['name'] = album_name
            yield item


