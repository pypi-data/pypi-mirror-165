""" Sensospot Data Parser

Parsing the numerical output from Sensovations Sensospot image analysis.
"""

__version__ = "0.8.0"


import sys
from pathlib import Path

import click
import pandas

from . import columns  # noqa: F401
from .parser import parse_file, parse_folder  # noqa: F401

DEFAULT_OUTPUT_FILENAME = "collected_data.csv"


@click.command()
@click.argument(
    "source",
    type=click.Path(
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        writable=True,
    ),
)
@click.option(
    "-o",
    "--outfile",
    default=DEFAULT_OUTPUT_FILENAME,
    help=(
        "Output file name, use a dash '-' for stdout, "
        f"default: '{DEFAULT_OUTPUT_FILENAME}'"
    ),
)
@click.option(
    "-q",
    "--quiet",
    is_flag=True,
    default=False,
    help="Ignore Sanity Check",
)
@click.option(
    "-r",
    "--recurse",
    is_flag=True,
    default=False,
    help="Recurse into folders one level down",
)
def main(source, outfile, quiet=False, recurse=False):
    if recurse:
        _parse_recursive(source, outfile, quiet)
    else:
        _parse_one_folder(source, outfile, quiet)


def _output(data, folder, outfile):
    """output a datafarme to stdout or csv file

    data:    the pandas dataframe
    folder:  the folder to save the file to
    outfile: the name of the outfile, '-' will output to stdout
    """
    if outfile.strip() == "-":
        data.to_csv(sys.stdout, sep="\t")
    else:
        csv_file = Path(folder) / outfile
        data.to_csv(csv_file, sep="\t")


def _parse_one_folder(source, outfile, quiet):
    """parses the data of one folder"""
    source_path = Path(source)
    # read the raw data of a folder
    raw_data = parse_folder(source_path, quiet=quiet)
    _output(raw_data, source_path, outfile)
    return raw_data


def _parse_recursive(source, outfile, quiet):
    """parses all folders one level down and collects the data"""
    child_outfile = DEFAULT_OUTPUT_FILENAME
    source_path = Path(source)
    folders = (i for i in source_path.iterdir() if i.is_dir())
    non_hidden = (i for i in folders if not i.name.startswith("."))
    collection = (
        _parse_one_folder(f, child_outfile, quiet) for f in non_hidden
    )
    try:
        collected = pandas.concat(collection, ignore_index=True)
        _output(collected.reset_index(), source_path, outfile)
    except ValueError as e:
        print(str(e))
