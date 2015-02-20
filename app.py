__author__ = "Jeremy Nelson"
__license__ = "GPLv3"


import os
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
with open(os.path.join(BASE_DIR, "VERSION")) as version:
    __version__ = version.read().strip()

import falcon
import importlib
import json
import rdflib
import subprocess
import sys

semantic_server = importlib.import_module("semantic-server.app", None)

fedora_repo = None
elastic_search = None
global fuseki

bf_ontology = rdflib.Graph().parse('http://bibframe.org/vocab.rdf')
sparql = """
SELECT DISTINCT ?bf
WHERE {
   ?bf <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2000/01/rdf-schema#Class> .
}"""

bf_classes = [row[0] for row in bf_ontology.query(sparql)]

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
    java_command.append(
        kwargs.get("war-file",
            "fcrepo-webapp-4.1.0-jetty-console.war"))
    java_command.append("--headless")
    return java_command

def start_fedora_messenger(**kwargs):
    java_command = [
        "java",
        "-jar"
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
        self.fuseki = None

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = json.dumps({ 'services': {
            "elastic-search": None,
            "fedora4": None,
            "fuseki": None

            }

            })

    def on_post(self, req, resp):
        if self.fedora_repo and (self.fuseki or self.elastic_search):
            raise falcon.HTTPForbidden(
                "Services Already Running",
                "Elastic Search, Fedora 4, and Fuseki already running")
        os.chdir(os.path.join(BASE_DIR, "repository"))
        self.fedora_repo = subprocess.Popen(
            start_fedora())
        os.chdir(os.path.join(BASE_DIR, "search", "bin"))
        self.elastic_search = subprocess.Popen(
            start_elastic_search())
        os.chdir(os.path.join(BASE_DIR, "triplestore"))
        self.fuseki = subprocess.Popen(
            start_fuseki())
        resp.status = falcon.HTTP_201
        resp.body = json.dumps({"services": {
            "elastic-search": {"pid": self.elastic_search.pid},
            "fedora4": {"pid": self.fedora_repo.pid},
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
        self.elastic_search.kill()
        self.fedora_repo.kill()
        self.fuseki.kill()
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
