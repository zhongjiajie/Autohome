#!/usr/bin/python
# -*- coding:utf8 -*-
#---
#---
#---

#-----导入模块-----#
#---原模块---#
import re
import sys
#---第三方---#
import requests
from bs4 import BeautifulSoup
#---自定义---#
import optMysqldb
import writeLog
import changeUA

#-----设置全局编码为utf8-----#
reload(sys)
sys.setdefaultencoding('utf-8')

#---从mysql中获取文章url---#
#--返回数组--#
def getArticleUrl(database,table,field):
    try:
        m_ay_fieldValue = []
        #自定义库conToMysql
        m_tup_fieldValue = optMysqldb.getValues(database, table, field)
        for m_str_eachValue in m_tup_fieldValue:
            m_ay_fieldValue.append(m_str_eachValue[0])
        return m_ay_fieldValue
    except Exception,e:
        writeLog.writeErrorLog('fail detailText getArticleUrl %s : %s' %(Exception,e),'autohome')
        writeLog.writeErrorLog('fail detailText getArticleUrl %s : %s' %(Exception,e),'autohome_error')

#---根据数据类型解析url---#
#--返回格式化soup--#
def getSoupFromUrl(url):
    params = {'Accept':'*/*',
              'Accept-Encoding':'gzip, deflate, sdch',
              'Accept-Language':'zh-CN,zh;q=0.8',
              'Cache-Control':'no-cache',
              'Connection':'keep-alive',
              'Host':'www.autohome.com.cn',
              'Pragma':'no-cache',
              'User-Agent':changeUA.getUA()
              }
    try:
        m_str_content = requests.get(url,params=params,timeout=30).content
        m_soup = BeautifulSoup(m_str_content,"html5lib")
        #判断正文是否有翻页，并解决
        if (m_soup.find(name='div',attrs={'class':'page'})):
            #正则表达式解决方案
            if (re.search('-',url)):                        #判断是否有'-'，有是第一页，没有不是第一页
                m_str_url = re.sub('-.*\.','-all.',url)     #有的替换方式
            else:
                m_str_url = re.sub('\.html','-all.html',url)#没有的替换方式
            m_str_content = requests.get(m_str_url,params=params,timeout=30).content
            m_soup = BeautifulSoup(m_str_content,"html5lib")
        return m_soup
    except Exception,e:
        writeLog.writeErrorLog('fail detailText getSoupFromUrl %s : %s' %(Exception,e),'autohome')
        writeLog.writeErrorLog('fail detailText getSoupFromUrl %s : %s' %(Exception,e),'autohome_error')

#---获取正文页面内容---#
#如果有对应的值，就赋值。没有对应的值，就赋值为null
def getArticleDetail(srcUrl,soup):
    try:
        global m_str_returnContent
        #--附加信息--#
        #文章所属分类
        try:
            m_str_articleClassify = soup.find(name='div',attrs={'class':'breadnav fn-left'}).get_text(strip=True)[0:-12]
        except:
            m_str_articleClassify = 'null'
        #所属车系
        try:
            m_str_articleCarClassify = soup.find(name='div',attrs={'class':'subnav-title-name'}).get_text(strip=True)
        except:
            m_str_articleCarClassify = 'null'
        #文章标题
        try:
            m_str_articleTitle = soup.find(name='div',attrs={'class':'area article'}).h1.get_text(strip=True)
        except:
            m_str_articleTitle = 'null'

        #---发布详情---#
        #时间
        try:
            m_str_articlePubInfo = [text for text in soup.find(name='div',attrs={'class':'article-info'}).stripped_strings]
            m_str_articlePubTime = m_str_articlePubInfo[0]
        except:
            m_str_articlePubTime = 'null'
        #来源
        try:
            m_str_articlePubSrcsys = m_str_articlePubInfo[2]
        except:
            m_str_articlePubSrcsys = 'null'
        #类型
        try:
            m_str_articlePubType = m_str_articlePubInfo[3]
        except:
            m_str_articlePubType = 'null'
        #作者
        try:
            m_str_articlePubAuthor = m_str_articlePubInfo[5]
        except:
            m_str_articlePubAuthor = 'null'

        #---正文---#
        #粗略版  要删减
        try:
            m_str_articleDetail = soup.find(name='div',attrs={'class':'article-content'}).get_text(strip=True)
        except:
            m_str_articleDetail = 'null'

        #---正文的图片---#
        #list以|P|为分隔符，以picStart开始，以picEnd结束
        try:
            target = soup.find(name='div',attrs={'class':'area article'}).find_all(name='img')
            m_list_pictureUrl = 'picStart'
            for i in range(0,len(target)):
                m_list_pictureUrl = m_list_pictureUrl + '|P|' + target[i]['src']
            m_list_pictureUrl = m_list_pictureUrl + '|P|' + 'picEnd'
        except:
            m_list_pictureUrl = 'null'
        try:

        #--评论页面--#
            m_str_articleCommentPage = soup.find(name='a',attrs={'id':'reply-all-btn1'})['href']#.href#.get_text(strip=True)
        except:
            m_str_articleCommentPage = 'null'

        #--返回顺序：文章分类，文章车系，文章标题，时间，来源，类型，作者，正文，评论页面,图片字符串--#
        m_str_returnContent = (srcUrl,m_str_articleClassify,m_str_articleCarClassify,m_str_articleTitle,m_str_articlePubTime,
                                m_str_articlePubSrcsys,m_str_articlePubType,m_str_articlePubAuthor,m_str_articleDetail,
                                m_str_articleCommentPage,m_list_pictureUrl)
        writeLog.writerNormalLog('succeed get article %s detail' % srcUrl, 'autohome')
        return m_str_returnContent
    except Exception,e:
        writeLog.writeErrorLog('fail detailText getArticleDetail %s : %s' %(Exception,e),'autohome')
        writeLog.writeErrorLog('fail detailText getArticleDetail %s : %s' %(Exception,e),'autohome_error')


#########################################################################################
# m_list_articleUrl = getArticleUrl('autohome','autohome_sample_text','article_url')
# for str_eachArticleUrl in m_list_articleUrl:
#     m_str_soup = getSoupFromUrl(str_eachArticleUrl)
#     m_str_detailText = getArticleDetail(str_eachArticleUrl,m_str_soup)
#     optMysqldb.insertArticleDetailText(m_str_detailText)
###########################################################################################
    #如果输入的是string类型
    # if type(targetUrl) is types.StringType:

    # #如果输入的是list类型
    # if type(targetUrl) is types.ListType:
    #     for m_str_eachUrl in targetUrl:
    #         m_str_content = requests.get(m_str_eachUrl).content
    #         m_html_soup = BeautifulSoup(m_str_content,"html5lib")
    # print m_soup
############################################################################################






#------------------------------------------正文的附加信息---------------------------------------#
# srcUrl = 'http://www.autohome.com.cn/drive/201604/884518-7.html#pvareaid=102624'
# src_Content = requests.get(srcUrl).content
# # print src_Content
# src_Soup = BeautifulSoup(src_Content)
# print src_Soup.original_encoding
# # print src_Soup
# #获取文章所属分类
# print src_Soup.find(name = 'div',attrs={'class':'breadnav fn-left'}).get_text(strip=True)[0:-12]
# print '###'
# #所属车系
# print src_Soup.find(name = 'div',attrs={'class':'subnav-title-name'}).get_text(strip=True)
# print '######'
# #文章标题
# print src_Soup.find(name = 'div',attrs={'class':'area article'}).h1.get_text(strip=True)
# print '#####'
# #文章信息
# info = [text for text in src_Soup.find(name = 'div',attrs={'class':'article-info'}).stripped_strings]
# print info[0]#时间
# print info[2]#来源
# print info[3]#类型
# print info[5]#作者




#--------------------------------------------正文内容---------------------------------------------------#
# #文章内容article-content
# #粗略版  要删减
# print src_Soup.find(name = 'div',attrs={'class':'article-content'}).get_text(strip=True)#.find_all(name='p')[0:-3]
# # str = ','.join(content)
# # print str.get_text(strip=True)




#-------------------------------------单篇文章评论页面------------------------------------------#
# #获取文章评论页面
# print src_Soup.find(name = 'a',attrs={'id':'reply-all-btn1'})['href']#.href#.get_text(strip=True)
# #解析评论文章
# commentUrl = 'http://reply.autohome.com.cn/Articlecomment.aspx?articleid=884518#pvareaid=103217'
# commentContent = requests.get(commentUrl).content
# # print src_Content
# commentSoup = BeautifulSoup(commentContent)
# print commentSoup.original_encoding
# #评论文章url
# print commentSoup.find(name = 'h1',attrs={'class':'tit_rev'}).a['href']#.h1.get_text(strip=True)
# #评论文章标题
# print commentSoup.find(name = 'h1',attrs={'class':'tit_rev'}).a.string
# #评论回复列表




#-------------------------------------单个用户评论-----------------------------------------------#
#-----dt------#
# print commentSoup.find(name = 'dl',attrs={'id':'reply-list'}).dt
# comment = commentSoup.find(name = 'dl',attrs={'id':'reply-list'}).dt#.get_text(strip=True)
# #回复的sk
# print comment.a['name']
# #回复人的主页
# print comment.find(name='a',attrs={'class':'user-fl'})['href']
# #回复人头像
# print comment.img['src']
# #回复人昵称
# print comment.find(name='a',attrs={'class':'user-fl'}).text
# #通过什么设备回复
# print comment.find(name='a',attrs={'class':'revgrey'}).text
# #几分钟前，楼层数
# print comment.find(name='span',attrs={'class':'fn-right'}).text
# -------dd-------#
# 当前用户回复内容
# print commentSoup.find(name = 'dl',attrs={'id':'reply-list'}).dd.p.string
# #当前用户获得赞的数量
# print commentSoup.find(name = 'dl',attrs={'id':'reply-list'}).dd.find(name='div',attrs={'class':'text-right'}).find(name='a',attrs={'target':'_self'}).text




#-----------------------------当前用户回复以往用户 以往用户的个人信息-------------------------------------#
# print commentSoup.find(name = 'dl',attrs={'id':'reply-list'}).dd.find(name='div',attrs={'class':'reply'})
# #原用户头像
# print commentSoup.find(name = 'dl',attrs={'id':'reply-list'}).dd.find(name='div',attrs={'class':'reply'}).img['src']
# #原用户主页
# print commentSoup.find(name = 'dl',attrs={'id':'reply-list'}).dd.find(name='div',attrs={'class':'reply'}).find(name='a',attrs={'class':'grey666'})['href']
# #原用户昵称
# print commentSoup.find(name = 'dl',attrs={'id':'reply-list'}).dd.find(name='div',attrs={'class':'reply'}).find(name='a',attrs={'class':'grey666'}).text
# #原用户回复日期
# print commentSoup.find(name = 'dl',attrs={'id':'reply-list'}).dd.find(name='div',attrs={'class':'reply'}).find(name='span',attrs={'class':'grey'},text='于').next_sibling
# #原评论所在楼数
# print commentSoup.find(name = 'dl',attrs={'id':'reply-list'}).dd.find(name='div',attrs={'class':'reply'}).find(name='span',attrs={'class':'grey666'}).text
# #原评论的回复
# print commentSoup.find(name = 'dl',attrs={'id':'reply-list'}).dd.find(name='div',attrs={'class':'reply'}).find(name='p',attrs={'class':'reply-name'}).next_sibling.text




#----------------------------------------用户资料获取------------------------------------------------#
# userUrl = 'http://i.autohome.com.cn/18382369'
# userContent = requests.get(userUrl).content
# # print src_Content
# userSoup = BeautifulSoup(userContent)
##用户头像
# print userSoup.img['src']
##用户基本信息
# print userSoup.find(name='div',attrs={'class':'user-center'})
##用户名
# print userSoup.find(name='div',attrs={'class':'user-center'}).find(name='h1',attrs={'class':'user-name'}).b.string
# #是否绑定手机
# print userSoup.find(name='div',attrs={'class':'user-center'}).find(name='h1',attrs={'class':'user-name'}).a['data-title']
# #男女
# print userSoup.find(name='div',attrs={'class':'user-center'}).find(name='h1',attrs={'class':'user-name'}).span['class'][0]
# #用户等级  ！！！！！隐藏了！！！！！
# print userSoup.find(name='div',attrs={'class':'user-center'}).find(name='div',attrs={'class':'user-lv'}).find(name='span',attrs={'class':'lv-txt'}).string
# #关注
# print userSoup.find(name='div',attrs={'class':'user-center'}).find(name='a',attrs={'class':'state-mes'}).span.text
#粉丝
# print userSoup.find(name='div',attrs={'class':'user-center'}).find_all(name='a',attrs={'class':'state-mes'})[1].span.text
#用户车库信息
# print userSoup.find(name='div',attrs={'class':'center-content'}).find(name='div',attrs='carport-title').a['href']


# #最关注的车型
# userUrl = 'http://i.autohome.com.cn/18382369/car#pvareaid=104341'
# userContent = requests.get(userUrl).content
# # print src_Content
# userSoup = BeautifulSoup(userContent)
#
# print userSoup.find_all(name='div',attrs={'class':'fcpc'}).strong.text