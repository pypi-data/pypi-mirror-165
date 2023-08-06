from dataclasses import dataclass
from typing import Dict, Iterable, Optional

from iolanta.loaders.base import Loader, PyLDOptions, PyLDResponse
from iolanta.models import LDDocument, Quad
from rdflib import URIRef
from urlpath import URL


@dataclass(frozen=True)
class SchemeChoiceLoader(Loader):
    """Try to load a file via several loaders."""

    loader_by_scheme: Dict[str, Loader]

    def __call__(self, url: str, options: PyLDOptions) -> PyLDResponse:
        """Compile document for PyLD."""
        return {
            'document': self.as_jsonld_document(
                url=URL(url),
                iri=url,
            ),
            'contextUrl': None,
        }

    def resolve_loader_by_url(self, url: URL):
        """Find loader instance by URL."""
        try:
            return self.loader_by_scheme[url.scheme]
        except KeyError:
            raise ValueError(f'Cannot find a loader for URL: {url}')

    def as_jsonld_document(
        self,
        url: URL,
        iri: Optional[URIRef] = None,
    ) -> LDDocument:
        """Represent a file as a JSON-LD document."""
        return self.resolve_loader_by_url(
            url=url,
        ).as_jsonld_document(
            url=url,
            iri=iri,
        )

    def as_quad_stream(
        self,
        url: str,
        iri: Optional[URIRef],
        root_loader: Optional[Loader] = None,
    ) -> Iterable[Quad]:
        """Convert data into a stream of RDF quads."""
        return self.resolve_loader_by_url(
            url=url,
        ).as_quad_stream(
            url=url,
            iri=iri,
            root_loader=root_loader or self,
        )
