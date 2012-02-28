from setuptools import setup

setup(name='couchclient',
      version='1.1.1',
      description=('Light-weight read-only CouchDB client for loading '
                   'documents and views'),
      maintainer='Gavin M. Roy',
      maintainer_email='gmr@myyearbook.com',
      url='http://github.com/gmr/couchclient',
      install_requires=['requests', 'simplejson'],
      tests_require=['mock'],
      py_modules = ['couchclient'],
      classifiers=[
                'Development Status :: 4 - Beta',
                'Intended Audience :: Developers',
                'Programming Language :: Python :: 2.5',
                'Programming Language :: Python :: 2.6',
                'Programming Language :: Python :: 2.7',
                'Topic :: Internet :: WWW/HTTP',
                'Topic :: Software Development :: Libraries',
                'Topic :: Software Development :: Libraries :: Python Modules',
                'License :: OSI Approved :: BSD License'],
      zip_safe=True)
