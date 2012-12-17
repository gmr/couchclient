"""
CouchDB Client

"""
__author__ = 'Gavin M. Roy'
__email__ = 'gmr@meetme.com'
__since__ = '2012-01-30'
__version__ = '1.4.3'

import logging
import requests
import urllib

LOGGER = logging.getLogger(__name__)


class CouchDB(object):
    """The CouchDB object creates a light-weight read-only client for CouchDB
    for retrieving documents and views.

    """
    _COUCHDB_ATTRIBUTES = ['_id', '_rev']
    _SCHEMES = {80: 'http', 443: 'https', 5984: 'http', 6984: 'https'}

    def __init__(self, host, port, database, strip_attributes=True):
        """Create a new configuration object for the given service and domain
        name.

        :param str host: The FQDN needed to make requests to the CouchDB server
        :param int port: The port to query CouchDB on
        :param str database: The database name for CouchDB requests
        :param bool strip_attributes: Remove _id and _rev from result

        """
        # Get the server to use from DNSConfig
        self._server = {'host': host, 'port': port}

        # Set the database name
        self._database = database

        # Set the strip attribute
        self._strip_attributes = strip_attributes

    @property
    def _base_url(self):
        """Return the base URL for the given server and service.

        :returns str: The base URL for the couchdb configuration server

        """
        return "%s://%s:%s/%s" % (CouchDB._SCHEMES[self._server['port']],
                                  self._server['host'],
                                  self._server['port'],
                                  self._database)
    def _deunicode(self, value):
        """Iterate the keys in value removing unicode values if possible.

        :param dict value: The dict to iterate
        :rtype: dict

        """
        LOGGER.debug('Received %r', value)
        new_value = dict()
        for key in value:
            new_value[key] = self._process_node(value[key])
        LOGGER.debug('Returning: %r', new_value)
        return new_value

    def _process_node(self, node):
        """Process a node to strip unicode from it if possible.

        :param unicode,list,dict,any node: The value to process
        :rtype: any

        """
        LOGGER.debug('Processing %r', node)
        if isinstance(node, unicode):
            try:
                return str(node.decode('ascii'))
            except UnicodeEncodeError:
                LOGGER.debug('Not changing unicode string: %r', node)
                return node

        elif isinstance(node, dict):
            new = dict()
            for key in node:
                new[key] = self._process_node(node[key])
            return new

        elif isinstance(node, list):
            new = list()
            for item in node:
                new.append(self._process_node(item))
            return new

        return node

    def _document_url(self, document_id):
        """Return the document URL for the given document_id

        :param str document_id: The document id for the URL
        :returns str: The document URL

        """
        return '%s/%s' % (self._base_url, self._quote(document_id))

    def _error(self, response):
        """Raise the DocumentNotFound error, building an error message from
        the couchdb response.

        :param requests.Response response: CouchDB request response
        :raises: DocumentNotFound
        :raises: DocumentRetrievalFailure

        """
        document = response.json
        error_message = 'Error: %s, reason: %s' % (document['error'],
                                                   document['reason'])
        if response.status_code == 404:
            raise DocumentNotFound((response.status_code,
                                    error_message,
                                    response.request.url))
        else:
            raise DocumentRetrievalFailure((response.status_code,
                                            error_message,
                                            response.request.url))

    def _get_couchdb_value(self, url):
        """Make the request to the CouchDB server, look at the result and
        return the JSON decoded document if found.

        :param str url: The URL to request
        :returns dict: The document value
        :raises: DocumentNotFound
        :raises: DocumentRetrievalFailure

        """
        response = self._http_request(url)

        # If the status code is 200, it was a successful request
        if response.status_code == 200:
            return response.json()

        # Raise the error that we did not find the document
        self._error(response)

    def _http_request(self, url):
        """Make the request to the CouchDB server and return the result

        :param str url: The URL to request
        :returns str: The document value
        :raises: DocumentNotFound
        :raises: DocumentRetrievalFailure

        """
        LOGGER.debug('Making HTTP GET request to %s', url)
        return requests.get(url)

    def _quote(self, value):
        """Return a quoted value, escaping bits for CouchDB.

        :param str value: The value to quote
        :rtype: str

        """
        return urllib.quote(value, '')

    def _strip(self, document):
        """Remove the attributes specified in CouchDB._COUCHDB_ATTRIBUTES
        from the passed in dictionary value.

        :param dict document: The returned document

        """
        LOGGER.debug('Removing %r from %r',
                     CouchDB._COUCHDB_ATTRIBUTES, document)
        for attribute in CouchDB._COUCHDB_ATTRIBUTES:
            del document[attribute]

    def _view_data(self, document):
        """Returns the view data as a dictionary of values with the key being
        the row key.

        :param dict document: The view document response
        :returns dict: Processed view data

        """
        LOGGER.debug('Transforming %i rows', len(document['rows']))
        view_data = dict()
        for row in document['rows']:
            view_data[row['key']] = row['value']
        return view_data

    def _view_url(self, document_id, view_name):
        """Return the document URL for the given document_id and view name

        :param str document_id: The document id for the URL
        :param str view_name: The name of the view in the document
        :returns str: The document URL

        """
        return '%s/_design/%s/_view/%s' % (self._base_url,
                                           document_id,
                                           view_name)

    def get_document(self, document_id):
        """Retrieve the document from the CouchDB server.

        :param str document_id: The document id to fetch
        :rtype: dict
        :raises: DocumentNotFound
        :raises: DocumentRetrievalFailure

        """
        url = self._document_url(document_id)

        # Request the document
        document = self._deunicode(self._get_couchdb_value(url))

        if self._strip_attributes:
            self._strip(document)

        # Return the document
        return document

    def get_view(self, document_id, view_name):
        """Retrieve the view rows from the CouchDB server returning a dictionary
        of key value pairs as taken from the view rows keyed on the row key.

        :param str document_id: The document_id with views
        :param str view_name: The name of the view in the document
        :rtype: dict
        :raises: DocumentNotFound
        :raises: DocumentRetrievalFailure

        """
        url = self._view_url(document_id, view_name)

        # Request the document
        document = self._deunicode(self._get_couchdb_value(url))

        # Return the view data
        return self._view_data(document)


# Define exceptions that may be raised
class DocumentNotFound(EnvironmentError):
    """Raised when a document is not found on the CouchDB Server"""
    pass


class DocumentRetrievalFailure(EnvironmentError):
    """Raised when a document was not retrieved from the CouchDB Server"""
    pass
