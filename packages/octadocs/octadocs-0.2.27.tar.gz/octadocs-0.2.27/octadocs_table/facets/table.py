import operator
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List

from dominate.tags import table, tbody, td, th, thead, tr
from dominate.util import raw
from iolanta.facet import Facet
from octadocs.iolanta import HTML, render
from octadocs.octiron import Octiron
from octadocs_table.models import TABLE
from rdflib import URIRef

Row = Dict[URIRef, Any]   # type: ignore


def list_columns(
    iri: URIRef,
    octiron: Octiron,
) -> List[URIRef]:
    """List of column IRIs for a table."""
    # Idea: http://www.snee.com/bobdc.blog/2014/04/rdf-lists-and-sparql.html
    return list(
        map(
            operator.itemgetter('column'),
            octiron.query(
                query_text='''
                SELECT ?column WHERE {
                    ?iri table:columns/rdf:rest*/rdf:first ?column .
                }
                ''',
                iri=URIRef(iri),
            ),
        ),
    )


def construct_headers(
    octiron: Octiron,
    table_iri: URIRef,
    columns: List[URIRef],
) -> Iterable[th]:
    """Construct table headers."""
    return (
        th(
            render(
                node=column,
                octiron=octiron,
                environments=[table_iri, TABLE.thead, HTML],
            ),
        ) for column in columns
    )


def construct_row(
    instance: URIRef,
    octiron: Octiron,
    columns: List[URIRef],
) -> Row:
    """Construct a table row."""
    formatted_columns = '({columns})'.format(
        columns=', '.join([
            f'<{column}>' for column in columns
        ]),
    )

    query_text = '''
    SELECT * WHERE {
        $instance ?column ?value .

        OPTIONAL {
            ?value octa:trustLevel ?trust_level .
        }

        FILTER(?column IN %s) .
    } ORDER BY ?column ?trust_level
    ''' % formatted_columns

    cells = octiron.query(
        query_text=query_text,
        instance=instance,
    )

    cells.append({
        'column': TABLE.self,
        'value': instance,
    })

    # This dictionary comprehension entails an implicit deduplication by
    # `cell['column']`, in which the last duplicate wins. Since we have sorted
    # the elements by `octa:trustLevel` this means we will prefer a higher trust
    # level over a lower one, or over an absence of defined trust level.
    return {
        cell['column']: instance if (
            cell['column'] == TABLE.self
        ) else cell['value']
        for cell in cells
    }


def select_instances(
    iri: URIRef,
    octiron: Octiron,
) -> Iterable[URIRef]:
    """Select instances, or rows, for the table."""
    return map(
        operator.itemgetter('instance'),
        octiron.query(
            query_text='''
            SELECT ?instance WHERE {
                $iri table:class ?class .
                ?instance a ?class .
            }
            ''',
            iri=iri,
        ),
    )


def render_row(
    row: Row,
    columns: List[URIRef],
    octiron: Octiron,
) -> Iterable[td]:
    """Compile a sequence of table cells for a row."""
    for column in columns:
        try:
            cell_value = row[column]
        except KeyError:
            yield td()
            continue

        cell_content = str(
            render(
                node=cell_value,
                octiron=octiron,
                environments=[column, TABLE.td, HTML],
            ),
        )
        yield td(raw(cell_content))


def get_ordering(iri: URIRef, octiron: Octiron) -> List[URIRef]:
    """List of columns that we are ordering by."""
    # Idea: http://www.snee.com/bobdc.blog/2014/04/rdf-lists-and-sparql.html
    return list(
        map(
            operator.itemgetter('column'),
            octiron.query(
                query_text='''
                SELECT ?column WHERE {
                    ?iri table:ordering/rdf:rest*/rdf:first ?column .
                }
                ''',
                iri=URIRef(iri),
            ),
        ),
    )


def construct_sorter(ordering: List[URIRef]):
    """Construct a sorting procedure for rows in a table."""
    def sorter(row: Row):   # noqa: WPS430
        return [
            row.get(order_field, None)
            for order_field in ordering
        ]

    return sorter


def order_rows(
    rows: List[Row],
    ordering: List[URIRef],
):
    """Order rows by particular properties."""
    return sorted(
        rows,
        key=construct_sorter(ordering),
    )


@dataclass
class Table(Facet):
    """Octadocs Table."""

    def render(self) -> table:
        """Render the table."""
        columns = list_columns(
            iri=self.uriref,
            octiron=self.octiron,
        )

        ordering = get_ordering(
            iri=self.uriref,
            octiron=self.octiron,
        )

        headers = construct_headers(
            octiron=self.octiron,
            table_iri=self.uriref,
            columns=columns,
        )

        instances = select_instances(
            iri=self.uriref,
            octiron=self.octiron,
        )

        rows = [
            construct_row(
                instance=instance,
                columns=columns,
                octiron=self.octiron,
            )
            for instance in instances
        ]

        rows = order_rows(
            rows=rows,
            ordering=ordering,
        )

        rows = [
            tr(
                *render_row(
                    row=row,
                    columns=columns,
                    octiron=self.octiron,
                ),
            )
            for row in rows
        ]

        return table(
            thead(
                tr(*headers),
            ),
            tbody(*rows),
        )
