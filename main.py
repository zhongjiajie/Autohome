# -*- coding:utf8 -*-
#!/usr/bin/python

#-----引入模块-----#
#---原模块---#
import sys
#---自定义---#
import allUrlAndShort
import detailText
import commentDetail
import writeLog
import optMysqldb

#-----设置全局UTF-8格式-----#
reload(sys)
sys.setdefaultencoding( "utf-8" )


# try:
    #-----获取autohome所有url和简介-----#
    # allUrlAndShort.getUrlAndShort()

    #-----获取autohome文章的详细信息-----#
    # m_list_articleUrl = detailText.getArticleUrl('autohome','autohome_sample_text','article_url')
    # for str_eachArticleUrl in m_list_articleUrl:
    #     m_str_soup = detailText.getSoupFromUrl(str_eachArticleUrl)
    #     m_str_detailText = detailText.getArticleDetail(str_eachArticleUrl, m_str_soup)
    #     optMysqldb.insertArticleDetailText(m_str_detailText)

    #-----获取autohome评论详情-----#
m_list_articleCommentPage = commentDetail.getArticleUrl('autohome','autohome_detail_text','article_commentPage')
for m_str_articleCommentPage in m_list_articleCommentPage:
    try:
        m_str_soup = commentDetail.getSoupFromUrl(m_str_articleCommentPage)
        m_queue_commentPage = commentDetail.getCommentPage(m_str_articleCommentPage, m_str_soup)
        commentDetail.getCommentDetail(m_queue_commentPage)
    except Exception,e:
        writeLog.writeErrorLog('fail main %s : %s'%(Exception,e),'autohome')       #写入总日志文件
        writeLog.writeErrorLog('fail main %s : %s'%(Exception,e),'autohome_error') #写入错误日志文件
        continue
# except Exception,e:
#     writeLog.writeErrorLog('fail main %s : %s'%(Exception,e),'autohome')       #写入总日志文件
#     writeLog.writeErrorLog('fail main %s : %s'%(Exception,e),'autohome_error') #写入错误日志文件