import pytest

from url_shortener.utils import is_url_valid, base62_to_integer, integer_to_base62


@pytest.mark.parametrize('url', [
    'http://foo.com/blah_blah'
    'http://foo.com/blah_blah/',
    'http://foo.com/blah_blah_(wikipedia)',
    'http://foo.com/blah_blah_(wikipedia)_(again)',
    'http://www.example.com/wpstyle/?p=364'
])
def test_valid_urls(url):
    assert is_url_valid(url)


@pytest.mark.parametrize('url', [
    'http://',
    'http://.',
    'http://-a.b.co',
    'http://a.b-.co',
    'http://.www.foo.bar./'
])
def test_invalid_urls(url):
    assert not is_url_valid(url)


def test_integer_to_base62():
    base62_string = integer_to_base62(12345)

    assert base62_string == '3D7'
    
    integer = base62_to_integer(base62_string)

    assert integer == 12345
