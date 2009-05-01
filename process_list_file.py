#!/usr/bin/env python

from xml.dom.minidom import parse, parseString
import urllib
import sys


filename = 'zach_lists'

for line in file(filename).readlines():
    [listname,title,oclc] = line.strip().split(' %%% ')
    params = urllib.urlencode({'method': 'getMetadata', 'format': 'xml', 'fl': 'lccn'})
    dom = parseString(urllib.urlopen("http://xisbn.worldcat.org/webservices/xid/oclcnum/"+oclc+"?%s" % params).read())
    el = dom.getElementsByTagName("oclcnum")
    if len(el):
        lccn = el[0].getAttribute('lccn')
        if lccn:
            print lccn+' '+oclc
        else:
            print "no lccn"
    else:
        print "no go"

