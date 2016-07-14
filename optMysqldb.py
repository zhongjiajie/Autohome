#! /usr/bin/python 
# -*- coding:utf8 -*-
#======================#
#---脚本名：optMysqldb.py
#---作者：zhongjiajie
#---日期：2016/03/20
#---功能：MySQL数据库一系列操作
#======================#

#===导入模块===#
#---原模块---#
#---第三方---#
import MySQLdb
#---自定义---#
import writeLog

#===连接数据库===#
def conToMysql():
    try:
        #打开数据库连接
        global conn
        conn = MySQLdb.connect(host='localhost',user='root',passwd='mysql',port=3306,use_unicode=True, charset='utf8')
        #使用cursor()方法获取操作游标
        global cur
        cur = conn.cursor()
    except MySQLdb.Error,e:
        writeLog.writeErrorLog('fail optMysqldb conToMysql Mysql Error %d: %s'%(e.args[0],e.args[1]),'autohome')#写入总日志文件
        writeLog.writeErrorLog('fail optMysqldb conToMysql Mysql Error %d: %s'%(e.args[0],e.args[1]),'autohome_error')#写入错误日志文
    return 0

def closeMysql():
    try:
        conn.commit()     #提交事务
        cur.close()       #关闭游标
        conn.close()      #关闭连接
    except MySQLdb.Error,e:
        writeLog.writeErrorLog('fail optMysqldb closeMysql Mysql Error %d: %s'%(e.args[0],e.args[1]),'autohome')#写入总日志文件
        writeLog.writeErrorLog('fail optMysqldb closeMysql Mysql Error %d: %s'%(e.args[0],e.args[1]),'autohome_error')#写入错误日志文
    return 0

#===删除数据库===#
def dropDatabase(databaseName):
    try:
        conToMysql()
        cur.execute('DROP DATABASE IF EXISTS autohome')
        closeMysql()
    except MySQLdb.Error,e:
        writeLog.writeErrorLog('fail optMysqldb dropDatabase Mysql Error %d: %s'%(e.args[0],e.args[1]),'autohome')#写入总日志文件
        writeLog.writeErrorLog('fail optMysqldb dropDatabase Mysql Error %d: %s'%(e.args[0],e.args[1]),'autohome_error')#写入错误日志文
    return 0

#===从数据库中取值===#
def getValues(database,table,field):
    try:
        conToMysql()

        conn.select_db(database)
        #生成mysql语句
        m_str_selectSql = 'SELECT %s FROM %s'%(field,table)
        m_str_allValue = cur.execute(m_str_selectSql)
        m_str_getAllVal = cur.fetchmany(m_str_allValue)

        closeMysql()
        return m_str_getAllVal
    except MySQLdb.Error,e:
        writeLog.writeErrorLog('fail optMysqldb getValues Mysql Error %d: %s'%(e.args[0],e.args[1]),'autohome')#写入总日志文件
        writeLog.writeErrorLog('fail optMysqldb getValues Mysql Error %d: %s'%(e.args[0],e.args[1]),'autohome_error')#写入错误日志文

#===连接MySQL 写入autohome所有页面的URL page_URL===#
def insertPageUrl(pageUrl):
    try:
        conToMysql()

        #---创建autohome 创建表结构---#
        #使用execute方法执行SQL语句
        cur.execute('CREATE DATABASE IF NOT EXISTS autohome')
        conn.select_db('autohome')
        cur.execute('CREATE TABLE IF NOT EXISTS autohome_page_url('
                    'page_url VARCHAR(100) PRIMARY KEY COMMENT"汽车之家页面url",'
                    'insert_time DATETIME COMMENT"插入时间",'
                    'change_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT"更新时间"'
                    ')COMMENT"页面url"')
        cur.execute('INSERT INTO autohome_page_url VALUES(%s,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)',pageUrl)

        closeMysql()
    except MySQLdb.Error,e:
        writeLog.writeErrorLog('fail optMysqldb insertPageUrl Mysql Error %d: %s'%(e.args[0],e.args[1]),'autohome')#写入总日志文件
        writeLog.writeErrorLog('fail optMysqldb insertPageUrl Mysql Error %d: %s'%(e.args[0],e.args[1]),'autohome_error')#写入错误日志文
    return 0

#===连接MySQL 写入autohome每个页面的所有文章===#
def insertArticleSampleText(articleSampleText):
    try:
        conToMysql()

        cur.execute('CREATE DATABASE IF NOT EXISTS autohome')
        conn.select_db('autohome')
        cur.execute('CREATE TABLE IF NOT EXISTS autohome_sample_text('
                    'article_url VARCHAR(100) PRIMARY KEY COMMENT"文章的url",'
                    'article_cover_url VARCHAR(200) COMMENT"文章封面url",'
                    'article_title VARCHAR(100) COMMENT"文章标题",'
                    'article_viewer_num VARCHAR(20) COMMENT"查看文章人数",'
                    'article_short_text VARCHAR(500) COMMENT"文章简略信息",'
                    'insert_time DATETIME COMMENT"插入时间",'
                    'change_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT"更新时间"'
                    ')COMMENT"文章简述"')

        cur.execute('INSERT INTO autohome_sample_text VALUES('
                    '%s,%s,%s,%s,%s,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)',articleSampleText)

        closeMysql()
    except MySQLdb.Error,e:
        writeLog.writeErrorLog('fail optMysqldb insertArticleSampleText Mysql Error %d: %s'%(e.args[0],e.args[1]),'autohome')#写入总日志文件
        writeLog.writeErrorLog('fail optMysqldb insertArticleSampleText Mysql Error %d: %s'%(e.args[0],e.args[1]),'autohome_error')#写入错误日志文
    return 0

#===写入文章细节部分===#
def insertArticleDetailText(articleDetailText):
    try:
        conToMysql()

        cur.execute('CREATE DATABASE IF NOT EXISTS autohome')
        conn.select_db('autohome')
        cur.execute('CREATE TABLE IF NOT EXISTS autohome_detail_text('
                    'article_url VARCHAR(100) PRIMARY KEY COMMENT"文章url",'
                    'article_classify VARCHAR(30) COMMENT"文章分类",'
                    'article_carClassify VARCHAR(40) COMMENT"文章描述的汽车分类",'
                    'article_title VARCHAR(55) COMMENT"文章标题",'
                    'article_pubTime VARCHAR(25) COMMENT"发布时间",'
                    'article_pubSrcsys VARCHAR(20) COMMENT"发布系统",'
                    'article_pubType VARCHAR(15) COMMENT"发布类型",'
                    'article_pubAuthor VARCHAR(10) COMMENT"文章作者",'
                    'article_detailText MEDIUMTEXT COMMENT"正文",'
                    'article_commentPage VARCHAR(100) COMMENT"评论页面url",'
                    'article_picUrlList MEDIUMTEXT COMMENT"文章图片列表",'
                    'insert_time DATETIME COMMENT"插入时间",'
                    'change_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT"更新时间"'
                    ')COMMENT"文章详情表"')

        cur.execute('INSERT INTO autohome_detail_text VALUES('
                    '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)',articleDetailText)

        closeMysql()
    except MySQLdb.Error,e:
        writeLog.writeErrorLog('fail optMysqldb insertArticleDetailText Mysql Error %d: %s'%(e.args[0],e.args[1]),'autohome')#写入总日志文件
        writeLog.writeErrorLog('fail optMysqldb insertArticleDetailText Mysql Error %d: %s'%(e.args[0],e.args[1]),'autohome_error')#写入错误日志文
    return 0

#===commentDetail===#
def insertCommentDetail(commentDetail):
    try:
        conToMysql()

        cur.execute('CREATE DATABASE IF NOT EXISTS autohome')
        conn.select_db('autohome')
        cur.execute('CREATE TABLE IF NOT EXISTS autohome_comment_detail('
                    'article_url VARCHAR(100) COMMENT"评论文章的url",'
                    'article_title VARCHAR(55) COMMENT"评论文章的标题",'
                    'reply_id VARCHAR(20) PRIMARY KEY COMMENT"该评论在汽车之家的sk",'
                    'repler_homePage VARCHAR(45) COMMENT"评论者的个人主页",'
                    'repler_logo VARCHAR(150) COMMENT"评论者的头像",'
                    'repler_name VARCHAR(35) COMMENT"评论者的名字",'
                    'repler_device VARCHAR(30) COMMENT"评论者所用的设备",'
                    'reply_timeAndFloor VARCHAR(55) COMMENT"评论时间和楼层",'
                    'reply_content TEXT COMMENT"评论发布内容",'
                    'reply_like VARCHAR(20) COMMENT"该评论获得的赞",'
                    'preRepler_logo VARCHAR(150) COMMENT"原评论者的头像",'
                    'preRepler_homePage VARCHAR(45) COMMENT"原评论者的个人主页",'
                    'preRepler_name VARCHAR(35) COMMENT"原评论者的名字",'
                    'preReply_date VARCHAR(25) COMMENT"原评论的日期",'
                    'preReply_floor VARCHAR(15) COMMENT"原评论的楼层",'
                    'preReply_content TEXT COMMENT"原评论的内容",'
                    'insert_time DATETIME COMMENT"插入时间",'
                    'change_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT"更新时间"'
                    ')COMMENT"评论页面表"')

        cur.execute('INSERT INTO autohome_comment_detail VALUES('
                    '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)',commentDetail)

        closeMysql()
    except MySQLdb.Error,e:
        writeLog.writeErrorLog('fail optMysqldb insertCommentDetail Mysql Error %d: %s'%(e.args[0],e.args[1]),'autohome')#写入总日志文件
        writeLog.writeErrorLog('fail optMysqldb insertCommentDetail Mysql Error %d: %s'%(e.args[0],e.args[1]),'autohome_error')#写入错误日志文
    return 0