from setuptools import setup, find_packages

setup(
    name='DeviceHub',
    version='0.1',
    packages=find_packages(),
    url='https://github.com/eReuse/DeviceHub',
    license='AGPLv3 License',
    author='eReuse team',
    author_email='x.bustamante@ereuse.org',
    description='The DeviceHub is a Device Management System (DMS) created under the project eReuse. Its purpose is to '
                'offer a way for donors and receivers to efficiently manage the reuse process ensuring final recycling.',
    install_requires=[
        'inflection',
        'eve',  # Which has a bug, for now... todo try 0.6.2 when stable
        'passlib',
        'validators'
    ],
    include_package_data=True,
    long_description="""
        Credits:
            Icons made by <a href="http://www.freepik.com" title="Freepik">Freepik</a> from <a href="http://www.flaticon.com" title="Flaticon">www.flaticon.com</a> is licensed by <a href="http://creativecommons.org/licenses/by/3.0/" title="Creative Commons BY 3.0">CC BY 3.0</a>
    """
)
