
import scrapy
from Tencent.items import TencentItem

class TencentSpider(scrapy.Spider):
    #爬虫名
    name = 'tencent'
    #爬虫爬取数据的域范围
    allowed_domains = ["tencent.com"]
    #1、需要拼接的url
    baseURL = "http://hr.tencent.com/position.php?start="
    #2需要拼接的url偏移量
    offset = 0
    #爬虫启动时，读取的url地址列表
    start_urls = [baseURL+str(offset)]

    #用来处理response
    def parse(self, response):
        #提取每一个response的数据
        node_list = response.xpath("//tr[@class = 'even'] | //tr[@class = 'odd']")

        for node in node_list:
            #提取每个职位的信息
            item = TencentItem()
            item['positionName'] = node.xpath("./td[1]/a/text()").extract()[0]
            item['positionLink'] = node.xpath("./td[1]/a/@href").extract()[0]

            if len(node.xpath("./td[2]/text()")):
                item['positionType'] = node.xpath("./td[2]/text()").extract()[0]
            else:
                item['positionType'] = ""
            item['peopleNumber'] = node.xpath("./td[3]/text()").extract()[0]
            item['workLocation'] = node.xpath("./td[4]/text()").extract()[0]
            item['publishTime'] = node.xpath("./td[5]/text()").extract()[0]
            yield item

        # if self.offset < 3870:
        #     self.offset +=10
        #     url = self.baseURL + str(self.offset)
        #     scrapy.Request(url,callback=self.parse)

        # if not len(response.xpath("//a[@id='noactive' and @id = 'next']")):
        #     response.xpath("//a[@id='next']/@herf")

        if len(response.xpath("//a[@class='noactive' and @id = 'next']"))==0:
              url = response.xpath("//a[@id='next']/@href").extract()[0]
              yield scrapy.Request("http://hr.tencent.com/"+url,callback=self.parse)


















