__author__ = "Jeremy Nelson"

import rdflib
from .semantic_server.repository.search import GraphIndexer

class WorkInstanceIndexer(GraphIndexer):
    display_predicates = [
        # Both
        rdflib.RDFS.label
    ]
    id_predicates = [
       # Work Identifiers
       BF.classificationDdc,
       BF.classificationLcc,
       BF.classificationUdc,
       BF.isan,
       BF.issnL,
       BF.istc,
       BF.iswc,
       # Instance Identifiers
       BF.ansi
       BF.doi
       BF.ean
       BF.isbn
       BF.isbn10
       BF.isbn13
       BF.ismn
       BF.lccn
       BF.nban
       BF.nbn
       BF.sici
       BF.strn
       BF.upc
       # Both
       BF.local
    ]
    reference = [
       BF.creator
       BF.instanceOf
    ]

    def __init__(self, **kwargs):
        kwargs['id_sparql'] = WORK_INSTANCE_ID_QUERY
        super(WorkInstanceIndexer, self).__init__(**kwargs)
        


