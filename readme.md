# 汽车之家定向爬虫及简单数据分析
## 爬虫方面
### 目前进展
* [ ] 实现对首页也简短文章的爬虫
* [ ] 实现了翻页的功能

### 跳板机版本
* [ ] **v1**:爬缩略信息和全部文章
* [ ] **v2**:爬缩略信息和文章评论
* [ ] **v3**:测试同时爬缩略信息、文章、评论

### 目前问题 20170118
* [x] 实现了用`UTF8`编码写入`json`的功能（原来的编码是ASCII）,通过`pepiline`加工，调用`codec`和`json`模块，同时要编辑相应的`setting.py`，在里面相应的`ITEM_PIPELINES`选项加上`ITEM_PIPELINES = {'autohome.pipelines.AutohomePipeline': 300,}`。http://blog.csdn.net/u012150179/article/details/32911511
* [x] 部分网站会先鉴定你是不是爬虫，直接用`start_urls = ['http://www.autohome.com.cn/all/']`会返回403-拒绝访问的错误码，这时就要加`User-Agent`，也就是`headers`,将原来的`start_urls = ['http://www.autohome.com.cn/all/']`改成`Request('http://www.autohome.com.cn/all/', headers=self.headers)`，就能200正常返回了。`Request`可以看做是一个可以自动封装的`start_urls`
* [x] 同一个网站，不同的页面进行爬虫，可以在`Requests`里面调用不同的`callback`函数，对原来的html页面进行解析。https://zm10.sm-tc.cn/?src=l4uLj4zF0NCIiIjRkIycl5aRntGRmovQjoqajIuWkJHQzs3Mx8bPoM7Lys%2FNzA%3D%3D&uid=678473732afa5c5cd8df78259839b081&hid=72d5959adb54c62721ef20e690bbb1cf&pos=1&cid=9&time=1484424809394&from=click&restype=1&pagetype=0000000000000402&bu=web&query=scrapy+%E5%A4%9A%E4%B8%AAitem&mode=&v=1&uc_param_str=dnntnwvepffrgibijbprsvdsei
* [ ] 评论数量是动态的，怎么获取动态的数据。应该用的是js进行动态的处理。在浏览器的F12下面找到了network,下面有一个`CountsByObjIds?_appid=cms&appid`的js访问接口，可以调节里面的参数，得到下面的请求`http://reply.autohome.com.cn/api/QueryComment/CountsByObjIds?_appid=cms&appid=1&dataType=json&objids=897874`返回一个json串，目前的做法是用urllib2从互联网中将内容解析出来，后期要考虑用scrapy自己的Requests和Response对象对内容进行解析
* [x] 每一页有一个是空的，怎么处理这个空值。在`pipeline`中，判断`article_url==[]`,如果等于就调用`from scrapy.exceptions import DropItem`，在相应的节点上加上`raise DropItem`主动吊起DropItem的事务
* [x] 通过在`setting.py`中设置`LOG_LEVEL = 'INFO'`，可以改变启动scrapy时候，显示日志的级别，一开始的级别是`LOG_LEVEL = 'DEBUG'`，会显示任务详细的日志，更方面编写过程中的调试。改成LOG_LEVEL = 'INFO'之后只会显示`INFO,WARINING,ERROR`等级的日志，更方便正式爬虫时查看爬取的速度，数量等。
* [ ] 对不同页面的爬取：spider通过Requests的callback选项指定相应的回调函数，可以实现对多个不同类型页面的爬取；不同页面的爬取，最好建多个Item便于维护；pepiline方面，通过if isinstance(item, AItem):来判断回调过来的item哪一个Item实例，然后进行相应的处理
* [ ] 要提交表单或者

### 目前问题 20170119
* [x] 从首页传每个页面的url的时候传错了，进入之后不是具体的文章链接。因为汽车之家改版了，有一个新的页面是纯粹图片的，要另外写一个爬虫。20170119发现了有一个返回文章的连接，通过分析发现拼接返回文章的部分是在html代码里面的，用response.xpath('//script[@type="text/javascript" and not(@src)]').re('(\?pvareaid=\d+)')[0]拼接相应的url，yield回这个parse
* [ ] 从api获取评论数量页面错误：http://reply.autohome.com.cn/api/QueryComment/CountsByObjIds?_appid=cms&appid=1&dataType=json&objids=897868，但是浏览器可以访问，估计要模拟一下请求
* [ ] 评论页面是通过api获取的http://reply.autohome.com.cn/showreply/ReplyJson.ashx?id=897978&page=1&ReplyCount=20&appid=1&datatype=jsonp&imgid=113196&callback=jsonpCallbackData&_=1484810584534
http://reply.autohome.com.cn/api/comments/show.json?count=50&page=9&id=897973&appid=1&datatype=json
* [x] 文章评论页面可能为空，try except为空时赋值为0.http://www.autohome.com.cn/news/201701/897838.html#pvareaid=102624
* [ ] 有部分文章是分页了的，要找到相应的分页文章
* [ ] 会有一些文章是没有内容的，也是个坑http://www.autohome.com.cn/tech/201607/890273.html#pvareaid=102624
	* 没有来源和编辑的页面：
		* 类型：新闻稿
			* http://www.autohome.com.cn/tuning/201606/889426.html#pvareaid=102624
			* http://www.autohome.com.cn/info/201509/879176.html#pvareaid=102624
			* http://www.autohome.com.cn/culture/201502/862113.html#pvareaid=102624
	* 最后一页
		* http://www.autohome.com.cn/all/5116/#liststart
* [ ] 通过yield的方式同时返回详细文章链接和评论api，发现详细文章链接可以爬到，但是评论页面不能爬取
* [x] 没有评论页面的话返回的commentlist:null:{"page":1,"commentcount":0,"commentcountall":0,"commentlist":null},提交的Request是http://reply.autohome.com.cn/api/comments/show.json?count=50&page=1&id=898156&appid=1&datatype=json
* [x] 修复了回复页面中的可能一开始就没有值的情况
* [x] 遇到一个问题：ajax动态页面，个人页的帮助值，精华帖，主帖，关注的车型都是通过这个加载
* [x] 汽车之家用户页面有robot禁止协议，scrapy也是遵循该协议，就爬不到
* [ ] 部分代码用re模块的，看一下能不能直接用scrapy的xpath('.//').re()解决
* [ ] pase_article_comment函数是通过fromdata来的，怎么通过response看到完整的url
* [x] user_info['tie_phone'] = ''.join(response.xpath('//a[@class="iphone"]/@data-title').extract()).strip()这个来解决可能xpath选择的字符串为空的问题
* [x] 部分爬虫没有response，发现了网站上有ROBOT不予许，在setting上加上了ROBOTSTXT_OBEY = False获取内容

### 20170226
* [x] 实现了汽车之家的模拟登陆，用到了scrapy的FormRequest功能，用meta={'cookiejar':1}实现了获取模拟登陆后的cookie功能
* [x] 通过meta之间传递cookiejar实现了访问用户的粉丝和关注列表
* [x] 修复了user_info['user_name']可能为空的情况
* [ ] 存在的隐患：
	* [ ] 部分ajax的页面没有用xhr的方式传值，可能存在隐患。但是目前是可以访问的
	* [x] IP被封了，由于爬的太快了，考虑用ip代理池。
	* [ ] IP代理加上了，要考虑怎么维护这个代理池
	* [ ] 考虑别的情况下用header访问，只有有用到cookie的时候才把cookie带上
	* [ ] 由于缓存的唯一url太多了，导致云主机的内存不足，考虑在不需要排除的request后面加上dont_filter=True实现不保存部分的url
* [x] setting中的DOWNLOAD_DELAY实现了抓取的频率；DOWNLOAD_TIMEOUT设置超时；CONCURRENT_REQUESTS设置并发量；USER_AGENT设置默认的user-agent；COOKIES_ENABLED设置是否带上cookie访问；DEFAULT_REQUEST_HEADERS设置request的默认部分；SPIDER_MIDDLEWARES设置spider的中间件；DOWNLOADER_MIDDLEWARES设置downloader中间件；ITEM_PIPELINES设置pipeline中间件；LOG_LEVEL设置打印日志的级别；LOG_FILE设置日志的名称
* [x] 增加downloader_middleware中的UserAgentMiddleware类，为每一个request随机一个ua
* [ ] Scrapy更新了:
	* [ ] `scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware` class is deprecated, use `scrapy.downloadermiddlewares.useragent.UserAgentMiddleware` instead
	* [x] log.msg has been deprecated, create a python logger and log through it instead
	*用了python本身的logging库解决了*
* [ ] 加了代理之后的分析：
	* [ ] 较多的情况可能代理用不到，所以要retry，retry的时候不清楚有没有更换代理
		* Retrying <GET http://i.autohome.com.cn/ajax/home/GetUserInfo?userid=24155248&r=0.924322805763&_=1488123990901> (failed 1 times): [<twisted.python.failure.Failure twisted.internet.error.ConnectionLost: Connection to the other side was lost in a non-clean fashion.>]
* [x] 没有检验user-agent有没有更换到，因为不知道怎么从request或者response中得到user-agent的数据
* [ ] http://reply.autohome.com.cn/api/QueryComment/CountsByObjIds?_appid=cms&appid=1&dataType=json&objids=899056用的是`GET`方法；http://reply.autohome.com.cn/api/comments/show.json?count=50用的是`POST`方法
* [x] cmd窗口显示出log的错误信息：Traceback (most recent call last):
  File "d:\python27\lib\logging\__init__.py", line 882, in emit
    stream.write(fs % msg.encode("UTF-8"))
UnicodeDecodeError: 'ascii' codec can't decode byte 0xd3 in position 210: ordinal not in range(128)
Logged from file retry.py, line 68
*用了python本身的logging库就没有问题了*
* [ ] 为什登陆后得到的cookie和浏览器提交的cookie不一样
* [ ] article_commnet_part还是有cookie发送到server
* [ ] http://account.autohome.com.cn/login?backUrl=http://i.autohome.com.cn/获得了一个cookie:Set-Cookie: rsessionid=c0f59e83-adf4-4a1d-9a85-a34c663f4915; domain=account.autohome.com.cn; expires=Tue, 28-Feb-2017 17:29:45 GMT; path=/; HttpOnly