__author__ = "Jeremy Nelson"

from setuptools import setup
import os

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = os.path.abspath(os.path.dirname(CURRENT_DIR))
if os.path.exists(os.path.join(CURRENT_DIR, "VERSION")):
    version_filepath = os.path.join(CURRENT_DIR, "VERSION")
if os.path.exists(os.path.join(BASE_DIR, "VERSION")):
    version_filepath = os.path.join(BASE_DIR, "VERSION")
with open(version_filepath) as version:
    __version__ = version.read().strip()

setup(
    name='bibframe_datastore',
    author=__author__,
    author_email='jermnelson@gmail.com',
    description='BIBFRAME Datastore Installation',
    url='https://github.com/jermnelson/bibframe-datastore',
    install_requires=[
        'falcon',
        'flask', 
        'rdflib',
        'requests',
    ],
    license='GPLv3',
    keywords=['bibframe',
              'libraries', 
              'linked-data', 
              'library of congress',
              'semantic web'],
    py_modules=['app'],
    version=__version__,
    packages=['.',
              'semantic_server',
              'semantic_server.analytics',
              'semantic_server.analytics.resources',
              'semantic_server.analytics.utilities',
              'semantic_server.repository.resources',
              'semantic_server.repository.utilities',
              'semantic_server.repository.utilities.migrating',
              'semantic_server.tests',
              'tests'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application']
)
      
