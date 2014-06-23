
from setuptools import setup
from setuptools import find_packages

from mockernaut import __version__


setup(
    name='mockernaut',
    version=__version__,
    url='http://github.com/marrrvin/mockernaut/',
    author='Sergey Orlov',
    author_email='foobar@list.ru',
    description='Web service mocking library written in python',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask',
        'mysql-connector-python',
        'requests',
        'jsonschema'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
