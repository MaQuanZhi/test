# -*- coding: utf-8 -*-
import scrapy
from dangdang.items import DangdangItem
from bs4 import BeautifulSoup
from bs4 import UnicodeDammit


class Spider1Spider(scrapy.Spider):
    name = 'spider1'
    allowed_domains = ['search.dangdang.com']
    start_urls = ['http://search.dangdang.com/']
    key = 'python'

    def start_requests(self):
        url = Spider1Spider.start_urls[0] + "?key=" + Spider1Spider.key
        print("start_requests url:", url)
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        try:
            # 解析页面
            dammit = UnicodeDammit(response.body, ["utf8", "gbk"])
            data = dammit.unicode_markup
            selector = scrapy.Selector(text=data)
            lis = selector.xpath("//li[re:test(@class, 'line')]")
            for li in lis:
                title = li.xpath("./a//@title").extract_first()
                detail = li.xpath("./p[@class='detail']/text()").extract_first()
                price = li.xpath("./p/span[@class='search_now_price']/text()").extract_first()
                author = li.xpath("./p[@class='search_book_author']/span/a[1]//@title").extract_first()
                date = li.xpath("./p[@class='search_book_author']/span[last()-1]/text()").extract_first()
                publisher = li.xpath("./p[@class='search_book_author']/span/a[@name='P_cbs']/text()").extract_first()

                item = DangdangItem()
                item["title"] = str(title).strip() if title else ""
                item["author"] = str(author).strip() if author else ""
                item["date"] = str(date).strip() if date else ""
                item["publisher"] = str(publisher).strip() if publisher else ""
                item["price"] = str(price).strip() if price else ""
                item["detail"] = str(detail).strip().replace('"', '').replace('\'', '') if detail else ""
                yield item
            link = selector.xpath("//li[@class='next']/a/@href").extract_first()
            # 下一页
            if link:
                url = response.urljoin(link)
                print(url)
                yield scrapy.Request(url=url, callback=self.parse)
        except Exception as e:
            print(e)
