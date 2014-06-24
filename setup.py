
from setuptools import setup
from setuptools import find_packages

from mockernaut import __version__


with open('README.md') as fp:
    description = fp.readline()

with open('requirements.txt') as fp:
    requirements = [req.strip() for req in fp.readlines() if not req.startswith('--')]


setup(
    name='mockernaut',
    description=description,
    version=__version__,
    url='http://github.com/marrrvin/mockernaut/',
    author='Sergey Orlov',
    author_email='foobar@list.ru',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=requirements,
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
