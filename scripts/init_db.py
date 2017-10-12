"""This script is used to initialize the Database tables."""

from url_shortener.app import db

db.create_all()
