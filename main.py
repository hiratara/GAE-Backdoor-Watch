#!/usr/bin/env python
# -*- coding: utf-8 -*-
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
import urllib2
import re
from model import LastError

backdoor_url = "http://hiratara.dyndns.org:8080/chaberi/"
# backdoor_url = "http://hiratara.dyndns.org:8080"
servers = [ur"ブルー", ur"オレンジ", ur"グリーン"]
pages   = [ur"トップ", ur"2", ur"3", ur"4", ur"5"]
last_error_key = "lasterror"

class MainHandler(webapp.RequestHandler):
    def is_contents_ok(self, content):
        for server, page in ((s, p) for p in pages for s in servers):
            if not re.search(ur"%s/%s" % (server, page), content): 
                return False
        return True

    def get(self):
        last_error = LastError.get_by_key_name(last_error_key)

        res = urllib2.urlopen(backdoor_url)
        content = "".join(res)
        if not content is unicode: content = content.decode("UTF-8")

        if self.is_contents_ok(content):
            if last_error:
                last_error.delete()
                message = 'recover'
            else:
                message = 'OK'

            self.response.out.write(message)
            return

        should_be_reported = True
        if last_error:
            should_be_reported = False
        else:
            LastError(key_name=last_error_key).put()

        self.response.out.write('fail' if should_be_reported else 'no report')

def main():
    application = webapp.WSGIApplication([('/', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
