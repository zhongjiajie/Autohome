# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from GetUserAgent.items import UserAgentItem
from scrapy.conf import settings


class UseragentMongodbPipeline(object):
    def __init__(self):
        # 创建MongoDB连接
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        # 连接user_agent数据库
        db_ua = connection[settings['MONGODB_USER_AGENT']]
        self.collection_user_agent = db_ua[settings['MONGODB_COLLECTION_USER_AGENT']]
        # 重跑的时候删除原来的user_agent
        self.collection_user_agent.remove()

    def process_item(self, item, spider):
        if isinstance(item, UserAgentItem):
            self.collection_user_agent.insert(dict(item))
            return item
