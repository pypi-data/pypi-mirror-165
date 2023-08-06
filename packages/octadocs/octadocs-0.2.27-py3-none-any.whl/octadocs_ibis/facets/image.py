import operator

from dominate.tags import img
from more_itertools import first

from iolanta.facet import Facet


class Image(Facet):
    sparql_query = 'SELECT * WHERE { $image octa:url ?url } LIMIT 1'

    def render(self):
        rows = self.query(
            self.sparql_query,
            image=self.iri,
        )

        urls = map(
            operator.itemgetter('url'),
            rows,
        )

        try:
            url = first(urls)
        except ValueError:
            return f'(No Image for {self.uriref} [{type(self.uriref)}])'

        return img(src=url)
