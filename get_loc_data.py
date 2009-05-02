#!/usr/bin/env python

from xml.dom.minidom import parse, parseString
import urllib
import sys


filename = 'just_lccn'

for line in file(filename).readlines():
    [lccn,oclc] = line.strip().split(' ')
    data = urllib.urlopen("http://lccn.loc.gov/"+lccn+"/dc").read()
    FILE = open('dublin_core/'+oclc+'.atom',"w")
    FILE.write(data)
    print oclc

