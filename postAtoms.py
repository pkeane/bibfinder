import fnmatch
import httplib2
import md5
import mimetypes
import os

"""
NOTE: this will use the filename (w/o extension) 
as the serial number
"""


coll = 'ee_jewish_history'
dase_url = "http://quickdraw.laits.utexas.edu/dase1"
path = "worldcat_atoms/"

def postFile(path,filename,dase_url,coll):
    slug = filename.replace('.atom','')
    headers = {'Content-Type': 'application/atom+xml;type=entry', 'Slug':'%s'%slug }
    f = file(path+filename, "rb")
    body = f.read()                                                                     
    f.close()                                                                                                            
    h = httplib2.Http(".cache")
    h.add_credentials('pkeane','opendata')
    url = dase_url+'/collection/'+coll+'/ingester'
    resp, content = h.request(url, "POST", body=body, headers=headers)  
    print resp
    print content

for f in os.listdir(path):
    if not fnmatch.fnmatch(f,'.*'):
        print "posting "+f
        postFile(path,f,dase_url,coll)
