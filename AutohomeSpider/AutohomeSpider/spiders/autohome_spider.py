#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import logging
import math
import random
import re
import time

from AutohomeSpider.items import AutohomeArticleShortItem, AutohomeArticleItem, AutohomeCommentItem, AutohomeUserItem
from scrapy import Request, FormRequest
from scrapy.spiders import Spider

logger = logging.getLogger(__name__)


class AutohomeSpider(Spider):
    """
    Autohome爬虫主程序 提交requests 解析response的绝大部分逻辑
    """
    name = 'autohome_article'
    allowed_domains = ['autohome.com.cn']
    start_urls = 'http://www.autohome.com.cn/all/'

    def __init__(self):
        # 登陆autohome链接 （post方法提交表单）
        self.account_valid_part = 'http://account.autohome.com.cn/Login/ValidIndex'
        self.account_part = 'http://account.autohome.com.cn/Login'
        # 文章缩略图下一页连接 （页面数字）
        self.article_next_page_part = 'http://www.autohome.com.cn{}'
        # 文章回复数量连接 （文章id）
        self.reply_count_part = 'http://reply.autohome.com.cn/api/QueryComment/CountsByObjIds?_appid=cms&appid=1&dataType=json&objids={}'
        # 文章评论链接 （通过post方法提交）
        self.article_commnet_part = 'http://reply.autohome.com.cn/api/comments/show.json?count=50'
        # 用户主页
        self.user_home_part = 'http://i.autohome.com.cn/{}'
        # 用户活跃度连接 （用户id, 随机数, timestamp）
        self.user_activity_part = 'http://i.autohome.com.cn/ajax/home/GetUserInfo?userid={}&r={}&_={}'
        # 用户车库连接 （随机数, 用户id）
        self.user_carbarn_part = 'http://i.autohome.com.cn/ajax/home/OtherHomeAppsData?appname=Car&r={}&TuserId={}'
        # 用户关注连接 （用户id, 关注页面数）
        self.user_following_part = 'http://i.autohome.com.cn/{}/following?page={}'
        # 用户粉丝连接 （用户id, 粉丝页面数）
        self.user_followers_part = 'http://i.autohome.com.cn/{}/followers?page={}'

    def start_requests(self):
        """
        重写start_requests方法 开始抓取页面
        :return: 
        """
        yield Request(self.start_urls, callback=self.parse_article_short)

    def parse_article_short(self, response):
        """
        解析文章首页的缩略信息页面
        迭代缩略文章首页的下一页Request,callback=parse_article_short
        迭代详细文章的Requests,callback=parse_article
        :param response: 从Internet中返回的response对象
        :return: 
        """
        article_short_item = AutohomeArticleShortItem()
        # 整个页面将文章分成四大块，遍历每一块
        for four_part_article in response.xpath('//ul[@class="article"]'):
            # 四大块里面各有真正的文章内容
            for each_short_article in four_part_article.xpath('.//li'):
                # 判断文章的url是否为空，将url是空的抛弃，解析非空的页面
                if each_short_article.xpath('.//a/@href').extract():
                    article_short_item['article_url'] = each_short_article.xpath('.//a/@href').extract()[0]
                    article_short_item['article_pic'] = each_short_article.xpath('.//img/@src').extract()[0]
                    article_short_item['article_title'] = each_short_article.xpath('.//h3/text()').extract()[0]
                    article_short_item['article_pub_time'] = \
                        each_short_article.xpath('.//span[@class="fn-left"]/text()').extract()[0]
                    read_commnet_node = each_short_article.xpath('.//span[@class="fn-right"]')
                    # 获取评论数量放在parse_article中获取
                    article_short_item['article_read_num'] = read_commnet_node.xpath('.//em[1]/text()').extract()[0]
                    # 文章缩略图有部分没有文字
                    article_short_item['article_short'] = ''.join(
                        each_short_article.xpath('.//p/text()').extract()).strip()
                    yield article_short_item
                    # 迭代详细文章
                    article_url = dict(article_short_item)['article_url']
                    yield Request(article_url, callback=self.parse_article)
                else:
                    logger.warning(('`parse_article_short` function warning: one of page `{}` '
                                    'article has no detail text.').format(response.url))

        # 迭代下一页
        next_url_part = ''.join(
            response.xpath('//div[@id="channelPage"]/a[@class="page-item-next"]/@href').extract()).strip()
        if next_url_part != '':
            # 迭代缩略文章首页的下一页Request
            article_next_url = self.article_next_page_part.format(next_url_part)
            yield Request(article_next_url, callback=self.parse_article_short)
        else:
            logger.info('arrive THE END OF article short page')

    def parse_article(self, response):
        """
        解析详细文章信息。其中一个是普通页面，可以直接解析；另一个是特殊页面，要找到原始的url再yield回来解析
        迭代文章评论页面Request,callback=pase_article_comment
        迭代车型页面Request,callback=pase_car
        :param response: 
        :return: 
        """
        # TODO 考虑迭代标签分类页面 增加一个分类
        # 有两种情况：一种是正常的文章（直接解析），另一种是以图片为主的新型文章（通过html拼接得到原始文章的连接，yield回parse_article解析）
        if response.xpath('//div[@class="area article"]/h1/text()').extract():
            article_item = AutohomeArticleItem()
            # 部分文章没有相关车型，要在后台跳过
            if response.xpath('//div[@class="subnav-title-name"]/a/text()').extract():
                article_item['car_name'] = response.xpath('//div[@class="subnav-title-name"]/a/text()').extract()[0]
                article_item['car_link'] = response.xpath('//div[@class="subnav-title-name"]/a/@href').extract()[0]
                article_item['car_type'] = \
                    response.xpath('//div[@class="subnav-title-rank"]/text()').extract()[0].replace(u'关注排名', '')
                article_item['car_type_rank'] = \
                    response.xpath('//div[@class="subnav-title-rank"]/span/text()').extract()[0].strip()
            else:
                article_item['car_name'] = ''
                article_item['car_link'] = ''
                article_item['car_type'] = ''
                article_item['car_type_rank'] = ''
            article_item['article_url'] = response.url
            article_item['article_title'] = \
                response.xpath('//div[@class="area article"]/h1/text()').extract()[0].strip()
            # 文章分类树是多层结构，用正则表达式替换特殊字符'[\r\n|\xa0| ]'
            article_item['article_classify'] = re.sub('[\r\n|\xa0| ]', '', ''.join(
                response.xpath('//div[@class="breadnav fn-left"]//text()').extract()))
            # 标题下面的日期、来源、类型、编辑。如果是新闻稿的话只有article_pub_time和article_type两个key
            if len(response.xpath('//div[@class="article-info"]//span').extract()) == 4:
                article_item['article_pub_time'] = \
                    response.xpath('//div[@class="article-info"]/span[1]/text()').extract()[0].strip()
                # 文章来源可能为空
                article_item['article_from'] = \
                    ''.join(response.xpath('//div[@class="article-info"]/span[2]/a/text()').extract()).strip()
                article_item['article_type'] = \
                    response.xpath('//div[@class="article-info"]/span[3]/text()').extract()[0].replace(u'类型：', '')
                # 前端变化了，先将list,join成一串，然后replace
                article_item['article_writer'] = ''.join(response.xpath('//div[@class="article-info"]/span[4]//text()'
                                                                        ).extract()).strip().replace(u'编辑：', '')
            elif len(response.xpath('//div[@class="article-info"]//span').extract()) == 2:
                article_item['article_pub_time'] = \
                    response.xpath('//div[@class="article-info"]/span[1]/text()').extract()[0].strip()
                article_item['article_type'] = \
                    response.xpath('//div[@class="article-info"]/span[2]/text()').extract()[0].replace(u'类型：', '')
            else:
                logger.warning('`parse_article` function warning: unkown `{}` item.'.format(response.url))
            # 正则替换两个特殊字符u'[\u3000\u3000|\xa0]'，p[not(@align)选择不含某属性的标签
            article_item['article_detail'] = re.sub(u'[\u3000\u3000|\xa0]', '', ''.join(
                response.xpath('//div[@class="article-content"]/p[not(@align)]//text()').extract()))
            article_item['article_photo'] = \
                response.xpath('//div[@class="article-content"]//p[@align="center"]//@src').extract()
            article_item['article_tag'] = response.xpath('//span[@class="tags fn-left"]//a/text()').extract()
            article_item['article_tag_link'] = response.xpath('//span[@class="tags fn-left"]//@href').extract()
            # 评论页面可能为空，为空时赋值为0
            article_item['article_comment_link'] = \
                ''.join(response.xpath('//a[@id="reply-all-btn1"]//@href').extract()).strip()
            # 迭代带有item的Request进一步获得评论数量
            # 正则出文章的序号（可能是897070-15格式），正则要注意点，然后通过urllib解析，得到需要的值
            reply_num_url = self.reply_count_part.format(re.search('/(\d+)[\.|-]', response.url).group(1))
            meta = {'item': article_item}
            yield Request(reply_num_url, meta=meta, callback=self.parse_article_comment_num)
            # 迭代文章评论，formdata提交表单，meta将提交的参数传给respon（评论的api仅支持单页的翻页功能，要将页码传给response做判断翻页操作）
            # response中的url已经是评论api的url了，要传article_url（写入Item），和id（生成翻页的Request）
            formdata = {'page': '1', 'id': re.search('/(\d+)[\.|-]', response.url).group(1), 'appid': '1',
                        'datatype': 'json'}
            meta = {'article_url': response.url, 'page': '1', 'id': re.search('/(\d+)[\.|-]', response.url).group(1)}
            yield FormRequest(self.article_commnet_part, formdata=formdata, meta=meta,
                              callback=self.pase_article_comment)
        else:
            # 通过xpath的正则找原始url的部分，并迭代新的Request
            article_src_url = '{}{}'.format(response.url, response.xpath(
                '//script[@type="text/javascript" and not(@src)]').re('(\?pvareaid=\d+)')[0])
            yield Request(article_src_url, callback=self.parse_article)

    def parse_article_comment_num(self, response):
        """
        获取文章评论数量，是通过js调用api实时获取最新评论数量的。
        接收parse_article传过来的item，增加article_comment_num的field
        调用方式是API地址+返回值类型+文章ID获得的
        :param response: 
        :return: 
        """
        # 从response.meta获取上一个request的item值
        article_item = response.meta['item']
        response_json = json.loads(response.text)
        # returncode == 0表示返回成功
        article_item['article_comment_num'] = \
            response_json['result']['objcounts'][0]['replycountall'] if response_json['returncode'] == 0 else ''
        yield article_item

    def pase_article_comment(self, response):
        """
        传文章id，页面page，通过文章评论api，获得文章的评论
        通过判断评论的有无确定是否继续爬该id的评论，如果不爬就停止，如果爬就page在原基础上+1
        :param response: 
        :return: 
        """
        # response用loads转换成json
        article_commnet = AutohomeCommentItem()
        response_json = json.loads(response.text)
        # 查看dict里面是否有commentlist这个key，以及对应的values是否为空（为空表示最后一页）
        if response_json.has_key('commentlist') and \
                        response_json['commentlist'] != None and response_json['commentlist'] != []:
            article_commnet['article_url'] = response.meta['article_url']
            article_commnet['comment_list'] = response_json['commentlist']
            article_commnet['comment_page'] = response_json['page']
            yield article_commnet

            # 迭代用户页面链接
            for each_comment in article_commnet['comment_list']:
                user_url = self.user_home_part.format(each_comment['RMemberId'])
                yield Request(user_url, callback=self.pase_autohome_user)

            # 迭代下一页的评论
            next_comment_page = str(int(response.meta['page']) + 1)
            formdata = {'page': next_comment_page, 'id': response.meta['id'], 'appid': '1', 'datatype': 'json'}
            meta = {'article_url': response.meta['article_url'], 'page': next_comment_page, 'id': response.meta['id']}
            yield FormRequest(self.article_commnet_part, formdata=formdata, meta=meta,
                              callback=self.pase_article_comment)
        else:
            logger.debug(('`pase_article_comment` function debug:'
                          '{} api post data {} has empty commentlist.').format(response.url, str(response.meta)))

    def pase_autohome_user(self, response):
        """
        接收pase_article_comment传递的Request,获取用户的基本信息,并将item传给pase_user_activity函数获取用户活跃度
        :param response: 
        :return: 
        """
        user_id = response.url.split('/')[-1]
        user_info = AutohomeUserItem()

        user_info['user_id'] = user_id
        # user_name 可能为空
        user_info['user_name'] = ''.join(response.xpath('//h1[@class="user-name"]/b/text()').extract()).strip()
        user_info['user_img'] = response.xpath('//div[@class="userHead"]/a/img/@src').extract()[0]
        # 是否绑定手机可能为空
        user_info['tie_phone'] = ''.join(response.xpath('//a[@class="iphone"]/@data-title').extract()).strip()
        user_info['following_num'] = response.xpath('//a[@class="state-mes"]/span/text()').extract()[0]
        user_info['followers_num'] = response.xpath('//a[@class="state-mes"]/span/text()').extract()[1]
        user_info['user_location'] = response.xpath('//a[@class="state-pos"]/text()').extract()[0]
        user_info['user_sex'] = response.xpath('//h1[@class="user-name"]/span/@class').extract()[0]
        # 构造用户活跃度url和用户车库url
        # 解析ajax -- 帮助值、精华帖、主帖等
        # 通过meta将item、header传给callback函数，进行下一步解析
        user_activity_url = self.user_activity_part.format(user_id, random.random(),
                                                           ('%.3f' % time.time()).replace('.', ''))
        meta = {'item': user_info}
        yield Request(user_activity_url, meta=meta, callback=self.pase_user_activity)
        # user_info['topics_link'] = 
        # user_info['reply_forum_link'] = 

    def pase_user_activity(self, response):
        """
        接收pase_autohome_user传递的mata，调用ajax接口为itme增加用户活跃度信息，并将增加后的item交给pase_user_carbarn获取用户车库
        ajax接口返回的是json字符串
        :param response: 
        :return: 
        """
        user_info_headers = {
            'Host': 'i.autohome.com.cn',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': self.user_home_part.format(re.search('userid=(.*?)&', response.url).group(1))
        }
        # 从response.meta中提取数据
        user_info = response.meta['item']

        # 从response中提取item用户活跃度的values
        response_json = json.loads(response.text)
        # create_time = response_json['UserGrade']['CreateTime']
        user_info['last_edit_time'] = response_json['UserGrade']['LastEditTime']
        user_info['help_score'] = response_json['HelpScore']
        user_info['jh_topic_count'] = response_json['JHTopicCount']
        user_info['topics_count'] = response_json['TopicCount']

        # 组装meta，将新的item传给pase_user_carbarn增加用户车库
        user_carbarn_url = self.user_carbarn_part.format(random.random(), user_info['user_id'])
        meta = {'item': user_info}
        yield Request(user_carbarn_url, meta=meta, headers=user_info_headers, callback=self.pase_user_carbarn)

    def pase_user_carbarn(self, response):
        """
        接收pase_user_activity传递的mata，调用ajax接口为itme增加用户关注车库，并将增加后的item交给pase_user_following获取用户关注名单
        ajax接口(api)返回的是json字符串
        :param response: 
        :return: 
        """
        # 从response.meta中提取数据
        user_info = response.meta['item']

        # 从response中提取item中用户关注车库
        response_json = json.loads(response.text)
        user_info['concern_car_count'] = response_json['ConcernCount']
        user_info['concern_carbarn'] = response_json['ConcernInfoList']

        # 组装meta和user_following_url，生成用户关注request
        user_following_url = self.user_following_part.format(user_info['user_id'], '1')
        following_list = []
        meta = {'following_list': following_list, 'page': '1', 'item': user_info}
        yield Request(user_following_url, meta=meta, callback=self.pase_user_following)

    def pase_user_following(self, response):
        """
        接收pase_user_carbarn传递的mata，调用ajax接口为itme增加用户关注名单，并将增加后的item交给pase_user_followers获取用户粉丝名单
        :param response: 
        :return: 
        """
        # 从response.meta中提取数据
        user_info = response.meta['item']
        following_num = int(user_info['following_num'])
        following_list = response.meta['following_list']

        # 更新meta内容，实现关注人员的翻页操作
        following_list.extend(response.xpath('//ul[@class="duList2"]//li/@id').extract())

        # 判断当前页面是最后一页（页面数=ceil(关注人数/每页最多人数（20）) if following_num != 0 else following_num）
        if int(response.meta['page']) == (int(math.ceil(float(following_num) / 20))) or following_num == 0:
            # 最后一页的following_list就是用户当前关注的所有人
            user_info['user_following'] = response.meta['following_list']

            # 组装meta和user_followers_url，生成用户粉丝request
            user_followers_url = self.user_followers_part.format(user_info['user_id'], 1)
            followers_list = []
            meta = {'followers_list': followers_list, 'page': '1', 'item': user_info}
            yield Request(user_followers_url, meta=meta, callback=self.pase_user_followers)
        else:
            # 不是最后一页时爬取page+1页内容
            user_following_url = self.user_following_part.format(user_info['user_id'], int(response.meta['page']) + 1)
            meta = {'following_list': following_list, 'page': str(int(response.meta['page']) + 1), 'item': user_info}
            yield Request(user_following_url, meta=meta, callback=self.pase_user_following)

    def pase_user_followers(self, response):
        """
        接收pase_user_following传递的mata，调用ajax接口为itme增加用户粉丝名单，并将增加后的item交给item pepiline处理
        """
        # 从response.meta中提取数据
        user_info = response.meta['item']
        followers_num = int(user_info['followers_num'])
        followers_list = response.meta['followers_list']

        # 更新meta内容，实现粉丝人员的翻页操作
        followers_list.extend(response.xpath('//ul[@class="duList2"]//li/@id').extract())

        # 判断当前页面是最后一页（页面数=ceil(粉丝人数/每页最多人数（20）) if following_num != 0 else following_num）
        if int(response.meta['page']) == (int(math.ceil(float(followers_num) / 20))) or followers_num == 0:
            # 最后一页的followers_list就是用户当前关注的所有人
            user_info['user_followers'] = response.meta['followers_list']
            yield user_info

        else:
            # 不是最后一页时爬取page+1页内容
            user_followers_url = self.user_followers_part.format(user_info['user_id'], int(response.meta['page']) + 1)
            meta = {'followers_list': followers_list, 'page': str(int(response.meta['page']) + 1), 'item': user_info}
            yield Request(user_followers_url, meta=meta, callback=self.pase_user_followers)
