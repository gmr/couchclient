# coding=utf-8
"""
test_client.py

"""
__author__ = 'Gavin M. Roy'
__email__ = 'gmr@myyearbook.com'
__since__ = '2012-01-31'

import unittest

import couchclient

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


class CouchClientTests(unittest.TestCase):

    def setUp(self):
        self._client = couchclient.CouchDB(**_HTTP_SERVER)

    def test_http_base_url(self):
        expectation = 'http://%(host)s:%(port)s/%(database)s' % _HTTP_SERVER
        self.assertEqual(self._client._base_url, expectation)

    def test_https_base_url(self):
        expectation = 'https://%(host)s:%(port)s/%(database)s' % _HTTPS_SERVER
        client = couchclient.CouchDB(**_HTTPS_SERVER)
        self.assertEqual(client._base_url, expectation)

    def test_document_url(self):
        test = _HTTP_SERVER.copy()
        test['doc'] = 'test_document'
        expectation = 'http://%(host)s:%(port)s/%(database)s/%(doc)s' % test
        self.assertEqual(self._client._document_url(test['doc']), expectation)

    def test_quote(self):
        client = couchclient.CouchDB(**_HTTP_SERVER)
        value = '/hi/there/test'
        expectation = '%2Fhi%2Fthere%2Ftest'
        self.assertEqual(client._quote(value), expectation)

    def test_deunicode(self):
        value = {u'exchange': u'generate_email',
                 u'vhost': u'messaging',
                 u'host': u'rabbit19',
                 u'user': u'rejected',
                 u'pass': u'rabbitmq',
                 u'port': 5672}
        expectation = {u'exchange': 'generate_email',
                       u'vhost': 'messaging',
                       u'host': 'rabbit19',
                       u'user': 'rejected',
                       u'pass': 'rabbitmq',
                       u'port': 5672}
        self._client._deunicode(value)
        self.assertDictEqual(value, expectation)

    def test_deunicode_complex_with_unicode(self):
        value = {
            u"en-US": {
                u"delivery_reason": {
                    u"html_part": u"You have received this email from",
                    u"text_part": u"You have received this email from"
                }
            },
            u"es-ES": {
                u"delivery_reason": {
                    u"html_part": u"Has recibido este correo electrónico",
                    u"text_part": u"Has recibido este correo electrónico"
                }
            },
            u"other": {
                u"values": [{u"delivery_reason": {
                                u"html_part": u"You have received email from",
                                u"text_part": u"You have received email from"
                            }},
                            {u"delivery_reason": {
                                u"html_part": u"Has recibido este electrónico",
                                u"text_part": u"Has recibido este electrónico"
                            }}]
                }
        }
        expectation = {
            u"en-US": {
                u"delivery_reason": {
                    u"html_part": "You have received this email from",
                    u"text_part": "You have received this email from"
                }
            },
            u"es-ES": {
                u"delivery_reason": {
                    u"html_part": u"Has recibido este correo electrónico",
                    u"text_part": u"Has recibido este correo electrónico"
                }
            },
            u"other": {
                u"values": [{u"delivery_reason": {
                    "html_part": u"You have received email from",
                    "text_part": u"You have received email from"
                }},
                {u"delivery_reason": {
                    u"html_part": u"Has recibido este electrónico",
                    u"text_part": u"Has recibido este electrónico"
                }}]
            }
        }
        self._client._deunicode(value)
        self.assertDictEqual(value, expectation)
