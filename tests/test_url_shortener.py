# -*- coding: utf-8 -*-

import json

import pytest

from sqlalchemy_utils.functions import create_database, database_exists, \
    drop_database

from url_shortener.app import application, cache, db
from url_shortener.utils import is_url_valid
from url_shortener.models import Url


@pytest.fixture(scope='session')
def app(request):
    application.config.update(
        DEBUG=True,
        SECRET_KEY='TEST_SECRET_KEY',
        SQLALCHEMY_DATABASE_URI='postgresql+psycopg2://babylon:babylon@database:5432/testdb',
        CACHE_REDIS_URL='redis://redis:6379/1'
    )

    with application.app_context():
        cache.clear()
        if not database_exists(db.engine.url):
            create_database(db.engine.url)
            db.create_all()

        yield application

        drop_database(db.engine.url)
        cache.clear()


def test_shorten_url_returns_400_when_no_json_content_type(app):
    with app.test_client() as c:
        response = c.post(
            '/shorten_url',
            content_type='text/html',
            data=json.dumps({
                'test': 'test',
            }),
        )

    assert response.status_code == 400
    assert json.loads(response.data) == {u'message': u'no valid JSON data was received'}


def test_shorten_url_returns_400_when_no_url_key(app):
    with app.test_client() as c:
        response = c.post(
            '/shorten_url',
            content_type='application/json',
            data=json.dumps({
                'test': 'test',
            }),
        )

    assert response.status_code == 400
    assert json.loads(response.data) == {u'message': u'url key is missing from POST data'}


def test_shorten_url_returns_400_when_invalid_url(app):
    with app.test_client() as c:
        response = c.post(
            '/shorten_url',
            content_type='application/json',
            data=json.dumps({
                'url': 'test',
            }),
        )

    assert response.status_code == 400
    assert json.loads(response.data) == {u'message': u'the url format is invalid'}


def test_shorten_url_returns_400_when_url_over_2000_chars(app):
    with app.test_client() as c:
        response = c.post(
            '/shorten_url',
            content_type='application/json',
            data=json.dumps({
                'url': 'http://test.com?foo=' + 'bar' * 2000,
            }),
        )

    assert response.status_code == 400
    assert json.loads(response.data) == {u'message': u'the url is too long - maximum is 2000 characters'}


def test_shorten_url_returns_201_when_ok(app):
    with app.test_client() as c:
        response = c.post(
            '/shorten_url',
            content_type='application/json',
            data=json.dumps({
                'url': 'http://test.com?foo=bar',
            }),
        )

    assert response.status_code == 201

    url = Url.query.filter_by(url="http://test.com?foo=bar").all()
    assert url


def test_get_url_returns_404_when_not_found(app):
    with app.test_client() as c:
        response = c.get('/foo')

    assert response.status_code == 404


def test_get_url_redirects(app):
    with app.test_client() as c:
        response = c.post(
            '/shorten_url',
            content_type='application/json',
            data=json.dumps({
                'url': 'http://test.com?bar=baz',
            }),
        )
        assert response.status_code == 201

        short_url = json.loads(response.data)

        response = c.get(short_url['shortened_url'])

        assert response.status_code == 302
        assert response.location == 'http://test.com?bar=baz'


def test_get_url_redirects_gets_cached(app):
    with app.test_client() as c:
        response = c.post(
            '/shorten_url',
            content_type='application/json',
            data=json.dumps({
                'url': 'http://cacheme.com',
            }),
        )
        assert response.status_code == 201

        short_url = json.loads(response.data)['shortened_url']

        url_hash = short_url.split('/')[-1]

        assert not cache.get(url_hash)

        response = c.get(short_url)

        assert cache.get(url_hash) == 'http://cacheme.com'
