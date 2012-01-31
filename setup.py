from setuptools import setup

setup(name='couchclient',
      version="1.0.0",
      description="Light-weight CouchDB client for loading documents and views",
      maintainer="Gavin M. Roy",
      maintainer_email="gmr@myyearbook.com",
      url="http://github.com/Python/couchclient",
      install_requires=['requests', 'simplejson', 'mock'],
      packages = ['couchclient'],
      zip_safe=True)
