import json
import re
from io import StringIO
from typing import Iterable, Optional, TextIO

import frontmatter
from yaml.scanner import ScannerError

from iolanta.convert_dollar_signs import convert_dollar_signs
from iolanta.loaders import Loader
from iolanta.models import LDContext, LDDocument, Quad
from iolanta.parsers.errors import YAMLError
from iolanta.parsers.json import JSON, assign_key_if_not_present
from iolanta.parsers.yaml import YAML
from octadocs.types import OCTA
from rdflib import RDF, URIRef

try:  # noqa
    from yaml import CSafeLoader as SafeLoader  # noqa
except ImportError:
    from yaml import SafeLoader  # type: ignore   # noqa


class Markdown(YAML):
    """Load YAML data."""

    def as_jsonld_document(self, raw_data: TextIO) -> LDDocument:
        """Read YAML content and adapt it to JSON-LD format."""
        raw_data.seek(0)
        document = frontmatter.load(raw_data).metadata
        return convert_dollar_signs(document)

    def construct_page_url(self, iri: URIRef) -> str:
        """Construct URL of a page."""
        match = re.match('^local:(?P<path>.+)$', str(iri))
        if match is None:
            raise ValueError(f'Could not decode URL: {iri}')

        url = match.groupdict()['path']

        url = re.sub(
            r'(index)?\.md$',
            '',
            url,
        )

        if not url.endswith('/'):
            url = f'{url}/'

        return f'/{url}'

    def as_quad_stream(
        self,
        raw_data: TextIO,
        iri: Optional[URIRef],
        context: LDContext,
        root_loader: Loader,
    ) -> Iterable[Quad]:
        """Assign octa:url and generate quad stream."""
        try:
            json_data = self.as_jsonld_document(raw_data)
        except ScannerError as err:
            raise YAMLError(
                iri=iri,
                error=err,
            ) from err

        json_data = assign_key_if_not_present(
            document=json_data,
            key=str(OCTA.url),
            default_value=self.construct_page_url(iri),
        )

        quad_stream = JSON().as_quad_stream(
            raw_data=StringIO(json.dumps(json_data, ensure_ascii=False)),
            iri=iri,
            context=context,
            root_loader=root_loader,
        )

        return [
            Quad(iri, RDF.type, OCTA.Page, iri),
            *quad_stream,
        ]
