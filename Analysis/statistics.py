# -*- coding:utf8 -*-

"""
统计MongoDB中的内容
"""
import pymongo

from config import MONGO_CONFIG, MONGO_SQL


class SimpleStatistics(object):
    """
    对爬取的结构化数据进行简单的统计，mongodb的sql统一在config.py文件中配置
    """

    def __init__(self):
        """
        获得mongodb的配置信息，连接到collection，读取配置文件的mongo_sql
        """
        # 创建MongoDB连接
        connection = pymongo.MongoClient(
            MONGO_CONFIG['MONGODB_SERVER'],
            int(MONGO_CONFIG['MONGODB_PORT'])
        )
        # 连接autohome数据库
        db_autohome = connection[MONGO_CONFIG['MONGODB_DB_AUTOHOME']]
        self.collection_article = db_autohome[MONGO_CONFIG['MONGODB_COLLECTION_ARTICLE']]
        # 从配置文件获取统计的mongodb脚本
        self.mongo_sql = MONGO_SQL['statistics']

    def editor_article_count(self):
        """
        各个小编的发文量
        """
        result = [
            item for item in \
            self.collection_article.aggregate(self.mongo_sql['editor_article_count'])
        ]
        return result

    def editor_comment_count(self):
        """
        各个小编获得的评论数量
        """
        result = [
            item for item in \
            self.collection_article.aggregate(self.mongo_sql['editor_comment_count'])
        ]
        return result


if __name__ == '__main__':
    conn = SimpleStatistics()
    conn.editor_article_count()
    conn.editor_comment_count()
