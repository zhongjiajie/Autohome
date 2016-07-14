#Python_car
这是一个Python的爬虫和数据分析程序，目的是通过爬取汽车之家的数据进行分析。
通过汽车之家的数据分析当今的汽车市场情况，并通过多年的数据预测汽车市场的走势。

*[当前进度]
2016/04/20    已经完成了爬虫程序的编写，并于同月25号完成了数据的爬取，合计14G数据，准备进行下一步的分析工作

*[文件结构图]
>Python_car
>>allUrlAndShort.py
>>changeUA.py
>>commentDetail.py
>>detailText.py
>>optMysqldb.py
>>writeLog.py
>>main.py
>>readme.md

*[各文件功能简介]     
  *allUrlAndShort.py  : 获取汽车之家页面链接、简要文章链接
  *changeUA.py          : 随机选择UA进行反爬虫
  *commentDetail.py : 获取评论内容
  *detailText.py           : 获取汽车之家文章细节
  *optMysqldb.py       : MySQL数据库一系列操作
  *writeLog.py             : 对操作过程写日志
  *main.py                    : 主程序入口
  *readme.md             : readme文档