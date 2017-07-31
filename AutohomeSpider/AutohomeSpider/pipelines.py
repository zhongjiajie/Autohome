#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json
import os

import pymongo
from AutohomeSpider.items import AutohomeArticleShortItem, AutohomeArticleItem, AutohomeCommentItem, AutohomeUserItem
from scrapy.conf import settings
from scrapy.exceptions import DropItem


class AutohomeJsonPipeline(object):
    def __init__(self):
        """
        重跑程序时，删除文件，文件头加[组成完整json文件
        """
        # 删除存在文件
        self.remove_exists_file('autohome_article_short.json')
        self.remove_exists_file('autohome_article.json')
        self.remove_exists_file('autohome_article_comment.json')
        self.remove_exists_file('autohome_user.json')

        # 汽车之家文章缩略页面
        self.article_short_wrt = codecs.open('autohome_article_short.json', 'a', encoding='utf-8')
        self.article_short_wrt.write('[\n')
        self.article_short_first_item = True

        # 汽车之家文件详情
        self.article_wrt = codecs.open('autohome_article.json', 'a', encoding='utf-8')
        self.article_wrt.write('[\n')
        self.article_first_item = True

        # 汽车之家评论详情
        self.article_comment_wrt = codecs.open('autohome_article_comment.json', 'a', encoding='utf-8')
        self.article_comment_wrt.write('[\n')
        self.article_comment_first_item = True

        # 汽车之家用户详情
        self.article_user_wrt = codecs.open('autohome_user.json', 'a', encoding='utf-8')
        self.article_user_wrt.write('[\n')
        self.article_user_first_item = True

    def remove_exists_file(self, file_name):
        """
        删除存在的文件
        :param file_name: 要判断删除的文件名
        :return: 
        """
        if os.path.exists(file_name):
            os.remove(file_name)

    def process_item(self, item, spider):
        """
        通过isinstance判断属于哪个item实例，然后进行不同的pipeline
        :param item: spider传递过来的item
        :return: return item
        """
        if isinstance(item, AutohomeArticleShortItem):
            # 文章连接为空就删除
            if not item['article_url']:
                raise DropItem("Missing article url, drop it")
            # 判断是否第一行
            if self.article_short_first_item:
                self.article_short_first_item = False
            else:
                self.article_short_wrt.write(',\n')
            line = json.dumps(dict(item))
            self.article_short_wrt.write(line.decode("unicode_escape"))
            return item

        elif isinstance(item, AutohomeArticleItem):
            # 判断是否第一行
            if self.article_first_item:
                self.article_first_item = False
            else:
                self.article_wrt.write(',\n')
            line = json.dumps(dict(item))
            self.article_wrt.write(line.decode("unicode_escape"))
            return item

        elif isinstance(item, AutohomeCommentItem):
            # 判断是否第一行
            if self.article_comment_first_item:
                self.article_comment_first_item = False
            else:
                self.article_comment_wrt.write(',\n')
            line = json.dumps(dict(item))
            self.article_comment_wrt.write(line.decode("unicode_escape"))
            return item

        elif isinstance(item, AutohomeUserItem):
            # 判断是否第一行
            if self.article_user_first_item:
                self.article_user_first_item = False
            else:
                self.article_user_wrt.write(',\n')
            line = json.dumps(dict(item))
            self.article_user_wrt.write(line.decode("unicode_escape"))
            return item

        else:
            pass

    def __del__(self):
        """
        在文件末尾增加]组成完整json文件
        关闭文件句柄
        """
        self.article_short_wrt.write('\n]')
        self.article_short_wrt.close()
        self.article_wrt.write('\n]')
        self.article_wrt.close()
        self.article_comment_wrt.write('\n]')
        self.article_comment_wrt.close()
        self.article_user_wrt.write('\n]')
        self.article_user_wrt.close()


class AutohomeMongodbPipeline(object):
    def __init__(self):
        """
        scrapy.conf读取配置文件中的MongDB配置，并将MongDB几个collections中的数据清空
        """
        # 创建MongoDB连接
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        # 连接autohome数据库
        db_autohome = connection[settings['MONGODB_AUTOHOME']]
        self.collection_article_short = db_autohome[settings['MONGODB_COLLECTION_ARTICLE_SHORT']]
        self.collection_article = db_autohome[settings['MONGODB_COLLECTION_ARTICLE']]
        self.collection_comment = db_autohome[settings['MONGODB_COLLECTION_COMMENT']]
        self.collection_user = db_autohome[settings['MONGODB_COLLECTION_USER']]
        # 将要写入的collection清空
        self.collection_article_short.remove()
        self.collection_article.remove()
        self.collection_comment.remove()
        self.collection_user.remove()

    def process_item(self, item, spider):
        """
        根据进来的item属于哪个items的实例，判断应该写入MongDB的那个collections
        :param item: spider传递过来的item
        :return: 
        """
        # TODO insert可能会有数据库写入的瓶颈，可以考虑用insert_many实现快速写入
        if isinstance(item, AutohomeArticleShortItem):
            self.collection_article_short.insert(dict(item))
            return item

        if isinstance(item, AutohomeArticleItem):
            self.collection_article.insert(dict(item))
            return item

        if isinstance(item, AutohomeCommentItem):
            self.collection_comment.insert(dict(item))
            return item

        if isinstance(item, AutohomeUserItem):
            self.collection_user.insert(dict(item))
            return item
