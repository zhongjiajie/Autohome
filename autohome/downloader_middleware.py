#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import logging
import re

import pymongo
from scrapy.conf import settings
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

logger = logging.getLogger(__name__)


class RotateUserAgentMiddleware(UserAgentMiddleware):
    """
    MongoDB中随机选择一个UA 实现防反爬
    """

    # the default user_agent_list composes chrome,I E,firefox,Mozilla,opera,netscape
    # for more user agent strings,you can find it in http://www.useragentstring.com/pages/useragentstring.php
    def __init__(self, user_agent=''):
        self.user_agent = user_agent
        # 创建MongoDB连接
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db_ua = connection[settings['MONGODB_USER_AGENT']]
        self.collection_user_agent = db_ua[settings['MONGODB_COLLECTION_USER_AGENT']]
        # 设置首次调用RotateUserAgentMiddleware类标识
        self.rotate_user_agent_first_time = True

    def process_request(self, request, spider):
        # 如果首次调用RotateUserAgentMiddleware类 mongodb中还未有user agent 调用默认的UA
        # 非首次调用就在MongoDB中随机选择一个UA
        if self.rotate_user_agent_first_time:
            self.rotate_user_agent_first_time = False
            request.headers['User-Agent'] = ('Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) '
                                             'Chrome/41.0.2228.0 Safari/537.36')
            logger.debug('first ua: {}'.format(request.headers['User-Agent']))
        else:
            # 从MongDB中随机获取一个ua的doc '$sample'mongodb 3.2以上支持
            for doc in self.collection_user_agent.aggregate([{'$sample': {'size': 1}}]):
                request.headers['User-Agent'] = doc['ua']
                logger.debug('request user agent change to {}'.format(request.headers['User-Agent']))


class RotateProxyMiddleware(object):
    """
    MongoDB中随机选择一个IP 实现防反爬
    """

    def __init__(self):
        # 创建MongoDB连接
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db_proxy = connection[settings['MONGODB_PROXY']]
        self.collection_proxy = db_proxy[settings['MONGODB_COLLECTION_PROXY']]

    def process_request(self, request):
        """
        每次向服务器提交就随机选择
        :param request: 
        :return: 
        """
        # 从mongodb中随机选择一个doc 拼接 并设置自动提交
        for doc in self.collection_proxy.aggregate([{'$sample': {'size': 1}}]):
            request.meta['proxy'] = 'http://{}:{}'.format(doc['ip'], doc['port'])
            request.headers['Proxy-Authorization'] = 'Basic {}'.format(base64.b64encode(''))
            logger.debug('proxy change to {}'.format(request.meta['proxy']))

    def process_response(self, request, response):
        """
        没有返回正确状态码就删除该访问的IP
        :param request: 
        :param response: 
        :return: 
        """
        if response.status != 200 and 'proxy' in request.meta:
            logger.debug('Response status: {0} using proxy {1} retrying request to {2}'.format(response.status,
                                                                                               request.meta['proxy'],
                                                                                               request.url))
            proxy = request.meta['proxy']
            del request.meta['proxy']
            # 在MongoDB中删除访问失败的IP
            try:
                ip, port = re.search('http://(.*):(.*)', proxy).group(1, 2)
                self.collection_proxy.delete_one({'ip': ip, 'port': int(port)})
                logger.info('removed banned proxy {}:{}'.format(ip, port))
            except KeyError:
                logger.info('can not delete banned proxy {}:{}'.format(ip, port))
            return request
        return response
