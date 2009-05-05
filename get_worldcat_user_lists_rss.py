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
lists_directory = 'user_lists'

def dirify(str):
    str = re.sub('\&amp\;|\&', ' and ', str) 
    str = re.sub('[-\s]+', '_', str)
    return re.sub('[^\w\s-]', '', str).strip().lower()

def main():
    url = "http://www.worldcat.org/profiles/"+wcname+"/lists"
    soup = BeautifulSoup(urllib.urlopen(url).read())
    for list in soup('td','list'):
        list_url = 'http://www.worldcat.org'+list.contents[1]['href']+'/rss'
        list_name = dirify(list.contents[1].contents[0].contents[0])
        data = urllib.urlopen(list_url).read()
        FILE = open(lists_directory+'/'+list_name+'.rss',"w")
        FILE.write(data)
        print list_name

if __name__=='__main__':
    main()
