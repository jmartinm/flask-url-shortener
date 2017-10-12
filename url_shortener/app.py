"""URL Shortening service main application."""

from flask import Flask
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)
# Once the application becomes a Python library, the configuration
# would be in a config.py file, and loaded via
# app.config.from_object('yourapplication.default_settings')
application.config.update(
    DEBUG=True,
    SECRET_KEY='THIS_SHOULD_BE_SECRET',
    SQLALCHEMY_DATABASE_URI='postgresql+psycopg2://babylon:babylon@database:5432/babylon',
    CACHE_REDIS_URL='redis://redis:6379/0'
)

cache = Cache(application, config={'CACHE_TYPE': 'redis'})
db = SQLAlchemy(application)
