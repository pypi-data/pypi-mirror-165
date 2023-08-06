""" Sensospot Data Parser

Parsing the numerical output from Sensovations Sensospot image analysis.
"""

import re
import pathlib
from typing import Union, TextIO, Optional, Sequence
from collections import namedtuple

import pandas

from . import columns
from .parameters import add_measurement_parameters

PathLike = Union[str, pathlib.Path]

REGEX_WELL = re.compile(
    r"""
    (?P<row>([A-Z]+))  # row name containing one or more letters
    (?P<column>(\d+))     # column, one or more decimals
    """,
    re.VERBOSE | re.IGNORECASE,
)

FileInfo = namedtuple("FileInfo", ["row", "column", "exposure"])


def _guess_decimal_separator(file_handle: TextIO) -> str:
    """guesses the decimal spearator of a opened data file

    This is a very crude method, but depending on the language setting,
    different decimal separators may be used.

    file_handle:  a file handle to an opened csv file
    returns: either '.' or ',' as a decimal separator
    """
    file_handle.seek(0)
    headers = next(file_handle)  # noqa: F841
    data = next(file_handle)
    separator = "," if data.count(",") > data.count(".") else "."
    file_handle.seek(0)
    return separator


def _parse_csv(data_file: PathLike) -> pandas.DataFrame:
    """parse a csv sensovation data file

    Tries to guess the decimal separator from the file contents

    data_file: path to the csv file
    returns:   pandas DataFrame with the parsed data
    """
    data_path = pathlib.Path(data_file)
    with data_path.open("r") as handle:
        decimal_sep = _guess_decimal_separator(handle)
        handle.seek(0)
        return pandas.read_csv(handle, sep="\t", decimal=decimal_sep)


def _extract_measurement_info(data_file: PathLike) -> FileInfo:
    """extract measurement meta data from a file name

    data_file:  path to the csv data file
    returns:    named tuple FileInfo with parsed metadata
    """
    data_path = pathlib.Path(data_file)
    *rest, well, exposure = data_path.stem.rsplit("_", 2)  # noqa: F841
    matched = REGEX_WELL.match(well)
    if matched is None:
        raise ValueError(f"not a valid well: '{well}'")
    row = matched["row"].upper()
    column = int(matched["column"])
    exposure = int(exposure)
    return FileInfo(row, column, exposure)


def _cleanup_data_columns(data_frame: pandas.DataFrame) -> pandas.DataFrame:
    """renames some data columns for consistency and drops unused columns

    data_frame: pandas DataFrame with parsed measurement data
    returns:    pandas DataFrame, column names cleaned up
    """
    renamed = data_frame.rename(columns=columns.CSV_RENAME_MAP)
    surplus_columns = set(renamed.columns) - columns.PARSED_DATA_COLUMN_SET
    return renamed.drop(columns=surplus_columns)


def parse_file(data_file: PathLike) -> pandas.DataFrame:
    """parses one data file and adds metadata to result

    will race a ValueError, if metadata could not be extracted

    data_file: path to the csv data file
    raises:    ValueError if metadata could not be extracted
    returns:   pandas DataFrame with the parsed data
    """
    data_path = pathlib.Path(data_file).resolve()
    measurement_info = _extract_measurement_info(data_path)
    data_frame = _parse_csv(data_path)
    # normalized well name
    data_frame[
        columns.WELL_NAME
    ] = f"{measurement_info.row}{measurement_info.column:02d}"
    data_frame[columns.WELL_ROW] = measurement_info.row
    data_frame[columns.WELL_COLUMN] = measurement_info.column
    data_frame[columns.EXPOSURE_ID] = measurement_info.exposure
    data_frame[columns.ANALYSIS_NAME] = data_path.parent.name
    return _cleanup_data_columns(data_frame)


def _parse_file_silenced(data_file: PathLike) -> Optional[pandas.DataFrame]:
    """parses one data file and adds metadata

    data_file: path to the csv data file
    returns: pandas DataFrame with the parsed data or None on error
    """
    try:
        return parse_file(data_file)
    except ValueError:
        return None


def parse_multiple_files(file_list: Sequence[PathLike]) -> pandas.DataFrame:
    """parses a list of file paths to one combined data frame

    file_list: collection of paths to csv data files
    returns:   pandas DataFrame with all parsed data combined
    """
    if not file_list:
        raise ValueError("Empty file list provided")
    collection = (_parse_file_silenced(path) for path in file_list)
    filtered = (frame for frame in collection if frame is not None)
    data_frame = pandas.concat(filtered, ignore_index=True).reset_index()
    data_frame[columns.WELL_ROW] = data_frame[columns.WELL_ROW].astype(
        "category"
    )
    return data_frame


def find_csv_files(folder: PathLike) -> Sequence[pathlib.Path]:
    """returns all csv files in a folder

    folder:  path to the folder to search for csv files
    returns: iterator with the found csv files
    """
    folder_path = pathlib.Path(folder)
    files = (item for item in folder_path.iterdir() if item.is_file())
    visible = (item for item in files if not item.stem.startswith("."))
    return (item for item in visible if item.suffix.lower() == ".csv")


def _sanity_check(data_frame: pandas.DataFrame) -> pandas.DataFrame:
    """checks some basic constrains of a combined data frame

    data_frame: measurement data
    raises:     ValueError if basic constrains are not met
    returns:    pandas DataFrame
    """
    field_rows = len(data_frame[columns.WELL_ROW].unique())
    field_cols = len(data_frame[columns.WELL_COLUMN].unique())
    exposures = len(data_frame[columns.EXPOSURE_ID].unique())
    spot_positions = len(data_frame[columns.POS_ID].unique())
    expected_rows = field_rows * field_cols * exposures * spot_positions
    if expected_rows != len(data_frame):
        raise ValueError(
            f"Measurements are missing: {expected_rows} != {len(data_frame)}"
        )
    # set the right data type for measurement columns
    for raw_column in columns.NUMERIC_COLUMNS:
        data_frame[raw_column] = pandas.to_numeric(data_frame[raw_column])
    return data_frame


def parse_folder(folder: PathLike, quiet: bool = False) -> pandas.DataFrame:
    """parses all csv files in a folder to one large dataframe

    Will raise an ValueError, if no sensospot data could be found in
    the folder

    folder:  path of folder containing data files
    quiet:   skip sanity check, defaults to False
    returns: pandas dataframe with parsed data
    """
    folder_path = pathlib.Path(folder)
    file_list = find_csv_files(folder_path)
    try:
        data_frame = parse_multiple_files(file_list)
    except ValueError:
        raise ValueError(f"No sensospot data found in folder '{folder}'")
    data_frame = add_measurement_parameters(data_frame, folder_path)
    if quiet:
        return data_frame
    return _sanity_check(data_frame)
