#!/usr/bin/env python

import urllib
import simplejson
import sys


filename = 'isbn_list'

for line in file(filename).readlines():
    [isbn,oclc] = line.strip().split(' ')
    #params = urllib.urlencode({'method': 'getMetadata', 'format': 'xml', 'fl': 'lccn'})
    params = urllib.urlencode({'query':'{"type":"\/type\/edition","isbn_13":"'+isbn+'"}'})
    f = urllib.urlopen("http://openlibrary.org/api/things?%s" % params)
    res = simplejson.loads(f.read())
    if len(res['result']):
        id = res['result'][0]
        url = "http://openlibrary.org"+id+'.rdf'
        g = urllib.urlopen(url)
        data = g.read()
        FILE = open('rdf/'+oclc+'.rdf',"w")
        FILE.write(data)
        print oclc

