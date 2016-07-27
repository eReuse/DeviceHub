from setuptools import setup, find_packages

setup(
    name='eReuse-DeviceHub',
    version='0.1',
    packages=find_packages(),
    url='https://github.com/eReuse/DeviceHub',
    license='AGPLv3 License',
    author='eReuse team',
    author_email='x.bustamante@ereuse.org',
    description='The DeviceHub is a Device Management System (DMS) created under the project eReuse. Its purpose is to '
                'offer a way for donors and receivers to efficiently manage the reuse process ensuring final recycling.',
    install_requires=[
        'inflection>=0.3.1,<0.4',
        'eve>=0.6.3,<7.0',
        'passlib>=1.6.5,<2.0',
        'validators>=0.10,<0.20',
        'requests>=2.9.1,<3.0',
        'python-gnupg>=0.3.8,<0.4',  # To use gnupg, install gpg2
        'flask-cache>=0.13.1',
        'assertpy',
        'python-gnupg',
        'iso3166'
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
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ]
)
