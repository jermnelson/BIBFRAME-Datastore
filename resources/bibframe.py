__author__ = "Jeremy Nelson"

import importlib
import rdflib
import sys

#semantic_server = importlib.import_module("../semantic-server")
#fedora = importlib.import_module(".repository.resources.fedora", "..semantic-server")
sys.path.append("../../semantic_server")


import semantic_server.repository.resources.fedora as fedora
from semantic_server.repository import BF, RDF

class Bibframe(fedora.Resource):

    def on_post(self, req, resp):
        rdf = req.get_param('rdf', None)
        if rdf is None:
            turtle_rdf = "PREFIX bf: <" + str(BF) + ">\n"
            turtle_rdf += "PREFIX rdf: <" + str(RDF) + ">\n"
##            turtle_rdf += "INSERT DATA {"
            turtle_rdf += "<> rdf:type bf:" + str(req.path[1:]) + " .\n"
            req._params['rdf'] = turtle_rdf
        super(Bibframe, self).on_post(req, resp)



def bibframe_duck_typing():
    def _get_or_add_class(name_uri):
        name = str(name_uri).split("/")[-1]
        if hasattr(sys.modules[__name__], name):
            return getattr(sys.modules[__name__], name)
        parent_uri = bf_ontology.value(
            subject=name_uri,
            predicate=rdflib.RDFS.subClassOf)
        if parent_uri:
            parent_class = _get_or_add_class(parent_uri)
        else:
            parent_class = Bibframe
        class_ = type(name, (parent_class,), {})
        setattr(
            sys.modules[__name__],
            name,
            class_)
        return class_
    bf_ontology = rdflib.Graph().parse('http://bibframe.org/vocab.rdf')
    class_sparql = """
    SELECT DISTINCT ?bf
    WHERE {
       ?bf <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2000/01/rdf-schema#Class> .
    }"""
    bf_classes = [row[0] for row in bf_ontology.query(class_sparql)]
    for class_ in bf_classes:
        class_name = str(class_).split("/")[-1]
        new_class = _get_or_add_class(class_)

bibframe_duck_typing()

