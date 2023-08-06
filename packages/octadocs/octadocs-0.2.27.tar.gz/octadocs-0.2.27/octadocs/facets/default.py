from dominate.tags import a, span  # noqa: WPS347
from iolanta.facet import Facet
from more_itertools import first
from rdflib.term import Literal, URIRef


def language_by_row(row):
    try:
        return row['label'].language
    except KeyError:
        return None


class Default(Facet):
    """Default facet for rendering an unknown node."""

    sparql_query = '''
    SELECT * WHERE {
        OPTIONAL {
            ?page rdfs:label ?label .
        }

        OPTIONAL {
            ?page octa:symbol ?symbol .
        }

        OPTIONAL {
            ?page octa:url ?url .
        }

        OPTIONAL {
            ?page rdfs:comment ?comment .
        }

        OPTIONAL {
            ?page a octa:Page .
            BIND(true AS ?is_page)
        }
    } ORDER BY ?label
    '''

    def retrieve_row(self, page: URIRef):
        rows = self.query(
            self.sparql_query,
            page=page,
        )

        row_by_language = {
            language_by_row(row): row
            for row in rows
        }

        return row_by_language.get(
            self.language,
        ) or row_by_language.get(None)

    def render(self):   # noqa: C901
        """Render HTML."""
        if isinstance(self.iri, Literal):
            return str(self.iri.value)

        description = self.retrieve_row(self.uriref)
        if description is None:
            return str(self.iri)

        label = description.get('label', str(self.iri))
        url = description.get('url')

        symbol = description.get('symbol')
        if not symbol:
            symbol = ''

        comment = description.get('comment')

        if url:
            return a(
                symbol,
                label,
                href=url,
                title=comment,
            )

        if comment:
            return span(label, title=comment)

        return label
