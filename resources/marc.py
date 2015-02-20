__author__ = "Jeremy Nelson"

import importlib
import pymarc
import rdflib

fedora = importlib.import_module(
    "..semantic-server.repository.resources.fedora")


class MARC(fedora.Resource):
    """MARC REST endpoint"""

    def __dedup__(self, record, ils):
        if ils.startswith('III'):
            # III MARC specific sys number
            bib_number = record['907']['a'][1:-1]
        # Default is the Record's 001 Control number
        else:
            bib_number = record['001'].data
        if self.search is not None:
            existing_result = self.elastic_search.search(
                index='marc',
                body={
                    "query": { "match": { "rdfs:label": bib_number}},
                    "_source": ["rdfs:label", "owl:sameAs"]})
            if existing_result.get('hits').get('total') > 0:
                # Returns first id
                first_hit = existing_result['hits']['hits'][0]
                return first_hit['_source']['owl:sameAs']

    def on_post(self, req, resp):
        record = req.get_param('record')
        ils = req.get_parm('ils')
        try:
            marc21 = record.as_marc()
        except UnicodeEncodeError:
            record.force_utf8 = True
            marc21 = record.as_marc()
        if self.__dedup__(record)
        req.set_param('binary', marc21)
        result = super(MARC, self).on_post(req, resp)

