#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import datetime

# Scrapy settings for autohome project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'AutohomeSpider'

SPIDER_MODULES = ['AutohomeSpider.spiders']
NEWSPIDER_MODULE = 'AutohomeSpider.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# 设置默认的USER_AGENT
# USER_AGENT = 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# DOWNLOAD_TIMEOUT
DOWNLOAD_TIMEOUT = 180

# retry time
RETRY_TIMES = 6

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# 并发请求数量
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# 设置访问频率
# DOWNLOAD_DELAY = 0.3
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# 是否允许使用cookie
# COOKIES_ENABLED = False
# 查看每一个cookie
COOKIES_DEBUG = True

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# 默认request 的headers
DEFAULT_REQUEST_HEADERS = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive'
}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'autohome.middlewares.MyCustomSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#     # 禁止默认的UserAgentMiddleware，启用新的
#     'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
#     'AutohomeSpider.downloader_middleware.RotateUserAgentMiddleware': 400,
#     'AutohomeSpider.downloader_middleware.RotateProxyMiddleware': 450,
# }

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # 'AutohomeSpider.pipelines.AutohomeMongodbPipeline': 100,
    'AutohomeSpider.pipelines.AutohomeJsonPipeline': 300,
}

# Configure MongoDB connection
MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017

# Configure MongoDB database
# MongoDB database autohome
MONGODB_AUTOHOME = "autohome"
MONGODB_COLLECTION_ARTICLE_SHORT = "article_short"
MONGODB_COLLECTION_ARTICLE = "article"
MONGODB_COLLECTION_COMMENT = "comment"
MONGODB_COLLECTION_USER = "user"
# MongoDB database user agent
MONGODB_USER_AGENT = "user_agent"
MONGODB_COLLECTION_USER_AGENT = "user_agents"
# MongoDB database proxy
MONGODB_PROXY = "proxy"
MONGODB_COLLECTION_PROXY = "proxys"

# autohome account configure
AUTOHOME_USER_NAME = '15692427903'
AUTOHOME_PASSWORD = 'Zjjcxf955293'

# Configure log file level
# LOG_LEVEL = 'INFO'

# Configure log file name
# LOG_FILE = '{}.log'.format(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))

# configure proxy list
# PROXIES = [
#     {'ip_port': '222.82.222.242:9999', 'user_pass': ''},
#     {'ip_port': '115.231.105.109:8081', 'user_pass': ''},
#     {'ip_port': '115.231.175.68:8081', 'user_pass': ''},
#     {'ip_port': '218.76.106.78:3128', 'user_pass': ''},
#     {'ip_port': '124.88.67.54:80', 'user_pass': ''},
#     {'ip_port': '60.27.244.158:9999', 'user_pass': ''},
#     {'ip_port': '116.62.45.185:3128', 'user_pass': ''},
#     {'ip_port': '182.92.207.196:3128', 'user_pass': ''},
#     {'ip_port': '219.132.232.61:9797', 'user_pass': ''},
#     {'ip_port': '218.65.30.28:8118', 'user_pass': ''},
#     {'ip_port': '222.161.56.166:9000', 'user_pass': ''},
# ]

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
