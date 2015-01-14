README for Bibliographic Framework Datastore
============================================

Redis Bibliographic Framework Datastore
---------------------------------------
The Redis Bibliographic Framework Datastore is based upon the current 
work being done by the Library of Congress's Bibliographic Framework
Transition Initiative Forum first introduced by Sally McCallum in this
PowerPoint presentation at 
http://igelu.org/wp-content/uploads/2012/09/IGeLU-sally-McCallum.pptx
and further defined by the following report, 
.

This datastore used their preliminary high level model with four core
classes that borrows a lot from RDA and FRBR. They effectively collapse
the FRBR Work and Expression into a *Creative Work* class and the FRBR Manifestation
and Items into an "Instance" class. The *Authority* class is made up of the
FRBR Person, Place, Topics, and Corporate Bodies. The last class is the
*Annotation* class that is made up of assertions about the other core classes
including related resources to the Creative Work (reviews, abstract, etc.), 
Instance
(book cover images, web site opening page, etc.), Name authority 
(creator biographical information), and administrative metadata.

This project contains the following Redis 2.6.1+ version rdb files for the following
collections:

1.  Colorado Alliance of Research Libraries random MARC21 records from union Prospector
    catalog. Filename - **prospector-random.rdb**

1.  Project Gutenberg RDF records. Filename - **project-gutenberg.rdb** 

