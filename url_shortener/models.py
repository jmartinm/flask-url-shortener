"""URL Shortening service SQLAlchemy views."""

from .app import db


class Url(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    """Primary key. Used to produce the short URL with base 62 conversion."""

    url = db.Column(db.String(2000), unique=True, nullable=False, index=True)
    """Full URL. Max length of URL is 2000 - see https://stackoverflow.com/a/417184/890185"""

    def __repr__(self):
        return '<Url %r - %r>' % (self.id, self.url)
