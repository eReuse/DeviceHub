from setuptools import setup, find_packages

setup(
    name='eReuse-DeviceHub',
    version='0.4',
    packages=find_packages(exclude=('contrib', 'docs', 'scripts')),
    url='https://github.com/eReuse/DeviceHub',
    license='AGPLv3 License',
    author='eReuse.org team',
    author_email='x.bustamante@ereuse.org',
    description='DeviceHub is a system to manage devices focused in reusing them. ',
    # Updated in 2017-07-29
    install_requires=[
        'inflection>=0.3.1',
        'eve>=0.6.3,<0.8',
        'flask>=0.11'
        'passlib>=1.6.5,<2.0',
        'validators>=0.10,<0.20',
        'requests>=2.9.1,<3.0',
        'python-gnupg>=0.3.8,<0.4',  # To use gnupg, install gpg2
        'flask-caching',
        'python-gnupg',
        'iso3166',
        'flask-excel>=0.0.7,<0.0.8',
        'pyexcel-ods',
        'pyexcel-xlsx',
        'pydash>=3.4,<4',
        'sortedcontainers>=1.5.7,<1.6',
        'geojson_utils',
        'geojson>=1.3.4,<1.4',
        'geoip2>=2.4.2,<3',
        'flask-cors>=3.0.2,<4',
        'shortid>=0.1.2,<0.2',
        'beautifulsoup4>=4.6,<5',
        'wikipedia>=1.4,<2'
    ],
    keywords='eReuse.org DeviceHub devices devicehub reuse recycle it asset management',
    # http://setuptools.readthedocs.io/en/latest/setuptools.html#declaring-extras-optional-features-with-their-own-dependencies
    extras_require={
        'docs': [
            'sphinx>=1.4.7',
            'sphinxcontrib-httpdomain>=1.5'
        ]
    },
    # Use `python setup.py test` to run the tests
    # http://setuptools.readthedocs.io/en/latest/setuptools.html#test-build-package-and-run-a-unittest-suite
    test_suite='ereuse_devicehub.tests',
    tests_require=[
        'assertpy'
    ],
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Manufacturing',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Office/Business',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content'
    ]
)
