#!/usr/bin/env python

from xml.dom.minidom import parse, parseString
from BeautifulSoup import BeautifulSoup
import codecs
import datetime
import feedparser
import os
import random
import re
import simplejson as json
import string
import sys
import urllib

#necessary for printing to file
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

wcname = 'zdoleshal'

def main():
    url = "http://www.worldcat.org/profiles/"+wcname+"/lists"
    soup = BeautifulSoup(urllib.urlopen(url).read())
    for list in soup('td','list'):
        list_url = 'http://www.worldcat.org'+list.contents[1]['href']+'/rss'
        list_name = list.contents[1].contents[0].contents[0]
        d = feedparser.parse(list_url)
        for entry in d['entries']:
          oclcnum = entry['guid'].replace('http://www.worldcat.org/oclc/','')
          title = entry['title'].encode("utf-8")
#          params = urllib.urlencode({'method': 'getMetadata', 'format': 'xml', 'fl': 'lccn'})
#          dom = parseString(urllib.urlopen("http://xisbn.worldcat.org/webservices/xid/oclcnum/"+oclcnum+"?%s" % params).read())
#          el = dom.getElementsByTagName("oclcnum")
#          if len(el):
#              lccn = el[0].getAttribute('lccn')
#              if lccn:
#                  #print lccn
#              else:
#                  #print "no lccn"
#                  #print urllib.urlopen("http://xisbn.worldcat.org/webservices/xid/oclcnum/"+oclcnum+"?%s" % params).read()
#          else:
#              #print "no go"
          if title:
              print list_name+' %%% '+title.decode("utf-8")+' %%% '+oclcnum
          else:
              print list_name+' %%% NO TITLE %%% '+oclcnum


if __name__=='__main__':
    main()
