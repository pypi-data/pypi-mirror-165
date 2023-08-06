from pathlib import Path
from typing import Dict

from iolanta import as_document
from iolanta.models import LDContext
from mkdocs.plugins import BasePlugin
from octadocs.mixins import OctadocsMixin
from octadocs.types import OCTA
from rdflib import PROV, URIRef
from urlpath import URL


class ProvenancePlugin(OctadocsMixin, BasePlugin):
    """Render an HTML table from data presented in the graph."""

    plugin_data_dir = Path(__file__).parent / 'data'

    def named_contexts(self) -> Dict[str, LDContext]:
        """Reusable named contexts."""
        return {
            'prov': as_document(
                URL('file://', self.plugin_data_dir / 'named-context.json'),
            ),
        }

    def vocabularies(self) -> Dict[URIRef, Path]:
        """Load PROV-O ontology."""
        return {
            URIRef(PROV): self.plugin_data_dir / 'prov.json',
            URIRef(OCTA.term('prov')): (
                self.plugin_data_dir / 'inference.yaml'
            ),
        }
