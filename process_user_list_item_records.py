#!/usr/bin/env python

from xml.dom.minidom import parse, parseString
from BeautifulSoup import BeautifulSoup
import atomlib
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
atomdir = 'worldcat_atoms'
scheme = 'http://daseproject.org/category/metadata'

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
        topic = d.feed['title']
        for entry in d.entries:
            e = atomlib.Entry()
            e.setUpdated()
            book_url = entry['guid']
            book_filename = book_url.split('/').pop()
            e.setTitle(book_filename)
            print 'oclc_num: '+book_filename
            e.addCategory('oclc_num',scheme,None,book_filename)
            print 'topic: '+topic
            e.addCategory('topic',scheme,None,topic)
            book_record_path = records_path+'/'+book_filename+'.html'
            bib_html_path = records_path+'/'+book_filename+'.bib.html'
            if not os.path.exists(book_record_path):
                book_data = urllib.urlopen(book_url).read()
                FILE = open(book_record_path,"w")
                FILE.write(book_data)
                print "wrote "+book_filename
            else:
                if not os.path.exists(book_record_path):
                    soup = BeautifulSoup(open(book_record_path).read())
                    bib_data = str(soup.find('div',id='bib-cont'))
                    FILE = open(bib_html_path,"w")
                    FILE.write(bib_data)
                    print "wrote "+bib_html_path
                else:
                    soup = BeautifulSoup(unicode(open(bib_html_path).read(),'utf-8'))
                    #print soup.find('h1','title').decode('utf-8')
                    # title && subtitle
                    if soup.find('img','cover'):
                        enc = soup.find('img','cover')['src']
                        print 'enclosure: '+enc
                        e.addLink(enc,'enclosure')
                    if soup.find('h1','title'):
                        title = soup.find('h1','title').contents[0].split(':')
                        if len(title):
                            ti = title[0]
                            e.addCategory('title',scheme,None,ti)
                        if len(title) > 1:
                            subti = title[1]
                            e.addCategory('subtitle',scheme,None,subti)
                    auth = soup.find('th',text='Author:')
                    if auth:
                        for a in auth.parent.findNextSibling('td').findAll('a'):
                            author = a.contents[0]
                            e.addCategory('author',scheme,None,author)
                    format = soup.find('th',text='Edition/Format:')
                    if format:
                        fmt = format.parent.findNextSibling('td').find('span','bks')
                        if fmt and len(fmt.contents):
                            format = fmt.contents[0].strip()
                            e.addCategory('format',scheme,None,format)
                    series = soup.find('th',text='Series:')
                    if series:
                        for a in series.parent.findNextSibling('td').findAll('a'):
                            if len(a.contents):
                                series = a.contents[0]
                                e.addCategory('series',scheme,None,series)
                    pub = soup.find('th',text='Publisher:')
                    if pub:
                        publisher = pub.parent.findNextSibling('td').contents[0]
                        e.addCategory('publisher',scheme,None,publisher)
                    subjects = soup.find('h3',text='Subjects')
                    if subjects:
                        for subj in subjects.parent.findNextSibling('ul').findAll('a'):
                            if len(subj.contents):
                                if 'View all s' not in subj.contents[0]:
                                   subject = subj.contents[0]
                                   e.addCategory('subject',scheme,None,subject)

            FILE = open('worldcat_atoms/'+book_filename+'.atom',"w")
            FILE.write(e.asXml())


if __name__=='__main__':
    main()
