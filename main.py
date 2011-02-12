#!/usr/bin/env python
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
import urllib2


class MainHandler(webapp.RequestHandler):
    def get(self):
        res = urllib2.urlopen("http://ubuntumini:8080/chaberi/")
        self.response.out.write("".join(res))


def main():
    application = webapp.WSGIApplication([('/', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
