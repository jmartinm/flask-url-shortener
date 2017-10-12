"""URL Shortening service views."""

from flask import abort, request, redirect, jsonify, url_for

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError

from .utils import is_url_valid, integer_to_base62, base62_to_integer
from .models import Url
from .app import application, cache, db

MAX_RETRIES = 10
"""Used for concurrent situations where a URL is not found
when querying the DB, but it is present on insert, meaning
that another process inserted it between the two operations.
"""


@application.route('/shorten_url', methods=['POST'])
def shorten_url():
    """Handles requests from the user with the format

    {
        "url": "www.helloworld.com"
    }

    and returns short URL.
    """
    data = request.json

    if not data:
        return jsonify({
            'message': 'no valid JSON data was received'
        }), 400

    if 'url' not in data:
        return jsonify({
            'message': 'url key is missing from POST data'
        }), 400

    url = request.json['url']
    if not url.startswith('http://'):
        url = 'http://{}'.format(url)

    if not is_url_valid(url):
        return jsonify({
            'message': 'the url format is invalid'
        }), 400

    if len(url) > 2000:
        return jsonify({
            'message': 'the url is too long - maximum is 2000 characters'
        }), 400

    retries = 0
    while retries < MAX_RETRIES:
        try:
            full_url = Url.query.filter_by(url=url).one()
            break
        except NoResultFound:
            full_url = Url(url=url)
            db.session.add(full_url)
            try:
                db.session.commit()
            except IntegrityError:
                retries += 1
            else:
                break

    if retries == MAX_RETRIES:
        # The URL could not be created
        return jsonify({
            'message': 'there was an error processing the request - please retry'
        }), 500

    base62_string = integer_to_base62(full_url.id)

    return jsonify({
        "shortened_url": url_for('get_url', url_hash=base62_string, _external=True)
    }), 201


@application.route('/<url_hash>', methods=['GET'])
def get_url(url_hash):
    """Get a full URL from a short url.

    First tries to find an occurrence in the cache.

    If that fails, make a request in the database.
    """
    url = cache.get(url_hash)
    if url:
        return redirect(url)

    key = base62_to_integer(url_hash)
    try:
        url = Url.query.filter_by(id=key).one().url
        cache.set(url_hash, url)
        return redirect(url)
    except NoResultFound:
        abort(404)
