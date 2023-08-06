from dominate.tags import span, a
from iolanta.facet import Facet
from more_itertools import first


class GithubLicense(Facet):
    """Render license information."""

    sparql_text = '''
    SELECT * WHERE {
        $license
            <http://spdx.org/rdf/terms#licenseId> ?id ;
            <http://spdx.org/rdf/terms#name> ?name .

        OPTIONAL {
            $license rdfs:label ?label .
        }
    } ORDER BY ?id
    '''

    def render(self):
        """Render."""
        rows = self.query(
            self.sparql_text,
            license=self.iri,
        )

        row = first(rows)

        url = row['license']
        title = row['name']
        text = str(row['id'])

        if text == 'NOASSERTION':
            text = title

        label = row.get('label')

        return a(
            label or text,
            title=title,
            href=url,
        )
