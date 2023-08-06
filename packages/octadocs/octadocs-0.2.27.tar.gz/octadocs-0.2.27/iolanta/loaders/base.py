from abc import ABC
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Optional, TextIO, TypedDict

from iolanta.models import LDContext, LDDocument, Quad
from iolanta.namespaces import PYTHON
from rdflib import URIRef
from urlpath import URL

PyLDOptions = Dict[str, Any]

PyLDResponse = TypedDict('PyLDResponse', {
    'contentType': str,
    'contextUrl': Optional[str],
    'documentUrl': str,
    'document': LDDocument,
})


def term_for_python_class(cls: type) -> URIRef:
    """Construct term for Python class."""
    return PYTHON.term(f'{cls.__module__}.{cls.__qualname__}')


# noinspection TaskProblemsInspection
@dataclass(frozen=True)
class Loader(ABC):
    """
    Base class for loaders.

    Loader receives a URL (or a path) to certain location. It is responsible for
    reading data from that location and returning it as a stream of RDF quads.

    Usually, depending on the data format, Loader leverages Parsers for that
    purpose.
    """

    @classmethod
    def loader_class_iri(cls) -> URIRef:
        """Import path to the loader class."""
        return term_for_python_class(cls)

    def choose_parser_class(self, url: URL):
        """Find which parser class to use for this URL."""
        raise NotImplementedError(
            f'{self}.choose_parser_class() is not implemented.',
        )

    def as_jsonld_document(
        self,
        url: URL,
        iri: Optional[URIRef] = None,
    ) -> LDDocument:
        """Represent a file as a JSON-LD document."""
        raise NotImplementedError(
            f'{self}.as_jsonld_document() is not implemented.',
        )

    def as_file(self, url: URL) -> TextIO:
        """Construct a file-like object."""
        raise NotImplementedError()

    def as_quad_stream(
        self,
        url: str,
        iri: Optional[URIRef],
        root_loader: 'Loader',
    ) -> Iterable[Quad]:
        """Convert data into a stream of RDF quads."""
        raise NotImplementedError(
            f'{self}.as_quad_stream() is not implemented.',
        )

    def find_context(self, url: str) -> LDContext:
        """Find context for the file."""
        raise NotImplementedError(
            f'{self}.find_context() is not implemented.',
        )

    def __call__(self, url: str, options: PyLDOptions) -> PyLDResponse:
        """
        Call the loader to retrieve the document in a PYLD friendly format.

        Used to resolve remote contexts.
        """
        return {
            'document': self.as_jsonld_document(
                url=URL(url),
                iri=url,
            ),
            'contextUrl': None,
        }
