#! /usr/bin/python 
# -*- coding:utf8 -*-
#==============================#
#---脚本名：allUrlAndShort.py
#---作者：zhongjiajie
#---日期：2016/03/20
#---功能：获取汽车之家页面链接、简要文章链接
#==============================#

#===导入模块===#
#---原模块---#
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

#===获取autohome所有页面的URL 写入temp_URL_List===#
def getUrlAndShort():
    #---变量声明---#
    s_n_isloop = 0    #0循环 1退出
    m_str_tempPage = '/all/2/#liststart'    #开始页面

    #===获取autohome所有页面链接 文章简介===#
    #---所有页面链接 m_str_tempUrlList---#
    #---所有文章简介 m_str_articleSampleText---#
    #删除已存在的数据库
    optMysqldb.dropDatabase('autohome')
    while (s_n_isloop == 0):
        try:
            #拼接网页连接  放进数组
            m_str_tempPageUrl = "http://www.autohome.com.cn%s"%m_str_tempPage
            #---m_str_tempUrlList导入Mysql的autohome_page_url表---#
            optMysqldb.insertPageUrl(m_str_tempPageUrl)
            writeLog.writerNormalLog('succeed get page url %s' % m_str_tempPageUrl, 'autohome')

            #获取网页源代码  用bs4解析
            params = {'Accept':'*/*',
                      'Accept-Encoding':'gzip, deflate, sdch',
                      'Accept-Language':'zh-CN,zh;q=0.8',
                      'Cache-Control':'no-cache',
                      'Connection':'keep-alive',
                      'Host':'www.autohome.com.cn',
                      'Pragma':'no-cache',
                      'User-Agent':changeUA.getUA()
                      }
            m_str_tempContent = requests.get(m_str_tempPageUrl,params=params,timeout=30).content
            m_str_tempSoup = BeautifulSoup(m_str_tempContent,"html5lib")
            #获取下一个页面的连接  用bs4的下一个兄弟节点的方法
            m_str_tempPage = m_str_tempSoup.find(name='div',attrs={'id':'channelPage'}).find(name='a',attrs='current').next_sibling['href']

            #获取文章的标题等信息（简略）
            m_str_articleHtml = m_str_tempSoup.find(id="auto-channel-lazyload-article").find_all(name='li')
            for m_n_rankOfList in range(len(m_str_articleHtml)):
                m_str_part_1 = m_str_articleHtml[m_n_rankOfList].a["href"]                 #文章连接 article_url
                m_str_part_2 = m_str_articleHtml[m_n_rankOfList].div.img["src"].strip()    #图片地址 article_cover_url
                m_str_part_3 = m_str_articleHtml[m_n_rankOfList].h3.string                 #文章标题 article_title
                m_str_part_4 = m_str_articleHtml[m_n_rankOfList].em.contents[1].strip()    #阅读数 article_viewer
                m_str_part_5 = m_str_articleHtml[m_n_rankOfList].p.string                  #文章征文部分
                m_str_articleSampleText = (m_str_part_1,m_str_part_2,m_str_part_3,m_str_part_4,m_str_part_5)

                #---m_str_articleSampleText导入Mysql的autohome_sample_text表---#
                optMysqldb.insertArticleSampleText(m_str_articleSampleText)
                writeLog.writerNormalLog('succeed get article%s,%s' % (m_str_part_1, m_str_part_3), 'autohome')
        except Exception,e:
            s_n_isloop = 1
            writeLog.writeErrorLog('fail allUrlAndShort getUrlAndShort %s : %s'%(Exception, e),'autohome')       #写入总日志文件
            writeLog.writeErrorLog('fail allUrlAndShort getUrlAndShort %s : %s'%(Exception, e),'autohome_error') #写入错误日志文件