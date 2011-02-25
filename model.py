from google.appengine.ext import db

class LastError(db.Model):
    date = db.DateTimeProperty(auto_now_add=True)
