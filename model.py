from google.appengine.ext import db

class LastError(db.Model):
    datetime = db.DateTimeProperty(auto_now_add=True)
