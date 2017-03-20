#coding:utf-8
import requests
import urllib2
import re
import HTMLParser
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
url="http://daily.zhihu.com/"
#获取源代码
def getHtml(url):
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0','Referer' : '******'}
    request=urllib2.Request(url,headers=header)
    response=urllib2.urlopen(request)
    text=response.read()
    # print text
    return text
def getUrls(html):
    pattern=re.compile('<a href="/story/(.*?)"')
    items=re.findall(pattern,html)
    # print items
    urls=[]
    for item in items:
        urls.append('http://daily.zhihu.com/story/'+item)
        # print urls[-1]
    return urls

def getContent(url):
    html = getHtml(url)
    pattern=re.compile('<h1 class="headline-title">(.*?)</h1>')
    items=re.findall(pattern,html)
    print '**************'+items[0]+'************'
    with open("zhihu.txt","a") as f:
        f.write("\n-------------------------------------"+items[0]+"-----------------------------------------\n")
    pattern=re.compile(r'<div class="content">.*?<p>(.*?)</div>',re.S)
    items2=re.findall(pattern,html)
    with open("zhihu.txt","a") as f:
        for item in items2:
            for content in characterProcessing(item):
                f.write(content)
                print(content)


#过滤一些没用的标签
def characterProcessing(html):
    htmlParser=HTMLParser.HTMLParser()
    pattern=re.compile('<p>(.*?)</p>|<li>(.*?)</li>.*?',re.S)
    items=re.findall(pattern,html)
    result=[]
    for index in items:
        if index!='':
            for content in index:
                tag=re.search('<(.*?)>',content)
                http=re.search('<.*?http.*?',content)
                html_tag=re.search('&',content)
                if html_tag:
                    content=htmlParser.unescape(content)
                if http:
                    continue
                elif tag:
                    pattern = re.compile('(.*?)<.*?>(.*?)</.*?>(.*?)')#
                    items=re.findall(pattern,content)
                    content_tags=''
                    if len(items)>0:
                        for item in items:
                            if len(item)>0:
                                for item_s in item:
                                    content_tags=content_tags+item_s
                            else:
                                content_tags=content_tags+item_s
                        content_tags=re.sub('<.*?>','',content_tags)
                        result.append(content_tags)
                    else:
                        continue
                else:
                    result.append(content)
    return result


html=getHtml(url)
urls=getUrls(html)
for url in urls:
    try:
        getContent(url)
    except Exception,e:
        print e