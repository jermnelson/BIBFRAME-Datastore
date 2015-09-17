__author__ = "Jeremy Nelson"

import hashlib
import pymarc
import rdflib
import redis
import socket
from .semantic_server.repository.utilities.ingesters import SimpleIngester, default_graph

AUTH_ACCESS_POINT_QUERY = """SELECT DISTINCT ?subject ?access_pt ?type
WHERE {
  ?subject <http://bibframe.org/vocab/authorizedAccessPoint> ?access_pt .
  ?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?type .
} LIMIT 10
"""

RDF_TYPE_DIGEST = hashlib.sha1(str(rdflib.RDF.type).encode()).hexdigest()

def dedup_bibframe(graph, cache_datastore):
    query = graph.query(AUTH_ACCESS_POINT_QUERY)
    
    for row in query:
        subject = row[0]
        access_point = row[1]
        bf_class = row[2]
        access_point_digest = hashlib.sha1(str(access_point).encode()).hexdigest()
        bf_class_digest = hashlib.sha1(str(bf_class_digest).encode()).hexdigest()
        pattern = "*:{}:{}".format(BF_AUTH_PT_DIGEST, access_point_digest)
        existing_subjects = cache_datastore.keys(pattern)
        if len(existing_subjects) > 0:
            subject_digest = existing_subjects[0].decode().split(":")[0]
            # Test if this subject's class exists, if not skip this lookup
            if not cache_datastore.exists("{}:{}:{}".format(
                subject_digest,
                RDF_TYPE_DIGEST,
                bf_class_digest):
                continue
            subject_iri = cache_datastore.get(subject_digest)
            new_subject = rdflib.URIRef(subject_iri.decode())
            for pred, obj in graph.predicate_objects(subject=subject):
                graph.add((new_subject, pred, obj))
                graph.remove((subject, pred, obj))
    return graph


class MARC2BibframeIngester(SimpleIngester):

    def __init__(self, **kwargs):
        super(MARC2BibframeIngester, self).__init__(
            fedora_rest_url = kwargs.get(
                'fedora_rest_url',
                'http://localhost:8080/fedora/rest'))
        self.bf_socket_host = kwargs.get('bf_socket_host',
                                         '0.0.0.0')
        self.bf_socket_port = kwargs.get('bf_socket_port',
                                         8089)
        self.cache_datastore = kwargs.get('cache_datastore',
                                          redis.StrictRedis())

    def __xquery_socket__(self, raw_xml):
        """Function takes raw_xml and converts to BIBFRAME RDF

        Args:
           raw_xml -- Raw XML 
        """
        xquery_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        xquery_server.connect((self.bf_socket_host, self.bf_socket_port))
        xquery_server.sendall(raw_xml + b'\n')
        rdf_xml = b''
        while 1:
            data = xquery_server.recv(1024)
            if not data:
                break
            rdf_xml += data
        xquery_server.close()
        bf_graph = default_graph()
        bf_graph.parse(data=rdf_xml.decode(), format='xml')
        return bf_graph

    def ingest(self, marc_record):
        sparql = """SELECT DISTINCT ?subject WHERE { ?subject ?pred ?obj . }"""
        bf_graph = self.__xquery_socket__(
            pymarc.record_to_xml(marc_record, namespace=True))
        self.deduplicate(
        for row in bf_graph.query(sparql):
            original_subject = row[0]
            subject_graph = default_graph()
            for predicate, object_ in bf_graph.predicate_objects(
                subject=original_subject):
                subject_graph.add((original_subject, predicate, object_))
            super(MARC2BibframeIngester, self).ingest(subject_graph)
