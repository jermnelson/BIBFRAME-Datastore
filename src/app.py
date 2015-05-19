__author__ = "Jeremy Nelson"
__license__ = "GPLv3"


import os

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = os.path.abspath(os.path.dirname(CURRENT_DIR))
if os.path.exists(os.path.join(CURRENT_DIR, "VERSION")):
    version_filepath = os.path.join(CURRENT_DIR, "VERSION")
if os.path.exists(os.path.join(BASE_DIR, "VERSION")):
    version_filepath = os.path.join(BASE_DIR, "VERSION")

with open(version_filepath) as version:
    __version__ = version.read().strip()

import falcon
import importlib
import inspect
import json
import rdflib
import subprocess
import sys
from core.resources import bibframe
import semantic_server.app  as semantic_server

fedora_repo = None
elastic_search = None
global fuseki

for name, obj in inspect.getmembers(bibframe):
    if inspect.isclass(obj):
        semantic_server.api.add_route(
            "/{}".format(name),
            obj(semantic_server.config))
        semantic_server.api.add_route(
            "/{}".format(name) + "/{id}",
            obj(semantic_server.config))


def start_elastic_search(**kwargs):
    if sys.platform.startswith("win"):
        es_command = ["elasticsearch.bat"]
    else:
        es_command = ["elasticsearch"]
    return es_command

def start_fedora(**kwargs):
    repo_json_file = os.path.join(BASE_DIR, "repository", "repository.json")
    if not os.path.exists(repo_json_file):
        repo_json_file = os.path.join(CURRENT_DIR, "repository", "repository.json")
    java_command = [
        "java",
        "-jar",
        "-Dfcrepo.modeshape.configuration=file:/{}".format(repo_json_file)]
    if "memory" in kwargs:
        java_command.append("-Xmx{}".format(kwargs.get("memory")))
    java_command.append(
        kwargs.get("jar-file",
            "fcrepo-webapp-4.1.1-jetty-console.jar"))
    java_command.append("--headless")
    return java_command


def start_fedora_messenger(**kwargs):
    java_command = [
        "java",
        "-jar",
        kwargs.get("war-file",
            "fcrepo-message-consumer-webapp-4.1.1-jetty-console.jar"),
        "--headless",
        "--port",
        kwargs.get("port", "9090")
    ]
    return java_command

def start_fuseki(**kwargs):
    java_command = [
        "java",
        "-Xmx1200M",
        "-jar",
        "fuseki-server.jar",
    ]
    if kwargs.get('update', True):
        java_command.append("--update")
    java_command.append("--loc=store")
    java_command.append("/{}".format(kwargs.get('datastore', 'bf')))
    return java_command


def main():
    print("Running BIBFRAME Datastore")
    semantic_server.main()

class Services(object):

    def __init__(self):
        self.elastic_search, self.fedora_repo = None, None
        self.fedora_messenger, self.fuseki = None, None

    def __start_services__(self):
        os.chdir(os.path.join(BASE_DIR, "search", "bin"))
        self.elastic_search = subprocess.Popen(
            start_elastic_search())
        os.chdir(os.path.join(BASE_DIR, "triplestore"))
        self.fuseki = subprocess.Popen(
            start_fuseki())
        os.chdir(os.path.join(BASE_DIR, "repository"))
        self.fedora_repo = subprocess.Popen(
            start_fedora(memory='1G'))
        #self.fedora_messenger = subprocess.Popen(
        #    start_fedora_messenger())
      

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = json.dumps({ 'services': {
            "elastic-search": self.elastic_search.pid or None,
            "fedora4": self.fedora_repo.pid or None,
            "fuseki": self.fuseki.pid or None 
            }

            })

    def on_post(self, req, resp):
        if self.fedora_repo and (self.fuseki or self.elastic_search):
            raise falcon.HTTPForbidden(
                "Services Already Running",
                "Elastic Search, Fedora 4, and Fuseki already running")
        self.__start_services__()
        resp.status = falcon.HTTP_201
        resp.body = json.dumps({"services": {
            "elastic-search": {"pid": self.elastic_search.pid},
            "fedora4": {"pid": self.fedora_repo.pid},
         #   "fedora4-messenger": {"pid": self.fedora_messenger.pid},
            "fuseki": {"pid": self.fuseki.pid}}})

    def on_delete(self, req, resp):
        if not self.elastic_search and not self.fedora_repo:
            raise falcon.HTTPServiceUnavailable(
                "Cannot Delete Services",
                "Elastic Search and Fedora 4 are not running",
                300)
        #! This doesn't work for Elastic Search because running from
##        #! elasticsearch.bat and not running the program directly with
        #! JAVA.
        for service in [self.elastic_search, 
                        self.fedora_repo,
                        self.fuseki]:
            if service is not None:
                service.kill()
                
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(
            {"message": "Services stopped"})




# Add Services REST API
semantic_server.api.add_route("/services", Services())



##semantic_server.api.add_route("/Work")
##semantic_server.api.add_route("/Annotation")
##semantic_server.api.add_route("/Authority")
##semantic_server.api.add_route("/Instance")

if __name__ == "__main__":
   main() 
