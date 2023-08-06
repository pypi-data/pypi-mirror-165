import itertools
import json
from dataclasses import dataclass, replace
from typing import Any, Iterable, Optional, TextIO

from documented import DocumentedError
from iolanta.loaders.base import Loader
from iolanta.models import LDContext, LDDocument, Quad
from iolanta.namespaces import LOCAL
from iolanta.parsers.base import Parser
from octadocs.types import OCTA
from pyld import jsonld
from pyld.jsonld import JsonLdError
from rdflib import XSD, URIRef, RDF
from rdflib.term import BNode, Literal, Node


def assign_key_if_not_present(  # type: ignore
    document: LDDocument,
    key: str,
    default_value: Any,
) -> LDDocument:
    """Add key to document if it does not exist yet."""
    if isinstance(document, dict):
        if document.get(key) is None:
            return {
                key: default_value,
                **document,
            }

        return document

    elif isinstance(document, list):
        return [
            assign_key_if_not_present(
                document=sub_document,
                key=key,
                default_value=default_value,
            )
            for sub_document in document
        ]

    return document


@dataclass
class UnresolvedIRI(DocumentedError):
    """
    An unresolved IRI found.

        IRI: {self.iri}
        file: {self.file}
        prefix: {self.prefix}

    Perhaps you forgot to import appropriate context? For example:

    ```yaml
    $context:
        - $import: {self.prefix}
    ```
    """

    iri: str
    prefix: str
    file: Optional[str] = None


def raise_if_term_is_qname(term_value: str):
    """Raise an error if a QName is provided instead of a full IRI."""
    prefix, etc = term_value.split(':', 1)

    if etc.startswith('/'):
        return

    if prefix in {'local', 'templates'}:
        return

    raise UnresolvedIRI(
        iri=term_value,
        prefix=prefix,
    )


def parse_term(
    term,
    blank_node_prefix,
) -> Node:
    """Parse N-Quads term into a Quad."""
    term_type = term['type']
    term_value = term['value']

    if term_type == 'IRI':
        raise_if_term_is_qname(term_value)
        return URIRef(term_value)

    if term_type == 'literal':
        language = term.get('language')

        if datatype := term.get('datatype'):
            datatype = URIRef(datatype)

            # XSD.string does not provide any extra information. Removing it.
            if datatype == XSD.string:
                datatype = None

        if language and datatype:
            datatype = None

        return Literal(
            term_value,
            datatype=datatype,
            lang=language,
        )

    if term_type == 'blank node':
        return BNode(
            value=term_value.replace('_:', f'{blank_node_prefix}/'),
        )

    raise ValueError(f'Unknown term: {term}')


def parse_quads(
    quads_document,
    graph: URIRef,
    blank_node_prefix: str = '',
) -> Iterable[Quad]:
    """Parse an N-Quads output into a Quads stream."""
    for graph_name, quads in quads_document.items():
        if graph_name == '@default':
            graph_name = graph

        else:
            graph_name = URIRef(graph_name)

        for quad in quads:
            try:
                yield Quad(
                    subject=parse_term(quad['subject'], blank_node_prefix),
                    predicate=parse_term(quad['predicate'], blank_node_prefix),
                    object=parse_term(quad['object'], blank_node_prefix),
                    graph=graph_name,
                )
            except UnresolvedIRI as unresolved_iri:
                raise replace(
                    unresolved_iri,
                    file=str(graph),
                )


class JSON(Parser):
    """Load JSON data."""

    def as_jsonld_document(self, raw_data: TextIO) -> LDDocument:
        """Read JSON content as a JSON-LD document."""
        return json.load(raw_data)

    def as_quad_stream(
        self,
        raw_data: TextIO,
        iri: Optional[URIRef],
        context: LDContext,
        root_loader: Loader,
    ) -> Iterable[Quad]:
        """Read JSON-LD data into a quad stream."""
        document = self.as_jsonld_document(raw_data)

        document = assign_key_if_not_present(
            document=document,
            key='@id',
            default_value=str(iri),
        )

        document = assign_key_if_not_present(
            document=document,
            key=str(OCTA.subjectOf),
            default_value={
                '@id': str(iri),
            },
        )

        try:
            document = jsonld.expand(
                document,
                options={
                    'expandContext': context,
                    'documentLoader': root_loader,

                    # Explanation:
                    #   https://github.com/digitalbazaar/pyld/issues/143
                    'base': str(LOCAL),
                },
            )
        except JsonLdError as err:
            raise ExpandError(
                message=str(err),
                document=document,
                context=context,
                iri=iri,
            ) from err

        document = jsonld.flatten(document)

        static_quads = [
            Quad(iri, RDF.type, OCTA.File, iri),
        ]

        return list(
            itertools.chain(
                parse_quads(
                    quads_document=jsonld.to_rdf(document),
                    graph=iri,
                    blank_node_prefix=str(iri),
                ),
                static_quads,
            )
        )


@dataclass
class ExpandError(DocumentedError):
    """
    JSON-LD expand operation failed.

    IRI: {self.iri}
    {self.message}
    """

    message: str
    document: LDDocument
    context: LDContext
    iri: str

    @property
    def formatted_data(self) -> str:
        """Format document for printing."""
        return json.dumps(self.document, indent=2)

    @property
    def formatted_context(self):
        """Format context for printing."""
        return json.dumps(self.context, indent=2)
