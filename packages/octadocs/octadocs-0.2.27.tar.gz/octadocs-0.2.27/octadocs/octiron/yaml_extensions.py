from typing import Any, Dict, List, Union

from iolanta.parsers.json import ExpandError
from octadocs.types import LOCAL
from pyld import jsonld
from pyld.jsonld import JsonLdError

try:  # noqa
    from yaml import CSafeDumper as SafeDumper  # noqa
    from yaml import CSafeLoader as SafeLoader  # noqa
except ImportError:
    from yaml import SafeDumper  # type: ignore   # noqa
    from yaml import SafeLoader  # type: ignore   # noqa

MetaData = Union[List[Dict[str, Any]], Dict[str, Any]]  # type: ignore  # noqa


def jsonld_expand(data, context, local_iri, pyld_loader=None):
    """Expand the JSON_LD data with the help of particular loader."""
    options = {
        'base': str(LOCAL),
    }

    if context:
        options.update({'expandContext': context})

    if pyld_loader is not None:
        options.update({'documentLoader': pyld_loader})

    try:
        return jsonld.expand(
            data,
            options=options,
        )
    except (TypeError, JsonLdError) as err:
        raise ExpandError(
            message=str(err),
            document=data,
            context=context,
            iri=local_iri,
        ) from err
