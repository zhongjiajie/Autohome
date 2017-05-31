# Autohome
[Autohome](https://github.com/zhongjiajie/Autohome)使用了[Scrapy](https://github.com/scrapy/scrapy)爬虫框架,实现对[汽车之家-文章](http://www.autohome.com.cn/all/)进行定向爬虫，并将抓取的数据存放进[MongoDB](https://github.com/mongodb/mongo)中。后期将对抓取数据进行简单的分析以及NLP的工作。

## 运行环境
Python 2.7.10
Scrapy 1.3.2
MonogDB 3.2.10






## TODO
* 优化模拟登陆的抓取速度 及完整度

## Change Log


## 当前进度
* [ 2016/04 ] 已经完成了爬虫程序的编写，并于同月25号完成了数据的爬取，合计**14G数据**，准备进行下一步的分析工作
* [ 2016/05 ] 正在MySQL进行简单的**统计分析**，*得出文章编辑活跃度排名*、*用户活跃度排名*、*用户活跃时间*

## 文件结构图
* Python_car<br> 
  * allUrlAndShort.py<br>
  * changeUA.py<br> 
  * commentDetail.py<br> 
  * detailText.py<br> 
  * optMysqldb.py<br> 
  * writeLog.py<br> 
  * main.py<br> 
  * readme.md<br> 

## 各文件功能简介    
* `allUrlAndShort.py`: 获取汽车之家页面链接、简要文章链接
* `changeUA.py`          : 随机选择UA进行反爬虫
* `commentDetail.py` : 获取评论内容
* `detailText.py`           : 获取汽车之家文章细节
* `optMysqldb.py`       : MySQL数据库一系列操作
* `writeLog.py`             : 对操作过程写日志
* `main.py`                    : 主程序入口
* `readme.md`             : readme文档
