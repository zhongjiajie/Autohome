#! /usr/bin/python
# -*- coding:utf8 -*-
#======================#
#---脚本名：commentDetail.py
#---作者：zhongjiajie
#---日期：2016/03/20
#---功能：获取评论内容
#======================#

#===导入模块===#
#---原模块---#
import Queue
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

#===从mysql中获取文章url===#
#---返回数组---#
def getArticleUrl(database,table,field):
    try:
        m_ay_fieldValue = []
        #自定义库conToMysql
        m_tup_fieldValue = optMysqldb.getValues(database,table,field)
        for m_str_eachValue in m_tup_fieldValue:
            m_ay_fieldValue.append(m_str_eachValue[0])
        print 'succeed to get url from mysql '
        return m_ay_fieldValue

    except Exception,e:
        print 'fail to get url from mysql ' + ' [%s,%s]'%(Exception,e)
        # writeLog.writeErrorLog('fail commentDetail getArticleUrl %s : %s'%(Exception,e),'autohome')       #写入总日志文件
        # writeLog.writeErrorLog('fail commentDetail getArticleUrl %s : %s'%(Exception,e),'autohome_error') #写入错误日志文件
#===根据数据类型解析url===#
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
        m_soup = BeautifulSoup(m_str_content,'html5lib')
        print 'succeed to download ' + url
        return m_soup

    except Exception,e:
        print 'fail to download ' + url + ' [%s,%s]'%(Exception,e)
        # writeLog.writeErrorLog('fail commentDetail getSoupFromUrl %s : %s'%(Exception,e),'autohome')       #写入总日志文件
        # writeLog.writeErrorLog('fail commentDetail getSoupFromUrl %s : %s'%(Exception,e),'autohome_error') #写入错误日志文件

#===获取所有的评论页面===#
def getCommentPage(firstPageUrl,soup):
    try:
        #存放评论页面
        m_queue_commentPage = Queue.Queue(maxsize=-1)
        m_url_nextPage = firstPageUrl

        while True:
            m_queue_commentPage.put(m_url_nextPage)  #进队
            #获得下一页连接
            m_url_nextPage = soup.find(name='div',attrs={'class':'page page-small'}).find(name='a',attrs={'class':'current'}).next_sibling['href']
            soup = getSoupFromUrl(m_url_nextPage)  #解析url
            #判断是否到达评论最后一页
            if (soup.find(name='div',attrs={'class':'page page-small'}).find(name='a',attrs={'class':'current'}).next_sibling['href'] == 'javascript:void(0);'):
                m_queue_commentPage.put(m_url_nextPage) #最后一页进队
                break
        print 'succeed to get comment page ' + firstPageUrl
        return m_queue_commentPage

    except Exception,e:
        print 'fail to get comment page ' + firstPageUrl + ' [%s,%s]'%(Exception,e)
        writeLog.writeErrorLog('fail commentDetail getCommentPage %s : %s'%(Exception,e),'autohome')       #写入总日志文件
        writeLog.writeErrorLog('fail commentDetail getCommentPage %s : %s'%(Exception,e),'autohome_error') #写入错误日志文件
        return 0

#===评论细节===#
def getCommentDetail(queue):
    while (queue.empty() != True):
        try:
            m_url_eachCommentPage = queue.get()
            #解析评论页面成soup
            m_soup_eachCommentPage = getSoupFromUrl(m_url_eachCommentPage)
            #评论文章url
            m_url_srcArticle = m_soup_eachCommentPage.find(name='h1',attrs={'class':'tit_rev'}).a['href']#.h1.get_text(strip=True)
            #评论文章标题
            m_str_srcArticleTitle = m_soup_eachCommentPage.find(name='h1',attrs={'class':'tit_rev'}).a.string
            #获取评论页面所有的dt标签
            m_list_eachPageDt = m_soup_eachCommentPage.find(name='dl',attrs={'id':'reply-list'}).find_all(name='dt')
            #获取评论页面所有的dd标签
            m_list_eachPageDd = m_soup_eachCommentPage.find(name='dl',attrs={'id':'reply-list'}).find_all(name='dd')
            for number in range(0,len(m_list_eachPageDt)):

                #---dt模块---#
                #回复者的sk
                try:
                    m_str_skReply = m_list_eachPageDt[number].a['name']
                except:
                    m_str_skReply = 'null'
                #回复者的主页
                try:
                    m_url_replerPage = m_list_eachPageDt[number].find(name='a',attrs={'class':'user-fl'})['href']
                except:
                    m_url_replerPage = 'null'
                #回复人头像
                try:
                    m_url_replerLogo = m_list_eachPageDt[number].img['src']
                except:
                    m_url_replerLogo = 'null'
                #回复人昵称
                try:
                    m_str_replerName = m_list_eachPageDt[number].find(name='a',attrs={'class':'user-fl'}).text
                except:
                    m_str_replerName = 'null'
                #通过什么设备回复
                try:
                    m_str_replerDevice = m_list_eachPageDt[number].find(name='a',attrs={'class':'revgrey'}).text
                except:
                    m_str_replerDevice = 'null'
                #几分钟前，楼层数
                try:
                    m_str_replerTimeAndFloor = m_list_eachPageDt[number].find(name='span',attrs={'class':'fn-right'}).text
                except:
                    m_str_replerTimeAndFloor = 'null'

                #---dd模块---#
                #当前用户回复内容
                try:
                    m_str_replyContent = m_list_eachPageDd[number].p.text
                except:
                    m_str_replyContent = 'null'
                # 当前用户获得赞的数量
                try:
                    m_n_likeNum = m_list_eachPageDd[number].find(name='div',attrs={'class':'text-right'}).find(name='a',attrs={'target':'_self'}).text
                except:
                    m_n_likeNum = 'null'
                #--当前用户回复以往用户 以往用户的个人信息--#
                #原评论部分
                try:
                    m_str_preReplyPart = m_list_eachPageDd[number].find(name='div',attrs={'class':'reply'})
                except:
                    m_str_preReplyPart = 'null'
                #原评论用户头像
                try:
                    m_url_preReplerLogo = m_str_preReplyPart.img['src']
                except:
                    m_url_preReplerLogo = 'null'
                #原评论用户主页
                try:
                    m_url_preReplerPage = m_str_preReplyPart.find(name='a',attrs={'class':'grey666'})['href']
                except:
                    m_url_preReplerPage = 'null'
                #原评论用户昵称
                try:
                    m_str_preReplerName = m_str_preReplyPart.find(name='a',attrs={'class':'grey666'}).text
                except:
                    m_str_preReplerName = 'null'
                #原评论用户回复日期
                try:
                    m_str_preReplyDate = m_str_preReplyPart.find(name='span',attrs={'class':'grey'},text='于').next_sibling
                except:
                    m_str_preReplyDate = 'null'
                #原评论评论所在楼数
                try:
                    m_n_preReplyFloor = m_str_preReplyPart.find(name='span',attrs={'class':'grey666'}).text
                except:
                    m_n_preReplyFloor = 'null'
                #原评论的回复
                try:
                    m_str_preReplyContent = m_str_preReplyPart.find(name='p',attrs={'class':'reply-name'}).next_sibling.text
                except:
                    m_str_preReplyContent = 'null'

                #---返回顺序：评论文章url,评论文章标题,回复者的sk，回复者的主页，回复人头像，回复人昵称，通过什么设备回复，几分钟前楼层数，
                # 当前用户回复内容，当前用户获得赞的数量,原评论用户头像，原评论用户回复日期，原评论评论所在楼数，原评论的回复
                m_str_CommentConnent = (m_url_srcArticle,m_str_srcArticleTitle,m_str_skReply,m_url_replerPage,m_url_replerLogo,
                                      m_str_replerName,m_str_replerDevice,m_str_replerTimeAndFloor,m_str_replyContent,m_n_likeNum,
                                      m_url_preReplerLogo,m_url_preReplerPage,m_str_preReplerName,m_str_preReplyDate,
                                      m_n_preReplyFloor,m_str_preReplyContent)
                optMysqldb.insertCommentDetail(m_str_CommentConnent)
                writeLog.writerNormalLog('succeed get comment skReplay %s' %m_str_skReply,'autohome')
            print 'succeed to get comment detail ' + m_url_eachCommentPage
        except Exception,e:
            print 'fail to get comment page ' + m_url_srcArticle + ' [%s,%s]'%(Exception,e)
            writeLog.writeErrorLog('fail commentDetail getCommentDetail %s : %s'%(Exception,e),'autohome')       #写入总日志文件
            writeLog.writeErrorLog('fail commentDetail getCommentDetail %s : %s'%(Exception,e),'autohome_error') #写入错误日志文件
    return 0