# -*- coding:utf-8 -*-

import re

from GetUserAgent.items import UserAgentItem
from scrapy.spiders import Spider


class UserAgentSpider(Spider):
    name = 'user_agent'
    allowed_domains = ['useragentstring.com']
    # 默认是爬取 chrome chromeplus firefox safari 的UA
    start_urls = [
        'http://www.useragentstring.com/pages/useragentstring.php?name=Chrome',
        'http://www.useragentstring.com/pages/useragentstring.php?name=ChromePlus',
        'http://www.useragentstring.com/pages/useragentstring.php?name=Firefox',
        'http://www.useragentstring.com/pages/useragentstring.php?name=Safari'
    ]

    def parse(self, response):
        ua_list = response.xpath('//div[@id="liste"]/ul/li/a/text()').extract()
        ua_type = re.search(r'\?name=(.*)', response.url).group(1)
        for each_ua in ua_list:
            user_agent = UserAgentItem()
            user_agent['ua_type'] = ua_type
            user_agent['ua'] = each_ua
            yield user_agent
