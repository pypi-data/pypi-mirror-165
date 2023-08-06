import json
from pathlib import Path

import rich
from typer import Typer, Option
from urlpath import URL

from iolanta.loaders import LocalFile
from iolanta.shortcuts import construct_root_loader
from ldflex import LDFlex
from octadocs.cli.formatters.csv import csv_print
from octadocs.cli.formatters.json import print_json
from octadocs.cli.formatters.pretty import pretty_print
from octadocs.conversions import src_path_to_iri
from octadocs.default_context import construct_root_context
from octadocs.storage import load_graph
from octadocs.types import QueryResultsFormat

app = Typer(name='show')


def find_docs_dir() -> Path:
    """Find the docs dir of the MkDocs site."""
    cwd = Path.cwd()

    while True:
        docs = cwd / 'docs'
        if docs.is_dir():
            return docs

        cwd = cwd.parent


@app.command(name='file')
def show_file(
    path: Path,
    fmt: QueryResultsFormat = Option(
        default=QueryResultsFormat.PRETTY,
        metavar='format',
    ),
):
    """Show graph from a file."""
    docs_dir = find_docs_dir()
    path = path.absolute().relative_to(docs_dir)

    iri = src_path_to_iri(str(path))

    graph = load_graph(Path.cwd() / '.cache/octadocs')
    ldflex = LDFlex(graph)

    query_result = ldflex.query(
        '''
        SELECT ?s ?p ?o WHERE {
            GRAPH ?g {
                ?s ?p ?o
            }
        }
        ''',
        g=iri,
    )

    {
        QueryResultsFormat.CSV: csv_print,
        QueryResultsFormat.PRETTY: pretty_print,
        QueryResultsFormat.JSON: print_json,
    }[fmt](query_result)  # type: ignore


@app.command(name='context')
def show_context(path: Path):
    docs_dir = find_docs_dir()

    path = path.absolute().relative_to(docs_dir)
    url = URL(f'file://{path}')

    root_context = construct_root_context({})
    loader = LocalFile(
        root_directory=docs_dir,
        default_context=root_context,
    )

    context = loader.find_context(url)

    rich.print(
        json.dumps(
            context,
            ensure_ascii=False,
            indent=2,
        ),
    )
