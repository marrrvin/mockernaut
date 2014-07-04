
from setuptools import setup
from setuptools import find_packages

from mockernaut import __version__


with open('README.rst') as fp:
    long_description = fp.readline()

with open('requirements.txt') as fp:
    requirements = [req.strip() for req in fp.readlines() if not req.startswith('--')]


setup(
    name='mockernaut',
    description='Web service mocking library written in python',
    long_description=long_description,
    version=__version__,
    url='http://github.com/marrrvin/mockernaut/',
    author='Sergey Orlov',
    author_email='foobar@list.ru',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'mockernaut': ['sql/*.sql', 'schema/*.json']
    },
    zip_safe=False,
    platforms='any',
    install_requires=requirements,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
