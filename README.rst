============================================
README for Bibliographic Framework Datastore
============================================

Redis Bibliographic Framework Datastore
---------------------------------------
The Redis Bibliographic Framework Datastore is based upon the current 
work being done by the Library of Congress's Bibliographic Framework
Transition Initiative Forum as presented by Sally McCallum in this
PowerPoint presentation at 
http://igelu.org/wp-content/uploads/2012/09/IGeLU-sally-McCallum.pptx.

This datastore used their preliminary high level model with four core
classes that borrows a lot from RDA and FRBR. They effectively collapse
the FRBR Work and Expression into a *Work* class and the FRBR Manifestation
and Items into an "Instance" class. The *Authority* class is made up of the
FRBR Person, Place, Topics, and Corporate Bodies. The last class is the
*Annotation* class that is made up of assertions about the other core classes
including related resources to the Work (reviews, abstract, etc.), Instance
(book cover images, web site opening page, etc.), Name authority 
(creator biographical information), and administrative metadata.


+------------------+---------------------+------+----------------------+
| Entity Model     | conf filename       | port | dbfilename           |
+------------------+---------------------+------+----------------------+
| Work             | work.conf           | 6380 | works.rdb            |
+------------------+---------------------+------+----------------------+
| Instance         | instance.conf       | 6381 | instances.rdb        |
+------------------+---------------------+------+----------------------+
| Authority        | authority.conf      | 6382 | authorities.rdb      | 
+------------------+---------------------+------+----------------------+
| Annotation       | annotation.conf     | 6383 | annotations.rdb      |
+------------------+---------------------+------+----------------------+
| Test             | test.conf           | 6385 | tests.rdb            | 
+------------------+---------------------+------+----------------------+
| Operation        | operational.conf    | 6379 | operations.rdb       |
+------------------+---------------------+------+----------------------+

