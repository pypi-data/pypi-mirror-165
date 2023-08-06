import operator

from dominate.tags import div, h2, ul, li

from iolanta.facet import Facet
from iolanta.namespaces import IOLANTA
from octadocs.iolanta import render
from octadocs_ibis.models import IBIS


class SuggestedNextSteps(Facet):
    sparql_query = '''
    SELECT ?issue_page WHERE {
        $position ibis:suggests ?issue .
        ?issue octa:subjectOf* ?issue_page .
        ?issue_page a octa:Page .
    } ORDER BY ?issue
    '''

    def render(self):
        suggestions = map(
            operator.itemgetter('issue_page'),
            self.query(
                self.sparql_query,
                position=self.uriref,
            )
        )

        renderables = [
            render(
                suggestion,
                octiron=self.octiron,
                environments=[IOLANTA.html],
            )
            for suggestion in suggestions
        ]

        if renderables:
            list_items = list(map(li, renderables))

            return div(
                h2('Что дальше?'),
                ul(*list_items),
            )

        return ''
