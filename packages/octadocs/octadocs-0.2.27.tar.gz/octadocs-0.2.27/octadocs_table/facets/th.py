from iolanta.facet import Facet
from octadocs.iolanta import render
from octadocs_table.models import TABLE


class Th(Facet):
    """Render a table column header."""

    def render(self):
        """Render the column."""
        return render(
            node=self.iri,
            octiron=self.octiron,
            environments=[TABLE.th],
        )
