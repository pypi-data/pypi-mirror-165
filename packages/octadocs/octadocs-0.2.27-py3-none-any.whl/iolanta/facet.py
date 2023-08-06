from dataclasses import dataclass
from functools import cached_property
from typing import Optional, Union

from ldflex import LDFlex
from octadocs.octiron import Octiron
from rdflib.term import Node, URIRef, BNode


@dataclass
class Facet:
    """Base facet class."""

    iri: Node
    octiron: Octiron
    environment: Optional[URIRef] = None

    @property
    def ldflex(self) -> LDFlex:
        """Extract LDFLex instance."""
        return self.octiron.ldflex

    @cached_property
    def uriref(self) -> Union[URIRef, BNode]:
        """Format as URIRef."""
        if isinstance(self.iri, BNode):
            return self.iri

        return URIRef(self.iri)

    def query(self, query_text: str, **kwargs):
        """SPARQL query."""
        return self.ldflex.query(
            query_text=query_text,
            **kwargs,
        )

    def render(self):
        """Render the facet."""
        raise NotImplementedError()

    @property
    def language(self):
        return self.octiron.language

    def __str__(self):
        """Render."""
        return str(self.render())
