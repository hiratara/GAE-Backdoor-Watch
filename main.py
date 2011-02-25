#!/usr/bin/env python
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
import urllib2
import re

servers = [u"ブルー", u"オレンジ", u"グリーン"]
pages   = [u"トップ", u"1", u"2", u"3", u"4", u"5"]

class MainHandler(webapp.RequestHandler):
    def is_contents_ok(self, content):
        for server, page in ((s, p) for p in pages for s in servers):
            if re.match(u"%s/%s" % (server, page), content): 
                return False
        return True

    def get(self):
        res = urllib2.urlopen("http://hiratara.dyndns.org:8080/chaberi/")
        content = "".join(res)
        if not content is unicode: content = content.decode("UTF-8")
        if self.is_contents_ok(content):
            self.response.out.write('OK')
            return

        self.response.out.write(fail)

def main():
    application = webapp.WSGIApplication([('/', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
