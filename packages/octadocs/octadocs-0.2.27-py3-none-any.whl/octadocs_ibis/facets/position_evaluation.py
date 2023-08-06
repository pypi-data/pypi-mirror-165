from dominate.tags import div, p, h2
from more_itertools import first

from iolanta.facet import Facet
from iolanta.namespaces import IOLANTA
from octadocs.iolanta import render
from octadocs_ibis.models import IBIS
from octadocs_ibis.queries import retrieve_evaluation_for_position


class PositionEvaluation(Facet):
    sparql_query = '''
    SELECT ?evaluation ?value WHERE {
        $position ibis:evaluation ?evaluation .
        ?evaluation prov:value* ?value .

        FILTER (!isBlank(?value))
    }
    '''

    def render(self):
        try:
            is_approved, evaluation = retrieve_evaluation_for_position(
                position=self.uriref,
                ldflex=self.ldflex,
            )
        except TypeError:
            return ''

        if not evaluation:
            return ''

        admonition_class = 'success' if is_approved else 'failure'
        title = 'Принято' if is_approved else 'Отвергнуто'

        return div(
            h2('Оценка'),
            div(
                p(
                    title,
                    cls='admonition-title',
                ),
                p(
                    render(
                        evaluation,
                        environments=[IOLANTA.html],
                        octiron=self.octiron,
                    ),
                ),
                cls=f'admonition {admonition_class}',
            ),
        )
