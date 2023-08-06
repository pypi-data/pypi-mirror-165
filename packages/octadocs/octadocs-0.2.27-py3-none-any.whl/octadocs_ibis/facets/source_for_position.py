from dominate.tags import blockquote, div, p
from more_itertools import first

from iolanta.facet import Facet
from iolanta.namespaces import IOLANTA
from octadocs.iolanta import render


class SourceForPosition(Facet):
    sparql_query = '''
    SELECT ?comment WHERE {
        $source rdfs:comment ?comment .
    } LIMIT 1
    '''

    def render(self):
        rows = self.query(
            self.sparql_query,
            source=self.iri,
        )

        try:
            row = first(rows)
        except ValueError:
            return f'[{self.uriref}]'

        return blockquote(
            p(
                row['comment'],
            ),
            p(
                render(
                    self.iri,
                    environments=[IOLANTA.html],
                    octiron=self.octiron,
                ),
                style='text-align: right',
            ),
        )
