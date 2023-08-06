import json
from dataclasses import dataclass, field
from functools import reduce
from pathlib import Path
from typing import Iterable, List, Optional, TextIO, Type

from documented import DocumentedError
from iolanta.context import merge
from iolanta.conversions import url_to_path
from iolanta.loaders.base import Loader
from iolanta.models import LDContext, LDDocument, Quad
from iolanta.parsers.base import Parser
from iolanta.parsers.json import JSON
from iolanta.parsers.markdown import Markdown
from iolanta.parsers.yaml import YAML
from rdflib import URIRef
from urlpath import URL


@dataclass
class IsAContext(DocumentedError):
    """
    The provided file is a context.

        - Path: {self.path}

    This file is not a piece of data and cannot be loaded into the graph.
    """

    path: URL


@dataclass
class ParserNotFound(DocumentedError):
    """
    Parser not found.

        Path: {self.path}
    """

    path: URL


def merge_contexts(*contexts: LDContext) -> LDContext:
    return reduce(
        merge,
        contexts,
    )


@dataclass(frozen=True)
class LocalFile(Loader):
    """
    Retrieve Linked Data from a file on local disk.

    Requires URL with file:// scheme as input.
    """

    root_directory: Optional[Path] = None
    context_filenames: List[str] = field(default_factory=lambda: [
        'context.yaml',
        'context.json',
    ])
    default_context: Optional[LDContext] = field(default=None, repr=False)

    def choose_parser_class(self, url: URL) -> Type[Parser]:
        """
        Choose parser class based on file extension.

        FIXME this is currently hard coded; need to change to a more extensible
          mechanism.
        """
        if url.suffix == '.yaml':
            return YAML

        elif url.suffix == '.json':
            return JSON

        elif url.suffix == '.md':
            return Markdown

        raise ParserNotFound(path=url)

    def as_quad_stream(
        self,
        url: URL,
        iri: Optional[URIRef],
        root_loader: Loader,
    ) -> Iterable[Quad]:
        """Extract a sequence of quads from a local file."""
        if url.stem == 'context':
            raise IsAContext(path=url)

        parser_class = self.choose_parser_class(url)

        context = self.find_context(url)

        with url_to_path(url).open() as text_io:
            return parser_class().as_quad_stream(
                raw_data=text_io,
                iri=iri,
                context=context,
                root_loader=root_loader,
            )

    def as_file(self, url: URL) -> TextIO:
        """Construct a file-like object."""
        path = url_to_path(url)
        with path.open() as text_io:
            return text_io

    def as_jsonld_document(
        self,
        url: URL,
        iri: Optional[URIRef] = None,
    ) -> LDDocument:
        """As JSON-LD document."""
        parser_class: Type[Parser] = self.choose_parser_class(url)
        with url_to_path(url).open() as text_io:
            document = parser_class().as_jsonld_document(text_io)

        if iri is not None and isinstance(document, dict):
            document.setdefault('@id', str(iri))

        return document

    def find_context(self, url: URL) -> LDContext:
        """Traverse the directories and construct context."""
        return merge_contexts(
            self.default_context,
            *self.contexts_by_url(url),
        )

    def contexts_by_url(self, url: URL) -> Iterable[LDContext]:
        return [
            self.as_jsonld_document(
                url=URL(f'file://{context_file}'),
            )
            for context_file in self.context_files_by_url(url)
        ]

    def context_files_by_url(self, url: URL) -> Iterable[Path]:
        """Yield all contexts by URL."""
        ancestor_directories = self.ancestors_by_url(url)
        for directory in ancestor_directories:
            for filename in self.context_filenames:
                if (context_file := directory / filename).exists():
                    yield context_file

    def ancestors_by_url(self, url: URL) -> Iterable[Path]:
        """Find all ancestor directories to this path."""
        if self.root_directory is None:
            raise ValueError('Please specify a root directory.')

        root_directory = self.root_directory.absolute()
        for ancestor in reversed(url_to_path(url).parents):
            ancestor = ancestor.absolute()

            # Replace with .is_relative_to() for Python 3.9.
            if str(ancestor).startswith(str(root_directory)):
                yield ancestor
