"""
# Name:        marc
# Purpose:     MARC21 module includes helper classes and functions for using
#              MARC 21 with Fedora 4 and Elasticsearch
#
# Author:      Jeremy Nelson
#
# Created:     2014/11/07
# Copyright:   (c) Jeremy Nelson 2014, 2015
# Licence:     GPLv3
"""
__author__ = "Jeremy Nelson"

import falcon
import pymarc
import rdflib
import urllib.request
from catalog.helpers.bibframe import FCREPO
from flask_fedora_commons import build_prefixes, Repository
from elasticsearch import Elasticsearch


class RecordIngester(object):
    """Class takes a MARC21 or MARC XML file, ingests into Fedora 4 repository
    and into Elastic search"""

    def __init__(
            self,
            record,
            elastic_search=Elasticsearch(),
            repository=Repository()
            ):
        """Initializes RecordIngester class

        Args:
            record: A MARC21 or MARC XML file
            elastic_search: Elasticsearch instance, defaults to localhost
            repository: Flask Fedora Commons Repository instance,
                        defaults to localhost
        """
        self.elastic_search = elastic_search
        if not self.elastic_search.indices.exists('marc'):
            self.elastic_search.indices.create('marc')
        self.record = record
        self.repository = repository




    def dedup(self, ils='III'):
        if ils.startswith('III'):
            # III MARC specific sys number
            bib_number = self.record['907']['a'][1:-1]
        else:
            return
        if self.elastic_search is not None:
            existing_result = self.elastic_search.search(
                index='marc',
                body={
                    "query": { "match": { "rdfs:label": bib_number}},
                    "_source": ["rdfs:label", "owl:sameAs"]})
            if existing_result.get('hits').get('total') > 0:
                # Returns first id
                first_hit = existing_result['hits']['hits'][0]
                return first_hit['_source']['owl:sameAs']

    def index(self, marc_meta_url):
        marc_graph = rdflib.Graph().parse(marc_meta_url)
        marc_uri = rdflib.URIRef(marc_meta_url)
        bib_number = str(marc_graph.value(
            subject=marc_uri,
            predicate=rdflib.RDFS.label)
        )
        created_on = str(marc_graph.value(
            subject=marc_uri,
            predicate=FCREPO.created)
        )
        marc_uuid = str(marc_graph.value(
            subject=marc_uri,
            predicate=FCREPO.uuid)
        )
        marc_body = {
            "owl:sameAs": [marc_meta_url,],
            "rdfs:label": [bib_number,],
            "fcrepo:created": [created_on,],
            "fcrepo:uuid": [marc_uuid,]}
        self.elastic_search.index(
            index='marc',
            doc_type='marc21',
            id=marc_uuid,
            body=marc_body)

    def ingest(self, ils):
        existing_marc = self.dedup(ils)
        if existing_marc is not None:
            return existing_marc
        try:
            marc21 = self.record.as_marc()
        except UnicodeEncodeError:
            self.record.force_utf8 = True
            marc21 = self.record.as_marc()
        create_request = urllib.request.Request(
            '/'.join([self.repository.base_url, 'rest']),
            method='POST',
            data=marc21)
        result = urllib.request.urlopen(create_request)
        marc_uri = result.read().decode()
        marc_meta_uri = "/".join([marc_uri, "fcr:metadata"])
        # III specific BIB Number
        if ils.startswith("III"):
            bib_number = self.record['907']['a'][1:-1]

        else:
            # Use 001 as rdfs:label for MARC record
            bib_number = self.record['001'].data
        self.repository.insert(
            marc_meta_uri,
            'rdfs:label',
            bib_number)
        self.index(marc_meta_uri)
        return marc_uri

def main():
    pass

if __name__ == '__main__':
    main()
