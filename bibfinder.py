#!/usr/bin/env python

import datetime
import os
import random
import re
import string
import sys
import urllib
import wsgiref.handlers

from django.utils import simplejson

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import login_required

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

class HomePage(BaseRequestHandler):
  """Lists the notes """

  #@login_required
  def get(self,id=0):
      isbn = self.request.get('isbn')
      params = urllib.urlencode({'query':'{"type":"\/type\/edition","isbn_10":"'+isbn+'"}'})
      f = urllib.urlopen("http://openlibrary.org/api/things?%s" % params)
      out = f.read()
      self.generate('index.html', {
          'isbn': out 
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
  ], debug=_DEBUG)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
