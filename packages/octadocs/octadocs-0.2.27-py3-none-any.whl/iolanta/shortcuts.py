from pathlib import Path
from typing import Dict, Iterable, Type

from iolanta.loaders.local_file import Loader, LocalFile
from iolanta.loaders.named import NamedContextLoader
from iolanta.loaders.scheme_choice import SchemeChoiceLoader
from iolanta.models import LDContext, LDDocument, Quad
from rdflib import URIRef
from urlpath import URL


def choose_loader_by_url(url: URL) -> Type[Loader]:
    """Find loader by URL scheme."""
    return LocalFile


def as_document(url: URL) -> LDDocument:
    """Retrieve the document presented by the specified URL."""
    loader_class = choose_loader_by_url(url)
    return loader_class().as_jsonld_document(url)


def construct_root_loader(
    root_directory: Path,
    default_context: LDContext,
    named_contexts: Dict[str, LDContext],
) -> SchemeChoiceLoader:
    return SchemeChoiceLoader(
        loader_by_scheme={
            'file': LocalFile(
                root_directory=root_directory,
                default_context=default_context,
            ),
            'local': NamedContextLoader(
                named_contexts=named_contexts,
            ),
        },
    )


def as_quad_stream(
    url: URL,
    iri: URIRef,
    default_context: LDContext,
    root_directory: Path,
    named_contexts: Dict[str, LDContext],
) -> Iterable[Quad]:
    """Retrieve the stream presented by the specified URL."""
    root_loader = construct_root_loader(
        default_context=default_context,
        root_directory=root_directory,
        named_contexts=named_contexts,
    )

    return root_loader.as_quad_stream(
        url=url,
        iri=iri,
    )
