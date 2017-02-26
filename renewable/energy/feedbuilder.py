import feedparser
import re
import urllib2
from bs4 import BeautifulSoup
import urllib2
import datetime
import time

c=0
def geturl(ent,site):
    if site == "google" :
        return ent.link
    elif site == "bing" :
        return ent.link

def gettitle(ent,site):
    if site == "google" :
        return ent.title
    elif site == "bing" :
        return ent.title
def getimageurl(ent , site):
    if site == "google" :
        summary=ent.summary
        soup = BeautifulSoup(summary, 'html.parser')
        try:
            return soup.find("img").attrs['src']
        except:
            return None
        # if 'src' in soup.find("img").attrs:
        #     return soup.find("img").attrs['src']
        # return None

def cleanhtmltags(raw_html):
    cleanr =re.compile('<.*?>')
    withouttags = re.sub(cleanr,'', raw_html)
    # return withouttags
    withouttags.split()
    without_mult_spaces= ' '.join(withouttags.split())
    return without_mult_spaces


def parse_description(ent , site):
    if site == "google" :
        description=ent.summary
        soup = BeautifulSoup(description, 'html.parser')
        des= soup.find_all("font", {"size": "-1"})[1]
        des_string=unicode.join(u'\n',map(unicode,des))
        return  cleanhtmltags(des_string)
def getpubdate(ent , site):
        if site == "google" :
            return ent.published_parsed
        elif site == "bing" :
            return ent.published_parsed


def get_redirected_url(url):
    # op = urllib2.build_opener(urllib2.HTTPCookieProcessor).open(url, headers={'User-Agent' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/11.04 Chromium/12.0.742.112 Chrome/12.0.742.112 Safari/534.30"})
    opener=urllib2.build_opener(urllib2.HTTPCookieProcessor)
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    op = opener.open(url)
    try:
        opener=urllib2.build_opener(urllib2.HTTPCookieProcessor)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        op = opener.open(url)
        return op.geturl()
    except:
        print "Error"
        return


def get_agency(ent, site):
    if site == "google" :
        summary = ent.summary
        soup = BeautifulSoup(summary, 'html.parser')
        pub_agency= soup.find_all("font", {"size": "-1"})[0]
        ch1 = pub_agency.findChildren()
        pub_agency = ch1[1].string
        return pub_agency


class feeds(object):
    title = ""
    originalurl = ""
    imageur = ""
    pubdate = ""
    pub_agency = ""
    description = ""
    pub = "" 

def get_google_feed(query , num=10):
    c=0
    query_list = query.split(' ')
    query_format = query_list[0]
    for i , q in enumerate(query_list):
        if (i>0):
            query_format=query_format+'+'+q
        url = "http://news.google.com/news?q="+query_format+"&output=rss"+"&num="+str(num)
    parsed = feedparser.parse(url)
    # print parsed.entries[0]
    my_feeds = []
    for ent in parsed.entries:
        c=c+1
        feeder = feeds()  
        feeder.title=gettitle(ent,"google")
        #print feeder.title
        feeder.originalurl=geturl(ent,"google")
        # cleanurl=get_redirected_url(originalurl)
        feeder.imageurl=getimageurl(ent,"google")
        feeder.pubdate=getpubdate(ent,"google")
        #print pubdate
        #print pubdate[0]
        #print pubdate[0] + 1
        #today = datetime.datetime.now()
        #print today.year
        '''if pubdate[0] == today.year:
           print 'yes' '''
        feeder.pub_agency=get_agency(ent,"google")
        #print
        #print feeder.pub_agency
        feeder.description=parse_description(ent,"google")
        
        my_feeds.append(feeder)
    return my_feeds


def get_bing_feed(query , num=10):
    query_list = query.split(' ')
    query_format = query_list[0]
    for i , q in enumerate(query_list):
        if (i>0):
            query_format=query_format+'+'+q
    url = "https://www.bing.com/news/search?q="+query_format+"&format=RSS"
    parsed = feedparser.parse(url)
    for ent in parsed.entries:

        title =gettitle(ent,"bing")
        #print title
        originalurl = geturl(ent,"bing")
        description=ent.summary_detail.value
        # cleanurl=get_redirected_url(originalurl)
        pubdate=getpubdate(ent,"bing")
    return

# query = raw_input("Enter the keyword to be seaarched")
# num = raw_input("Enter num of results you want")

'''
c=0
query="IIIT Hydrabad"
num=100
get_google_feed(query,num)
print c

'''

