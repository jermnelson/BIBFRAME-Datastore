__author__ = "Jeremy Nelson"

from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import re
import sys
import subprocess



CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = os.path.abspath(os.path.dirname(CURRENT_DIR))
if os.path.exists(os.path.join(CURRENT_DIR, "VERSION")):
    version_filepath = os.path.join(CURRENT_DIR, "VERSION")
if os.path.exists(os.path.join(BASE_DIR, "VERSION")):
    version_filepath = os.path.join(BASE_DIR, "VERSION")
with open(version_filepath) as version:
    __version__ = version.read().strip()



class BIBFRAMEDatastoreInstall(install):
    JAVA_CHECK = re.compile(r"java version \"(.+)\"")

    def __check_java__(self):
        """Method checks for a Java 7+ JVM to run other dependencies"""
        raw_output = subprocess.getoutput("java -version") 
        result = BIBFRAMEDatastoreInstall.JAVA_CHECK.search(raw_output)
        if result is not None:
            version = result.groups()[0].split(".")
            if int(version[1]) >= 7:
                return True
        return False

    def __install_dependency__(self, **kwargs):
        pass

    def run(self):
        install.run(self)
        if not self.__check_java__():
            raise ValueError("Missing Java or Java version < 7")
        
        

setup(
    name='bibframe_datastore',
    author=__author__,
    author_email='jermnelson@gmail.com',
    cmdclass={'install': BIBFRAMEDatastoreInstall},
    description='BIBFRAME Datastore Installation',
    url='https://github.com/jermnelson/bibframe-datastore',
    install_requires=[
        'elasticsearch',
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
    packages = find_packages(exclude=['repository', 
                                      'search', 
                                      'triplestore',
                                      'tests']),
#     packages=['app',
#              'semantic_server',
#              'semantic_server.analytics',
#              'semantic_server.analytics.resources',
#              'semantic_server.analytics.utilities',
#              'semantic_server.repository.resources',
#              'semantic_server.repository.utilities',
#              'semantic_server.repository.utilities.migrating',
#              ],
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
      
