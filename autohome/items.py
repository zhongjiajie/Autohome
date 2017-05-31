#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AutohomeArticleShortItem(scrapy.Item):
    """
    文章首页的缩略信息
    """
    # 文章url
    article_url = scrapy.Field()
    # 文章首页缩略图
    article_pic = scrapy.Field()
    # 文章标题
    article_title = scrapy.Field()
    # 文章发布时间
    article_pub_time = scrapy.Field()
    # 文章阅读数量
    article_read_num = scrapy.Field()
    # 文章缩略前面篇幅
    article_short = scrapy.Field()


class AutohomeArticleItem(scrapy.Item):
    """
    详细文章页面信息
    """
    # 车辆型号
    car_name = scrapy.Field()
    # 车辆连接
    car_link = scrapy.Field()  # 可进一步解析
    # 车辆所属类型
    car_type = scrapy.Field()
    # 车辆在该类型的排名
    car_type_rank = scrapy.Field()
    # 文章url
    article_url = scrapy.Field()
    # 文章标题
    article_title = scrapy.Field()
    # 所属分类
    article_classify = scrapy.Field()
    # 发布时间
    article_pub_time = scrapy.Field()
    # 文章来源
    article_from = scrapy.Field()
    # 文章类型
    article_type = scrapy.Field()
    # 文章作者
    article_writer = scrapy.Field()
    # 文章评论数量
    article_comment_num = scrapy.Field()
    # 详细文章
    article_detail = scrapy.Field()
    # 文章图片
    article_photo = scrapy.Field()  # 可进一步解析
    # 文章标签
    article_tag = scrapy.Field()
    # 文章标签连接
    article_tag_link = scrapy.Field()  # 可进一步解析
    # 文章评论连接
    article_comment_link = scrapy.Field()  # 可进一步解析


class AutohomeCommentItem(scrapy.Item):
    """
    评论页面，每一个连接有一个或多个评论页面
    """
    # 文章链接
    article_url = scrapy.Field()
    # 评论页面
    comment_page = scrapy.Field()
    # 评论列表
    comment_list = scrapy.Field()


class AutohomeUserItem(scrapy.Item):
    """
    用户页面
    """
    # 用户编号
    user_id = scrapy.Field()
    # 用户名
    user_name = scrapy.Field()
    # 用户头像
    user_img = scrapy.Field()
    # 创建时间
    create_time = scrapy.Field()
    # 最后编辑时间
    last_edit_time = scrapy.Field()
    # 是否绑定手机
    tie_phone = scrapy.Field()
    # 关注数
    following_num = scrapy.Field()
    # 关注用户
    user_following = scrapy.Field()
    # 粉丝数
    followers_num = scrapy.Field()
    # 粉丝用户
    user_followers = scrapy.Field()
    # 所在地
    user_location = scrapy.Field()
    # 性别
    user_sex = scrapy.Field()
    # 帮助值
    help_score = scrapy.Field()
    # 精华帖数
    jh_topic_count = scrapy.Field()
    # 主贴数
    topics_count = scrapy.Field()
    # 关注车数量
    concern_car_count = scrapy.Field()
    # 关注车库
    concern_carbarn = scrapy.Field()
    # 主帖连接
    topics_link = scrapy.Field()
    # 发出回复连接
    reply_forum_link = scrapy.Field()
