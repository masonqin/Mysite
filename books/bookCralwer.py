# -*- coding: utf-8 -*-

import urllib2
import urllib
import re
import thread
import time 
from models import DouBanBook

#gbkTypeStr = unicodeTypeStr.encode("GBK",'ignore');

class Spider_Model:

    def __init__(self):
        self.page = 0
        self.pages = []
        self.enable = False


    def GetPage(self,page):
        myUrl = "http://book.douban.com/top250?start=" + str(page*25)   
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'   
        headers = { 'User-Agent' : user_agent }   
        req = urllib2.Request(myUrl, headers = headers)   
        myResponse = urllib2.urlopen(req)  
        myPage = myResponse.read()     
        unicodePage = myPage.decode("utf-8",'ignore')  

        pattern = re.compile(r"""
            <table.*?>.*?
                <tr.*?class="item">.*?
                    <td.*?width=.*?valign="top">.*?
                        <img.*?src="(.*?)".*?width=.*?>.*?      #item1 图片链接
                    </td>.*?
                    <td.*?valign="top">.*?
                    <div.*?>.*?
                        <a.*?href="(.*?)".*?>                   #item2 书目链接
                           \s*(\S*?\s*?\S*?)\s*(<span.*?>(.*?)</span>)*?\s* 
                                                                #item3 5书名
                        </a>.*? 
                    </div>.*?
                    <p.*?class="pl".*?>
                        (.*?/?.*?)                              #item6 作者
                        \s*/\s*
                        (.*?)                                   #item7 出版社
                        \s*/\s*
                        (\S*)                                   #item8 日期
                        \s*/\s* 
                        (.*?)
                        \s*                                     #item9 售价                                      
                    </p>.*? 
                    <div.*?class="star.*?>.*?
                        <span.*?class="rating_nums">
                            (.*?)                               #item10 评分信息
                        </span>.*?
                        <span.*?class="pl">
                            \( \s*  (.*?) \s* \)                #item11 评价人数
                        </span>.*?                       
                    </div>.*? 
                    </td>.*?
            </table>""",re.S|re.X)

        
        myItems = pattern.findall(unicodePage)
        offset = 0
        g_num = page*25
        items = []
        for item in myItems:
            
            offset += 1
            print g_num + offset
            print item[0] + "\n"
            print item[1] + "\n"
            print u"书名："   + item[2]+item[4] + "\n"

            print u"作者："   + item[5] + "\n"
            print u"出版社：" + item[6] + "\n"
            print u"日期："   + item[7] + "\n"
            print u"售价："   + item[8] + "\n"
            print u"评分："   + item[9] + "\n"
            print u"评价数："   + item[10] + "\n"

            p = DouBanBook(
                    topNum = g_num + offset,
                    picLink = item[0],
                    itemLink = item[1],
                    titleMain = item[2],
                    titleSec = item[4],
                    author = item[5],
                    publisher = item[6],
                    pubdate = item[7],
                    price = item[8],
                    score = item[9],
                    evaluation = item[10]
                )
            p.save()
            print "--------------------------------------"

    def Start(self):    
        self.enable = True    
        page = 0    
    
        print u'正在加载中请稍候......'    
              
        #thread.start_new_thread(self.LoadPage,())    
            
        #----------- 加载处理糗事百科 -----------    
        while self.enable:    
            # 如果self的page数组中存有元素    
            if page<4:    
                self.GetPage(page)    
                page += 1
            else:
                self.enable = False
        

myModel = Spider_Model()    
myModel.Start()
