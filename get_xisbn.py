#!/usr/bin/env python

from xml.dom.minidom import parse, parseString
import urllib
import sys


filename = 'zach_lists'

for line in file(filename).readlines():
    [listname,title,oclc] = line.strip().split(' %%% ')
    params = urllib.urlencode({'method': 'getMetadata', 'format': 'xml', 'fl': '*'})
    data = urllib.urlopen("http://xisbn.worldcat.org/webservices/xid/oclcnum/"+oclc+"?%s" % params).read()
    FILE = open('xisbn/'+oclc,"w")
    FILE.write(data)
    print oclc


