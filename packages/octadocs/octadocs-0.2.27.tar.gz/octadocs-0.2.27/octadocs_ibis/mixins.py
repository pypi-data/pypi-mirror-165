from rdflib import Literal


class LanguageAware:
    """Language aware facet."""

    def _is_row_fitting_language(self, row) -> bool:
        """All literals in the row either have no language or match the site."""
        for field_name, field_value in row.items():
            if (
                isinstance(field_value, Literal)
                and field_value.language
                and field_value.language != self.octiron.language
            ):
                return False

        return True

    def filter_by_language(self, rows):
        return filter(
            self._is_row_fitting_language,
            rows,
        )

    def query(self, query_text: str, **kwargs):
        """Language aware query."""
        return self.filter_by_language(
            super().query(query_text, **kwargs),
        )
