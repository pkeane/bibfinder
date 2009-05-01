#!/usr/bin/env python

import datetime
import feedparser
import os
import random
import re
import simplejson
import string
import sys
import urllib
import wsgiref.handlers

from django.utils import simplejson
from BeautifulSoup import BeautifulSoup

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import login_required


# worldcat url
# http://www.worldcat.org/profiles/pkeane/lists


# Set to true if we want to have our webapp print stack traces, etc
_DEBUG = True

class BaseRequestHandler(webapp.RequestHandler):
  """Supplies a common template generation function.

  When you call generate(), we augment the template variables supplied with
  the current user in the 'user' variable and the current webapp request
  in the 'request' variable.
  """
  def generate(self, template_name, template_values={}):
    values = {
      'request': self.request,
      'user': users.GetCurrentUser(),
      'login_url': users.CreateLoginURL(self.request.uri),
      'logout_url': users.CreateLogoutURL('http://' + self.request.host + '/'),
      'debug': self.request.get('deb'),
      'application_name': 'BibFinder',
    }
    values.update(template_values)
    directory = os.path.dirname(__file__)
    path = os.path.join(directory, os.path.join('templates', template_name))
    self.response.out.write(template.render(path, values, debug=_DEBUG))

class TitlesJson(BaseRequestHandler):
    def get(self):
      url = self.request.get('url')
      d = feedparser.parse(url)
      titles = [] 
      for entry in d['entries']:
          titles.append({'guid':entry['guid'].replace('http://www.worldcat.org/oclc/',''),'title':entry['title']});

      self.generate('index.html', {
          'titles': titles,
      })

class HomePage(BaseRequestHandler):
  """Lists the notes """

  #@login_required
  def get(self):
      data = ''
      lists = []
      wcname = self.request.get('wcname')
      if wcname:
          url = "http://www.worldcat.org/profiles/"+wcname+"/lists"
          soup = BeautifulSoup(urllib.urlopen(url).read())
          for list in soup('td','list'):
              list_url = 'http://www.worldcat.org'+list.contents[1]['href']+'/rss'
              list_name = list.contents[1].contents[0].contents[0]
              lists.append({'list_url':list_url,'list_name':list_name})
            
            

#          params = urllib.urlencode({'query':'{"type":"\/type\/edition","isbn_10":"'+isbn+'"}'})
#          f = urllib.urlopen("http://openlibrary.org/api/things?%s" % params)
#          res = simplejson.loads(f.read())
#          id = res['result'][0]
#          url = "http://openlibrary.org"+id+'.json'
#          g = urllib.urlopen(url)
#          data = g.read()

      self.generate('index.html', {
          'wcname': wcname,
          'lists': lists 
      })

  def post(self):
      note_title = self.request.get('note_title')
      note_text =  self.request.get('note_text')
      slug = slugify(note_title) 
      if (note_text and note_title):
          record = Note(note_title=note_title,note_text=note_text,slug=slug);
          record.put()
      self.redirect('/')


def main():
  application = webapp.WSGIApplication([
    ('/', HomePage),
    ('/list_titles',TitlesJson ),
  ], debug=_DEBUG)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
