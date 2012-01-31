"""
test_client.py

"""
__author__ = 'Gavin M. Roy'
__email__ = 'gmr@myyearbook.com'
__since__ = '2012-01-31'

import sys
sys.path.insert(0, '..')

import mock
import nose
import couchclient
import simplejson

_HTTP_SERVER = {'host': 'unittest.info',
                'port': 5984,
                'database': 'http_database'}

_HTTPS_SERVER = {'host': 'unittest.info',
                 'port': 6984,
                 'database': 'https_database'}

_404_ERROR = '{"error":"not_found","reason":"missing"}'
_500_ERROR = '{"error":"server_error","reason":"mocks arent servers"}'

_DOC_CONTENT = ('{"_id": "events","_rev": "5-23643498471dea9ebaec5808cceecc'
                '17","storage_type": "postgresql","storage_host": "pgproxy0'
                '2","storage_db": "email","storage_port": 6000,"storage_use'
                'r": "www"}')
_VIEW_CONTENT = ('{"total_rows":40,"offset":0,"rows":[{"id":"activation",'
                 '"key":"activation","value":{"id":174,"stream":"account",'
                 '"bundle_counts":{"en_US":{"development":1,"qa":0,"produ'
                 'ction":0}}}}]}')


def _mock_http_document_request(url):
    response = mock.Mock()
    response.status_code = 200
    response.request = mock.Mock()
    response.request.url = url
    response.content = _DOC_CONTENT
    return response


def _mock_http_view_request(url):
    response = mock.Mock()
    response.status_code = 200
    response.request = mock.Mock()
    response.request.url = url
    response.content = _VIEW_CONTENT
    return response


def _mock_http_404_request(url):
    response = mock.Mock()
    response.status_code = 404
    response.request = mock.Mock()
    response.request.url = url
    response.content = _404_ERROR
    return response


def _mock_http_500_request(url):
    response = mock.Mock()
    response.status_code = 500
    response.request = mock.Mock()
    response.request.url = url
    response.content = _500_ERROR
    return response


def test_http_base_url():
    expectation = 'http://%(host)s:%(port)s/%(database)s' % _HTTP_SERVER
    client = couchclient.CouchDB(**_HTTP_SERVER)
    assert client._base_url == expectation


def test_https_base_url():
    expectation = 'https://%(host)s:%(port)s/%(database)s' % _HTTPS_SERVER
    client = couchclient.CouchDB(**_HTTPS_SERVER)
    assert client._base_url == expectation


def test_document_url():
    test = _HTTP_SERVER.copy()
    test['doc'] = 'test_document'
    expectation = 'http://%(host)s:%(port)s/%(database)s/%(doc)s' % test
    client = couchclient.CouchDB(**_HTTP_SERVER)
    assert client._document_url(test['doc']) == expectation


@nose.tools.raises(couchclient.DocumentNotFound)
def test_404_error_response():
    test = _HTTP_SERVER.copy()
    test['doc'] = 'test_document'
    url = 'http://%(host)s:%(port)s/%(database)s/%(doc)s' % test
    response = _mock_http_404_request(url)
    client = couchclient.CouchDB(**_HTTP_SERVER)
    client._error(response)


@nose.tools.raises(couchclient.DocumentRetrievalFailure)
def test_500_error_response():
    test = _HTTP_SERVER.copy()
    test['doc'] = 'test_document'
    url = 'http://%(host)s:%(port)s/%(database)s/%(doc)s' % test
    response = _mock_http_500_request(url)
    client = couchclient.CouchDB(**_HTTP_SERVER)
    client._error(response)


@nose.tools.raises(couchclient.DocumentNotFound)
def test_404_get_couchdb_value():
    client = couchclient.CouchDB(**_HTTP_SERVER)
    client._http_request = _mock_http_404_request
    client._get_couchdb_value('abc')


@nose.tools.raises(couchclient.DocumentRetrievalFailure)
def test_500_get_couchdb_value():
    client = couchclient.CouchDB(**_HTTP_SERVER)
    client._http_request = _mock_http_500_request
    client._get_couchdb_value('abc')


def test_get_couchdb_value_document():
    expectation = simplejson.loads(_DOC_CONTENT)
    client = couchclient.CouchDB(**_HTTP_SERVER)
    client._http_request = _mock_http_document_request
    assert client._get_couchdb_value('abc') == expectation


def test_get_couchdb_value_view():
    expectation = simplejson.loads(_VIEW_CONTENT)
    client = couchclient.CouchDB(**_HTTP_SERVER)
    client._http_request = _mock_http_view_request
    assert client._get_couchdb_value('abc') == expectation


def test_get_document():
    expectation = simplejson.loads(_DOC_CONTENT)
    del expectation['_id']
    del expectation['_rev']
    client = couchclient.CouchDB(**_HTTP_SERVER)
    client._http_request = _mock_http_document_request
    assert client.get_document('abc') == expectation


def test_get_view():
    test = simplejson.loads(_VIEW_CONTENT)
    temp = test['rows'].pop(0)
    expectation = {temp['key']: temp['value']}
    client = couchclient.CouchDB(**_HTTP_SERVER)
    client._http_request = _mock_http_view_request
    assert client.get_view('abc', 'def') == expectation
