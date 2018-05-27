# duck_prophet
### 春江水暖“鸭先知”，“鸭先知”是一个利用新闻文本做舆情分析的系统。——NKU_iip_Aron<br>

#### 1.	软硬件环境说明
    a)	Python2.7及其相关python依赖包,缺啥补啥<br>
      i.	tornado<br>
      ii.	requests<br>
      iii.	pymysql<br>
      iv.	urllib2<br>
      v.	cookielib<br>
      vi.	zlib<br>
      vii.	Queue<br>
      viii.	bs4<br>
      ix.	demjson<br>
      x.	textrank4zh<br>
      xi.	elasticsearch<br>
      xii.	jieba<br>

    b)	mysql，启动server<br>
    c)	elasticsearch-6.x以上，默认端口配置，启动elasticsearch<br>
    d)	elasticsearch 要求机器4G以上内存<br>



#### 2.	项目部署说明
    a)	进入项目文件夹的duck_prophet/config/db_operate/目录里的mysql_conf.py文件，修改mysql数据库连接配置。<br>
    b)	进入项目文件夹的script目录<br>
    c)	执行mysql_prepare.py脚本，完成数据库建库建表工作<br>
    d)	执行history_prepare.py脚本，抓取部分历史新闻数据，执行完成之后<br>
    e)	执行mysql2elastic.py脚本，完成全量导入elasticsearch简历索引工作<br>
    f)	执行daily_crawler.py脚本，开启日常爬虫程序，前台或后台运行<br>
    g)	执行mysql2elastic_yesterday.py脚本，开启每日索引新闻程序<br>
    h)	执行tornado_server.py脚本，开启web接口服务,端口为8888<br>


#### 3.	web接口说明，三个主要接口，请求地址应为host:8888,下图中18888端口不用管
    a)	news_search，请求方式如下，POST类型，返回Json格式新闻列表以及结果数目。<br>
      URL参数：target=news_search&page_num=分页号<br>
      POST请求参数：<br>
        Polarity: 极性选项，可选“all”、“1”、“-1”、“0”，表示全部、正面、负面、中性<br>
        src: 新闻源选项，可选“全部”“新浪”“搜狐”“新华”“腾讯”“网易”<br>
        topic: 话题选项，短文本<br>
        date_range: 日期可用两种类型，“2018-01-20 2018-01-30”这种表示某段时间范围，也可传“day”，“week”，“month”，“year”，“all”表示最近一天一周等等。<br>
![接口1](https://github.com/xiaopangxia/duck_prophet/blob/master/images/pic_1.bmp)

    b)	news_analyze，请求方式如下，POST类型，返回某篇文章的摘要句以及带权关键词列表，Json格式。<br>
      Url参数：target=news_analyze<br>
      POST请求参数：<br>
        news_url: 新闻文章的地址，也是它的唯一标识，可以来自与前一个接口返回的数据结果，也可以是未收录的新闻地址。<br>
        news_title: 新闻标题<br>
        news_src: 新闻源，写一个就行，不在五个预制来源内也没关系。<br>

![接口2](https://github.com/xiaopangxia/duck_prophet/blob/master/images/pic_2.bmp)

    c)	topic_trend，请求方式如下，POST类型，返回某段时间某个话题的分时文章数量，表示话题热度趋势，Json格式。
      Url参数：target=topic_trend<br>
      POST请求参数：<br>
      topic: 关注的话题文本<br>
      time_mode: 要关注话题的时间模式<br>
              day_week:	最近一周每日<br>
              day_month:	最近一个月每日<br>
              day_year:		最近一年每日<br>
              week_year:	最近一年每周<br>
              month_year:	最近一年每月<br>
 ![接口3](https://github.com/xiaopangxia/duck_prophet/blob/master/images/pic_3.bmp)
 
 #### 4.测试前端截图
 ![前端截图1](https://github.com/xiaopangxia/duck_prophet/blob/master/images/screen_1.PNG)
 ![前端截图2](https://github.com/xiaopangxia/duck_prophet/blob/master/images/screen_2.PNG)
 ![前端截图3](https://github.com/xiaopangxia/duck_prophet/blob/master/images/screen_3.PNG)




