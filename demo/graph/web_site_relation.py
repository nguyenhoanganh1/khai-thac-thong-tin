from pyorient.ogm import declarative

from page_rank.models import Website

RelationShip = declarative.declarative_relationship()

class WebSiteRelation(RelationShip):
    label = "references"
    out_element = Website
    in_element = "WebPage"
