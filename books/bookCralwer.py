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
                        <img.*?src="(.*?)".*?width=.*?>.*?          #item0 图片链接
                    </td>.*?
                    <td.*?valign="top">.*?
                    <div.*?>.*?
                        <a.*?href="(.*?)".*?title="(.*?)".*?>.*?    #item1 书目链接  #item2 书名
                        \s*?(<span.*?>\s*(.*?)</span>)*?\s*?        #4副书
                        </a>.*? 
                        \s*?(<span.*?>\s*(.*?)</span>)*?\s*?        #6原名
                    </div>.*?
                    <p.*?class="pl".*?>
                        (.*?)                                       #item7 作者 出版社 日期 售价                                                      
                    </p>.*? 
                    <div.*?class="star.*?>.*?
                        <span.*?class="rating_nums">
                            (.*?)                                   #item8 评分信息
                        </span>.*?
                        <span.*?class="pl">
                            \( \s*  (.*?) \s* \)                    #item9 评价人数
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
            try:
                print item[0] + "\n"
                print item[1] + "\n"
                print u"书名:"   + item[2] + "\n"
                print u"副名:"   + item[4] + "\n"
                print u"原名:"   + item[6] + "\n"
            except:
                print u"字符非法 \n"
            #print u"详细"   + item[7] + "\n"
            pattern_detail = re.compile(r"""
                        \s*(.*?)                        #item0 作者
                        \s*/\s*
                        (\S*?)                          #item1 出版社
                        \s*/\s*
                        (\d{1}\S*-?\d{1}\S*-?\d*\S*)   #item2 日期 xxx-xx-xx 
                                                        #           xxx年xx月 
                                                        #           可能连价格一起匹配
                        \s*/\s* 
                        (\d*\.\d*\S*)                   #item3 售价
                        \s*                                     
                        """,re.S|re.X)

            detailItems = pattern_detail.findall(item[7])
            #print detailItems
            for detailItem in detailItems:
                try:
                    print u"作者:"   + detailItem[0] + "\n"
                    print u"出版社:" + detailItem[1] + "\n"
                    print u"日期:"   + detailItem[2] + "\n"
                    print u"售价:"   + detailItem[3] + "\n"
                except:
                    print u"字符非法 \n"

            print u"评分:"   + item[8] + "\n"
            print u"评价数:" + item[9] + "\n"

            try:
                top_index = g_num + offset
                p = DouBanBook.objects.get(topNum=top_index)    

                p.topNum = top_index
                p.picLink = item[0]
                p.itemLink = item[1]
                p.titleMain = item[2]
                p.titleSec = item[4]
                p.titleOri = item[6]
                p.author = detailItem[0]
                p.publisher = detailItem[1]
                p.publishdate = detailItem[2]
                p.price = detailItem[3]
                p.score = item[8]
                p.evaluation = item[9]

                p.save()

                print "------------------update---------------"

            except:   
                p = DouBanBook(
                        topNum = g_num + offset,
                        picLink = item[0],
                        itemLink = item[1],
                        titleMain = item[2],
                        titleSec = item[4],
                        titleOri = item[6],
                        author = detailItem[0],
                        publisher = detailItem[1],
                        publishdate = detailItem[2],
                        price = detailItem[3],
                        score = item[8],
                        evaluation = item[9]
                    )
                p.save()

                print "------------------create---------------"

            print "--------------------------------------"

    def Start(self):    
        self.enable = True    
        page = 0    
    
        print u'正在加载中请稍候......'    
              
        #thread.start_new_thread(self.LoadPage,())    
   
        while self.enable:    
            # 如果self的page数组中存有元素    
            if page<10:    
                self.GetPage(page)    
                page += 1
            else:
                self.enable = False
        

#myModel = Spider_Model()    
#myModel.GetPage(1)
