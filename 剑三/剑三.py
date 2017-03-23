#coding:utf-8
import requests
import urllib2
import re
import HTMLParser
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
url="http://tieba.baidu.com/f?kw=%BD%A3%C8%FD&fr=ala0&tpl=5"

def getHtml(url):
    header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0','Referer' : '******'}
    request=urllib2.Request(url,headers=header)
    response=urllib2.urlopen(request)
    text=response.read()
    #print text
    return text

def getUrls(html):
    pattern=re.compile('<a href="/p/(.*?)"')
    items=re.findall(pattern,html)
    urls=[]
    for item in items:
        urls.append('https://tieba.baidu.com/p/'+item)
    return urls

def getContent(url):
    html = getHtml(url)
    # pattern=re.compile('style="width: 416px">(.*?)</h3><span class="core_title_btns pull-right">  ')
    # items=re.findall(pattern,html)
    # with open("jiansan.txt","a") as f:
    #     f.write(items[0]+"\n")
    pattern=re.compile(r'<meta name="description" content="(.*?)" /><meta charset="UTF-8">',re.S)
    items2=re.findall(pattern,html)
    with open("jiansan.txt","a") as f:
        for item in items2:
            print(item)
            f.write(item+"\n")



html=getHtml(url)
urls=getUrls(html)
for url in urls:
    try:
        getContent(url)
    except Exception,e:
        print e

