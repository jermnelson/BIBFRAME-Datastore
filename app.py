__author__ = "Jeremy Nelson"
__license__ = "GPLv3"


import os
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
with open(os.path.join(BASE_DIR, "VERSION")) as version:
    __version__ = version.read().strip()

import falcon
import importlib
import json
import subprocess
import sys

semantic_server = importlib.import_module("semantic-server.app", None)

fedora_repo = None
elastic_search = None
global fuseki

def start_elastic_search(**kwargs):
    if os.environ['OS'].startswith("Win"):
        es_command = ["elasticsearch.bat"]
    else:
        es_command = ["elasticsearch"]
    return es_command

def start_fedora(**kwargs):
    java_command = [
        "java",
        "-jar",
        "-Dfcrepo.modeshape.configuration=file:/{}".format(
            os.path.join(BASE_DIR, "repository", "repository.json"))]
    if "memory" in kwargs:
        java_command.append("-Xmx{}".format(kwargs.get("memory")))
    java_command.append("fcrepo-webapp-4.1.0-jetty-console.war")
##    java_command.append(os.path.join(
##        BASE_DIR,
##        "repository",
##        kwargs.get("jarfile", "fcrepo-webapp-4.1.0-jetty-console.war")))
    java_command.append("--headless")
    return java_command

def start_fedora_messenger(**kwargs):
    java_command = [
        "java",
        "-jar"
    ]

def start_fuseki(**kwargs):
    java_commands = []




def main():
    os.chdir(os.path.join(BASE_DIR, "repository"))
    fedora_process = subprocess.Popen(
        start_fedora())
    os.chdir(os.path.join(BASE_DIR, "search", "bin"))
    es_process = subprocess.Popen(
        start_elastic_search())
    print("Fedora Process pid={}".format(fedora_process.pid))
    print("Elastic search Process pid={}".format(es_process.pid))


class Services(object):

    def __init__(self):
        self.elastic_search, self.fedora_repo = None, None

    def on_post(self, req, resp):
        if self.elastic_search and self.fedora_repo:
            raise falcon.HTTPForbidden(
                "Services Already Running",
                "Elastic Search and Fedora 4 already running")
        os.chdir(os.path.join(BASE_DIR, "repository"))
        self.fedora_repo = subprocess.Popen(
            start_fedora())
        os.chdir(os.path.join(BASE_DIR, "search", "bin"))
        self.elastic_search = subprocess.Popen(
            start_elastic_search())
        resp.status = falcon.HTTP_200
        resp.body = json.dumps({"services": {
            "elastic-search": {"pid": self.elastic_search.pid},
            "fedora4": {"pid": self.fedora_repo.pid}}})

    def on_delete(self, req, resp):
        if not self.elastic_search and not self.fedora_repo:
            raise falcon.HTTPServiceUnavailable(
                "Cannot Delete Services",
                "Elastic Search and Fedora 4 are not running",
                300)
        #! This doesn't work for Elastic Search because running from
        #! elasticsearch.bat and not running the program directly with
        #! JAVA.
        self.elastic_search.kill()
        self.fedora_repo.kill()
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(
            {"message": "Fedora 4 and Elastic Search stopped"})




# Add Services REST API
semantic_server.api.add_route("/services", Services())


# Add BIBFRAME specific REST API
##semantic_server.api.add_route("/Work")
##semantic_server.api.add_route("/Annotation")
##semantic_server.api.add_route("/Authority")
##semantic_server.api.add_route("/Instance")

if __name__ == "__main__":
    semantic_server.main()
