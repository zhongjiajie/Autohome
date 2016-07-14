#! /usr/bin/python
# -*- coding:utf8 -*-
#======================#
#---脚本名：detailText.py
#---作者：zhongjiajie
#---日期：2016/03/20
#---功能：获取汽车之家文章细节
#======================#

#===导入模块===#
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

#===设置全局编码为utf8===#
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