import logging
import operator
import re
from functools import lru_cache, partial, cached_property
from pathlib import Path
from typing import Any, Callable, Dict, Optional

import rdflib
from mkdocs.livereload import LiveReloadServer
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files
from mkdocs.structure.nav import Navigation
from mkdocs.structure.pages import Page
from urlpath import URL

from iolanta import as_document
from iolanta.models import LDDocument
from octadocs.conversions import iri_by_page, src_path_to_iri
from octadocs.default_context import construct_root_context
from octadocs.iolanta import render
from octadocs.iolanta.errors import FacetNotFound
from octadocs.iolanta.iolanta import Render
from octadocs.macros import link
from octadocs.language_from_config import language_from_config
from octadocs.navigation.processor import OctadocsNavigationProcessor
from octadocs.octiron import Octiron
from octadocs.query import query
from octadocs.storage import save_graph
from octadocs.stored_query import StoredQuery
from octadocs.types import DEFAULT_NAMESPACES, LOCAL, OCTA, Query
from rdflib import URIRef
from rich.traceback import install
from typing_extensions import TypedDict

# install(show_locals=False)

logger = logging.getLogger(__name__)


class ConfigExtra(TypedDict):
    """Extra portion of the config which we put our graph into."""

    graph: rdflib.ConjunctiveGraph
    octiron: Octiron
    queries: StoredQuery
    named_contexts: Dict[str, Any]


class Config(TypedDict):
    """MkDocs configuration."""

    docs_dir: str
    extra: ConfigExtra
    nav: dict   # type: ignore


class TemplateContext(TypedDict):
    """Context for the native MkDocs page rendering engine."""

    graph: rdflib.ConjunctiveGraph
    iri: rdflib.URIRef
    this: rdflib.URIRef
    query: Query
    queries: StoredQuery
    local: rdflib.Namespace
    render: Callable[[rdflib.URIRef], str]

    # FIXME this is hardcode and should be removed
    rdfs: rdflib.Namespace


@lru_cache(None)
def cached_octiron(docs_dir: Path, language: Optional[str]) -> Octiron:
    """Retrieve cached Octiron instance or create it if absent."""
    return Octiron(
        root_directory=docs_dir,
        root_context=construct_root_context(
            namespaces=DEFAULT_NAMESPACES,
        ),
        language=language,
    )


class OctaDocsPlugin(BasePlugin):
    """MkDocs Meta plugin."""

    octiron: Octiron
    stored_query: StoredQuery

    def retrieve_named_context(self, relative_path: str) -> LDDocument:
        """Construct URL to the named context file."""
        return as_document(
            URL(
                'file://',
                Path(__file__).parent / 'data' / relative_path,
            ),
        )

    def on_config(self, config: Config) -> Config:
        """Initialize Octiron and provide graph to macros through the config."""
        docs_dir = Path(config['docs_dir'])

        self.octiron = cached_octiron(
            docs_dir=docs_dir,
            language=language_from_config(config),
        )

        self.stored_query = StoredQuery(
            path=docs_dir.parent / 'queries',
            executor=partial(
                query,
                instance=self.octiron.graph,
            ),
        )

        if config['extra'] is None:
            config['extra'] = {}  # type: ignore

        config['extra'].update({
            'graph': self.octiron.graph,
            'octiron': self.octiron,
            'queries': self.stored_query,

            'named_contexts': {
                'rdfs': self.retrieve_named_context('rdfs/named-context.json'),
                'iolanta': self.retrieve_named_context(
                    'iolanta/named-context.json',
                ),
                'owl': self.retrieve_named_context('owl/named-context.json'),
                # 'octa': self.retrieve_named_context('octa/named-context.json'),
            },
        })

        return config

    def on_files(self, files: Files, config: Config):
        """Extract metadata from files and compose the site graph."""
        # Load the Octadocs vocabulary into graph
        self.octiron.update_from_file(
            path=Path(__file__).parent / 'yaml/octadocs.yaml',
            local_iri=rdflib.URIRef(OCTA),
            global_url='/octadocs.yaml',
            named_contexts=config['extra']['named_contexts'],
        )

        # And the global iolanta vocabulary
        self.octiron.update_from_file(
            path=Path(__file__).parent / 'yaml/iolanta.yaml',
            local_iri=rdflib.URIRef('https://iolanta.tech/'),
            global_url='/iolanta.yaml',
            named_contexts=config['extra']['named_contexts'],
        )

        for mkdocs_file in files:
            self.octiron.update_from_file(
                path=Path(mkdocs_file.abs_src_path),
                local_iri=src_path_to_iri(mkdocs_file.src_path),
                global_url=f'/{mkdocs_file.url}',
                named_contexts=config['extra']['named_contexts'],
            )

    def on_page_markdown(
        self,
        markdown: str,
        page: Page,
        config: Config,
        files: Files,
    ):
        """Inject page template path, if necessary."""
        page.iri = iri_by_page(page)
        page.id = self.id_by_page.get(page.iri, page.iri)

        try:
            template_url = Render(
                ldflex=self.octiron.ldflex,
            ).find_facet_iri(
                node=page.id,
                environments=[URIRef(OCTA)],
            )
        except FacetNotFound:
            return markdown

        page.meta['template'] = re.sub(
            '^templates:/*',
            '',
            template_url,
        )

        return markdown

    @cached_property
    def id_by_page(self) -> Dict[URIRef, URIRef]:
        """Retrieve the best suitable IRI for an MkDocs page."""
        rows = self.octiron.ldflex.query(
            'SELECT ?page ?this WHERE { ?this octa:subjectOf ?page . }',
        )

        return {
            row['page']: row['this']
            for row in rows
        }

    def on_page_context(
        self,
        context: TemplateContext,
        page: Page,
        config: Config,
        nav: Page,
    ) -> TemplateContext:
        """Attach the views to certain pages."""
        page_iri = rdflib.URIRef(
            f'{LOCAL}{page.file.src_path}',
        )

        context['this'] = context['id'] = self.id_by_page.get(page_iri, page_iri)
        context['graph'] = self.octiron.graph
        context['iri'] = page_iri

        # noinspection PyTypedDict
        context['query'] = partial(
            query,
            instance=self.octiron.graph,
        )
        context['queries'] = self.stored_query

        context['local'] = LOCAL
        context['LOCAL'] = LOCAL
        context.update(self.octiron.namespaces)

        context['render'] = partial(
            render,
            octiron=self.octiron,
        )

        # Provide all the support namespaces into template context
        context['octiron'] = self.octiron
        context['link'] = partial(
            link,
            octiron=self.octiron,
        )

        # Page attributes
        page.iri = page_iri
        page.id = self.id_by_page.get(page_iri, page_iri)

        return context

    def on_nav(
        self,
        nav: Navigation,
        config: Config,
        files: Files,
    ) -> Navigation:
        """Update the site's navigation from the knowledge graph."""
        # This must run after all on_files() handlers of all plugins, but before
        # any page rendering and facets. Nav calculation depends on inference,
        # that's why we call it here in on_nav().
        self.octiron.apply_inference()

        if not config.get('nav'):
            nav = OctadocsNavigationProcessor(
                graph=self.octiron.graph,
                navigation=nav,
            ).generate()

        return nav

    def on_serve(
        self,
        server: LiveReloadServer,
        config: Config,
        builder,
    ) -> LiveReloadServer:
        inference_directory = Path(config['docs_dir']).parent / 'inference'
        if inference_directory.is_dir():
            for sparql_file in inference_directory.glob('**/*.sparql'):
                server.watch(str(sparql_file), builder)

        queries_directory = Path(config['docs_dir']).parent / 'queries'
        if queries_directory.is_dir():
            for sparql_file in queries_directory.glob('**/*.sparql'):
                server.watch(str(sparql_file), builder)

        return server

    def on_post_build(self, config: Config):
        """Save the graph to a file on disk."""
        self.octiron.save_graph_to_cache()

    def on_build_error(self, error):
        """Save the graph to a file on build error."""
        self.octiron.save_graph_to_cache()
