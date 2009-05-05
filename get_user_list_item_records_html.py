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
    for f in os.listdir(lists_directory):
        records_directory = f.replace('.rss','')
        records_path = lists_directory+'/'+records_directory
        if not os.path.exists(records_path):
            os.mkdir(records_path)
        d = feedparser.parse(records_path+'.rss')
        for entry in d.entries:
            book_url = entry['guid']
            book_filename = book_url.split('/').pop()
            book_data = urllib.urlopen(book_url).read()
            FILE = open(records_path+'/'+book_filename+'.html',"w")
            FILE.write(book_data)
            print "wrote "+book_filename
            
            


#    soup = BeautifulSoup(urllib.urlopen(url).read())
#    for list in soup('td','list'):
#        list_url = 'http://www.worldcat.org'+list.contents[1]['href']+'/rss'
#        list_name = dirify(list.contents[1].contents[0].contents[0])
#        data = urllib.urlopen(list_url).read()
#        FILE = open(lists_directory+'/'+list_name+'.rss',"w")
#        FILE.write(data)
#        print list_name

if __name__=='__main__':
    main()
