from dataclasses import dataclass, field
from typing import Dict, Optional

from documented import DocumentedError
from iolanta.loaders import Loader
from iolanta.loaders.base import PyLDOptions, PyLDResponse
from iolanta.models import LDContext, LDDocument
from rdflib import URIRef
from urlpath import URL


@dataclass
class NamedContextNotFound(DocumentedError):
    """
    Named context not found.

        URL: {self.url}
        Supported contexts: {self.context_names}
    """

    url: str
    named_contexts: Dict[str, LDContext]

    @property
    def context_names(self):
        """Render names of supported contexts."""
        return ', '.join(self.named_contexts.keys())


@dataclass(frozen=True)
class NamedContextLoader(Loader):
    """Retrieve context by name."""

    named_contexts: Dict[str, LDContext] = field(repr=False)

    def construct_context_name(self, url: URL) -> str:
        """Clean the context name."""
        return url.path

    def as_jsonld_document(
        self,
        url: URL,
        iri: Optional[URIRef] = None,
    ) -> LDDocument:
        """Get JSON-LD document from named contexts."""
        context_name = self.construct_context_name(url)

        try:
            return self.named_contexts[context_name]
        except KeyError:
            raise NamedContextNotFound(
                url=url,
                named_contexts=self.named_contexts,
            )

    def __call__(self, url: str, options: PyLDOptions) -> PyLDResponse:
        """Retrieve the pre loaded named context by name."""
        return {
            'document': self.as_jsonld_document(
                url=url,
                iri=url,
            ),
            'contextUrl': None,
        }
