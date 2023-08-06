from typing import Dict, TypeVar, Iterable

import funcy
from dominate.tags import i
from funcy import first
from urlpath import URL

from iolanta.facet import Facet
from iolanta.namespaces import IOLANTA
from octadocs.environment import iri_to_url
from octadocs.iolanta import render


Something = TypeVar('Something')


def path_depth(row: Dict[str, str]) -> int:
    """Depth of path."""
    url = URL(iri_to_url(row['parent_directory_index']))
    return len(url.parts)


def but_first(iterable: Iterable[Something]) -> Iterable[Something]:
    """Skip the first item of an iterable and return the remaining."""
    try:
        next(iterable)
    except StopIteration:
        pass

    return iterable


class Breadcrumbs(Facet):
    breadcrumbs_query = '''
    SELECT ?parent_directory_index ?parent_directory_index_subject WHERE {
        $this octa:subjectOf* ?this_page .

        ?this_page octa:isChildOf* ?parent_directory .
        ?parent_directory octa:isParentOf ?parent_directory_index .
        ?parent_directory_index a octa:IndexPage .

        ?parent_directory_index_subject octa:subjectOf ?parent_directory_index .

        FILTER( ?parent_directory_index != ?this_page )
    } ORDER BY ?parent_directory_index
    '''

    page_type_query = '''
    SELECT ?type WHERE {
        $this a ?type .
        ?type octa:position ?position .
    } ORDER BY ?position
    '''

    def renderable_page_type(self):
        return first(
            self.query(
                self.page_type_query,
                this=self.uriref,
            ),
        )['type']

    def render(self):
        rows = self.query(
            self.breadcrumbs_query,
            this=self.uriref,
        )

        sorted_rows = sorted(
            rows,
            key=path_depth,
        )

        instances = but_first(
            funcy.pluck(
                'parent_directory_index_subject',
                sorted_rows,
            ),
        )

        rendered_links = [
            render(
                instance,
                octiron=self.octiron,
                environments=[IOLANTA.html],
            )
            for instance in instances
        ]

        breadcrumbs = ' › '.join(map(str, rendered_links))

        rendered_type = i(
            render(
                self.renderable_page_type(),
                octiron=self.octiron,
                environments=[IOLANTA.html],
            ),
        )

        return ' › '.join(
            filter(
                bool,
                map(
                    str,
                    [
                        breadcrumbs,
                        rendered_type,
                    ],
                ),
            ),
        )
