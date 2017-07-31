# Autohome
[Autohome](https://github.com/zhongjiajie/Autohome)基于[Scrapy](https://github.com/scrapy/scrapy)爬虫框架,实现对[汽车之家-文章](http://www.autohome.com.cn/all/)进行定向爬虫，并将抓取的数据存放进[MongoDB](https://github.com/mongodb/mongo)中。后期将对抓取数据进行简单的分析以及NLP的工作。

* 说明：了解最新版本移步到[Autohome dev](https://github.com/zhongjiajie/Autohome/tree/dev)

## 运行环境
* Python 2.7.10
* MonogDB 3.2.10
* Scrapy 1.3.2
* pymongo 3.4.0

## 项目构成
```
│  readme.md
│  requirements.txt
│  
├─Analysis
│      config.py
│      sep_word.py
│      statistics.py
│      user_dict.txt
│      
├─AutohomeSpider
│  │  scrapy.cfg
│  │  
│  └─AutohomeSpider
│      │  downloader_middleware.py
│      │  items.py
│      │  pipelines.py
│      │  settings.py
│      │  __init__.py
│      │  
│      └─spiders
│              autohome_spider.py
│              __init__.py
│              
├─GetUserAgent
│  │  scrapy.cfg
│  │  
│  └─GetUserAgent
│      │  items.py
│      │  middlewares.py
│      │  pipelines.py
│      │  settings.py
│      │  __init__.py
│      │  
│      └─spiders
│              useragent_spider.py
│              __init__.py
│              
├─IPProxyPool
│          
└─support_file
```
* **AutohomeSpider**： Autohome项目爬虫主程序程序
* **Analysis**: Autohome项目简单分析模块
* **GetUserAgent**: Autohome项目获取`user agent`的爬虫模块
* **IPProxyPool**: Autohome项目获取开源IP代理，此处感谢@qiyeboy
* **support_file**： Autohome的支撑文件夹，只要存放说明相片以及原visio格式
* **requirements.txt**： Autohome项目依赖
* **readme.md**: Autohome项目readme

## 使用方式
* 安装[Pyhton](https://www.python.org/getit/)以及[MongoDB](https://www.mongodb.com/download-center)
* [启动MongoDB](http://blog.csdn.net/liusong0605/article/details/10574863)
* 安装Autohome相关依赖。将cmd切换到Autohome根目录，运行
```shell
pip install -r requirements.txt
```
可能会提示*pip不是内部或外部命令，也不是可运行的程序或批处理文件。*，请点[这里](http://blog.csdn.net/xueli1991/article/details/51914914)解决相应问题
* 根据需要选择数据下载的方式，默认同时下载到MongoDB和本地Json文件中，可以通过修改[Autohome/autohome/settings.py](https://github.com/zhongjiajie/Autohome/blob/master/autohome/settings.py#L88-89)中ITEM_PIPELINES进行选择（两个同时写入可能会导致磁盘I/O过高）,dev branch中默认储存为MongoDB，因为user agent和代理池都是在MongoDB中
* 在GetUserAgent目录下运行
```shell
scrapy crawl user_agent
```
获取主要浏览器的user agent，并储存到MonogDB中
* 在IPProxyPool目录下运行
```shell
python IPProxy.py
```
获取主要开源IP代理，并储存到MonogDB中
* 在AutohomeSpider目录下运行
```shell
scrapy crawl autohome_article
```
运行项目爬虫主程序，并储存到MonogDB中

## 设计概览
### 爬虫设计概览
* Autohome抓取的是[汽车之家-文章](http://www.autohome.com.cn/all/)页面，整个爬虫部分分成四大主题，分别是：文章简介、文章详情、文章评论、评论文章的用户。爬虫的根节点其中四个部分的逻辑如下：
![image](https://github.com/zhongjiajie/Autohome/raw/master/support_file/four_theme/autohome_four_theme.png)

* Autohome基于[Scrapy](https://github.com/scrapy/scrapy)爬虫框架，对四大主题进行抓取，整个流程图如下，其中绿色部分是Scrapy原生框架的逻辑，蓝色部分是[汽车之家-文章](http://www.autohome.com.cn/all/)的爬虫逻辑
![image](https://github.com/zhongjiajie/Autohome/raw/master/support_file/architecture/autohome_architecture.png)

## Features
* 全部基于Scrapy框架实现
* 定义两个Pipeline操作，分别是`AutohomeJsonPipeline`，即本地json文件；以及`AutohomeMongodbPipeline`，即存进MongoDB。可以在`setting.py`的`ITEM_PIPELINES`节点中设置启动的Pipeline
* 定义`RotateUserAgentMiddleware`实现随机的user agent操作，其中所有的User Agent的获取都是在[User Agent String.Com](http://www.useragentstring.com/)中获取的，项目默认是获取Chrome、ChromePlus、Firefox、Safari四个浏览器的UA
* 定义`RotateProxyMiddleware`实现随机代理操作，代理使用了
* `Analysis`用于对爬虫数据进行分析

## TODO
* 优化模拟登陆的抓取速度及完整度
* 对抓取的结构化数据进行分析
* 对抓取的非结构化数据分析

## Change Log
* 20170531 将原来自定义模块的爬虫程序切换到Scrapy爬虫框架
* 20170725 调整了项目架构，原爬虫文件夹`autohome`更名为`AutohomeSpider`,新增`IPProxyPool`开源代理池，新增`Analysis`分析模块，新增`GetUserAgent`user agent爬虫
