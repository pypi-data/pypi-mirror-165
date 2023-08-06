import logging
from functools import cached_property
from pathlib import Path
from typing import Dict, Any, Set

from funcy import pluck
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files
from mkdocs.structure.nav import Navigation
from mkdocs.structure.pages import Page
from rdflib import URIRef
from urlpath import URL

from iolanta import as_document
from iolanta.models import LDContext
from octadocs.mixins import OctadocsMixin
from octadocs.plugin import Config
from octadocs_ibis.models import IBIS

logger = logging.getLogger(__name__)


POSITIONS_WITH_EVALUATIONS = '''
INSERT {
    ?position octa:symbol ?symbol .
} WHERE {
    ?position a ibis:Position .

    ?position ibis:evaluation / prov:value* ?is_approved .
    FILTER (isLiteral(?is_approved)) .

    BIND(
        IF(?is_approved = TRUE, "✔️", "❌")
        AS ?symbol
    )
}
'''


class IbisPlugin(OctadocsMixin, BasePlugin):
    """Issue-based information system (IBIS) plugin."""

    plugin_data_dir = Path(__file__).parent / 'data'
    namespaces = {
        'ibis': IBIS,
    }

    @cached_property
    def ibis_page_uris(self) -> Set[URIRef]:
        """IRIs of all pages which describe IBIS nodes."""
        return set(
            pluck(
                'page',
                self.query(
                    '''
                    SELECT ?page WHERE {
                        { ?thing a ibis:Issue } UNION { ?thing a ibis:Position }
                        ?thing octa:subjectOf* ?page .
                    }
                    ''',
                ),
            ),
        )

    def named_contexts(self) -> Dict[str, LDContext]:
        """Reusable named contexts."""
        return {
            'ibis': as_document(
                URL('file://', self.plugin_data_dir / 'named-context.json'),
            ),
        }

    def vocabularies(self) -> Dict[URIRef, Path]:
        """Load IBIS ontology."""
        return {
            URIRef(IBIS): self.plugin_data_dir / 'ibis.json',
            IBIS.term('facets.yaml'): self.plugin_data_dir / 'facets.yaml',
        }

    @property
    def templates_path(self) -> Path:
        """Templates associated with the plugin."""
        return Path(__file__).parent / 'templates'

    def on_page_context(
        self,
        context: Dict[str, Any],
        page: Page,
        **kwargs,
    ):
        """Make custom functions available to the template."""
        return {
            **context,
            'ibis': IBIS,
        }

    def on_nav(
        self,
        nav: Navigation,
        config: Config,
        files: Files,
    ) -> Navigation:
        logger.info('Marking ibis:Positions with symbols...')
        self.update(POSITIONS_WITH_EVALUATIONS)
        logger.info('Symbols marked.')

        return nav

    def on_page_markdown(
        self,
        markdown: str,
        page: Page,
        config: Config,
        files: Files,
    ):
        """Inject page template path, if necessary."""
        if page.iri in self.ibis_page_uris:
            page.meta['hide'] = ['navigation']

        return markdown
