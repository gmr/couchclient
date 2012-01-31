couchclient
===========

A light-weight CouchDB client for read-only requests of documents and views.

Examples
--------

    import couchclient
    config = couchclient.CouchDB('config.scs.myyearbook.com', 80,
                                 'com_myyearbook_messaging')
    seedlist = config.get_document('seedlist')

    config = couchclient.CouchDB('config.scs.myyearbook.com', 80,
                                 'com_myyearbook_messaging_messages')
    messages = config.get_view('status', 'messages')
    print messages

API
---

    class CouchDB(__builtin__.object)
     |  The CouchDB object creates a light-weight read-only client for CouchDB
     |  for retrieving documents and views.
     |
     |  Methods defined here:
     |
     |  __init__(self, host, port, database)
     |      Create a new configuration object for the given service and domain
     |      name.
     |
     |      :param str host: The FQDN needed to make requests to the CouchDB server
     |      :param str port: The port to query CouchDB on
     |      :param str database: The database name for CouchDB requests
     |
     |  get_document(self, document_id)
     |      Retrieve the document from the CouchDB server.
     |
     |      :param str document_id: The document id to fetch
     |      :returns: dict
     |      :raises: DocumentNotFound
     |      :raises: DocumentRetrievalFailure
     |
     |  get_view(self, document_id, view_name)
     |      Retrieve the view rows from the CouchDB server returning a dictionary
     |      of key value pairs as taken from the view rows keyed on the row key.
     |
     |      :param str document_id: The document_id with views
     |      :param str view_name: The name of the view in the document
     |      :returns: dict
     |      :raises: DocumentNotFound
     |      :raises: DocumentRetrievalFailure
     |
     |  strip_couch_attributes(self)
     |      Enable the stripping of CouchDB attributes (_id, _rev) on document
     |      retrieval.
     |
     |  strip_couch_attributes_off(self)
     |      Disable the stripping of CouchDB attributes (_id, _rev) on document
     |      retrieval.

    class DocumentNotFound(exceptions.EnvironmentError)
     |  # Define exceptions that may be raised
     |
     |  Method resolution order:
     |      DocumentNotFound
     |      exceptions.EnvironmentError
     |      exceptions.StandardError
     |      exceptions.Exception
     |      exceptions.BaseException
     |      __builtin__.object
     |       |
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from exceptions.EnvironmentError:
     |
     |  errno
     |      exception errno
     |
     |  filename
     |      exception filename
     |
     |  strerror
     |      exception strerror
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from exceptions.BaseException:
     |
     |  __dict__
     |
     |  args
     |
     |  message

     class DocumentRetrievalFailure(exceptions.EnvironmentError)
      |  Raised when a document was not retrieved from the CouchDB Server
      |
      |  Method resolution order:
      |      DocumentRetrievalFailure
      |      exceptions.EnvironmentError
      |      exceptions.StandardError
      |      exceptions.Exception
      |      exceptions.BaseException
      |      __builtin__.object
      |
      |  ----------------------------------------------------------------------
      |  Data descriptors inherited from exceptions.EnvironmentError:
      |
      |  errno
      |      exception errno
      |
      |  filename
      |      exception filename
      |
      |  strerror
      |      exception strerror
      |
      |  ----------------------------------------------------------------------
      |  Data descriptors inherited from exceptions.BaseException:
      |
      |  __dict__
      |
      |  args
      |
      |  message

Requirements
------------
requests
simplejson
