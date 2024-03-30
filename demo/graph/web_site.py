from pyorient.ogm import declarative

Node = declarative.declarative_node()

class Website(Node):
    element_plural = "WebPages"
    url = "string"