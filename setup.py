from setuptools import setup, find_packages

setup(
    name='eReuse-DeviceHub',
    version='0.1.1',
    packages=find_packages(exclude=('contrib', 'docs', 'scripts')),
    url='https://github.com/eReuse/DeviceHub',
    license='AGPLv3 License',
    author='eReuse.org team',
    author_email='x.bustamante@ereuse.org',
    description='DeviceHub is a system to manage devices focused in reusing them. ',
    install_requires=[
        'inflection>=0.3.1,<0.4',
        'eve>=0.6.3,<7.0',
        'passlib>=1.6.5,<2.0',
        'validators>=0.10,<0.20',
        'flask>=0.10,<0.11',
        'requests>=2.9.1,<3.0',
        'python-gnupg>=0.3.8,<0.4',  # To use gnupg, install gpg2
        'flask-cache>=0.13.1',
        'python-gnupg',
        'iso3166',
        'flask-excel',
        'pyexcel-ods',
        'pyexcel-xlsx',
        'pydash>=3.4,<4',
        'sortedcontainers>=1.5.7,<1.6',
        'geojson_utils',
        'geojson>=1.3.4,<1.4',
        'geoip2>=2.4.2,<2.5',
        'flask-cors>=3.0.2,<3.1',
        'shortid>=0.1.2,<0.2'
    ],
    keywords='eReuse.org DeviceHub devices devicehub reuse recycle it asset management',
    # http://setuptools.readthedocs.io/en/latest/setuptools.html#declaring-extras-optional-features-with-their-own-dependencies
    extras_require={
        'docs': [
            'sphinx>=1.4.7',
            'sphinxcontrib-httpdomain>=1.5'
        ]
    },
    # http://setuptools.readthedocs.io/en/latest/setuptools.html#test-build-package-and-run-a-unittest-suite
    test_suite='ereuse_devicehub.tests',
    test_require=[
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
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Office/Business',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content'
    ]
)
