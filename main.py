#!/usr/bin/env python
# -*- coding: utf-8 -*-
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api import mail,urlfetch
import datetime
import re
from model import LastError

backdoor_url = "http://hiratara.dyndns.org/chaberi/"
servers = [ur"ブルー", ur"オレンジ", ur"グリーン", ur"ベータ版"]
pages   = [ur"トップ", ur"2", ur"3", ur"4", ur"5"]
last_error_key = "lasterror"
re_report = datetime.timedelta(hours=1)
mails_to = 'hira.tara@gmail.com'

class MainHandler(webapp.RequestHandler):
    def report(self, message):
        mail.send_mail(
            sender="hira.tara@gmail.com",
            to=mails_to,
            subject="backdoor report",
            body=message,
        )

    def is_contents_ok(self, content):
        for server, page in ((s, p) for p in pages for s in servers):
            if not re.search(ur"%s/%s" % (server, page), content): 
                return False
        if re.search(u"読み込めません", content): return False

        return True

    def get(self):
        last_error = LastError.get_by_key_name(last_error_key)

        error_message = ""
        is_good_status = False
        try:
            res = urlfetch.fetch(backdoor_url, deadline=4)
            if res.status_code == 200:
                content = res.content
                if not content is unicode: content = content.decode("UTF-8")

                is_good_status = self.is_contents_ok(content)
            else: error_message = "bad status %d" % res.status_code
        except Exception, e:
            error_message = str(e)

        self.response.headers['Content-Type'] = 'text/plain'
        if error_message == "":
            self.response.out.write("OK\n")
        else:
            self.response.out.write(error_message + "\n")

        if is_good_status:
            if last_error:
                last_error.delete()
                self.report("Recoverd now.\n")
            else: pass  # good status. NOP.
            return

        should_be_reported = True
        if last_error:
            elapsed = datetime.datetime.now() - last_error.datetime
            if elapsed > re_report:
                last_error.datetime = datetime.datetime.now()
                last_error.put()
            else:
                should_be_reported = False
        else:
            LastError(key_name=last_error_key).put()

        if should_be_reported:
            self.report(
                "Bad status. Check the backdoor.\n\n%s" % error_message
                )

def main():
    application = webapp.WSGIApplication([('/', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
