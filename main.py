#!/usr/bin/env python
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
import urllib2
import re

servers = [u"ブルー", u"オレンジ", u"グリーン"]
pages   = [u"トップ", u"1", u"2", u"3", u"4", u"5"]

class MainHandler(webapp.RequestHandler):
    def get(self):
        res = urllib2.urlopen("http://hiratara.dyndns.org:8080/chaberi/")
        content = "".join(res)
        if not content is unicode: content = content.decode("UTF-8")

        fail = False
        for server, page in ((s, p) for p in pages for s in servers):
            if re.match(u"%s/%s" % (server, page), content): 
                fail = True
                break

        self.response.out.write('Failed' if fail else 'OK')

def main():
    application = webapp.WSGIApplication([('/', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
