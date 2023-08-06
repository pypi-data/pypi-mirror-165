""" Sensospot Data Parser

Parsing the numerical output from Sensovations Sensospot image analysis.
"""

import pathlib
from typing import Any, Dict, Union, Optional
from xml.etree.ElementTree import Element as ElementType

import numpy
import pandas
from defusedxml import ElementTree

from . import columns

PathLike = Union[str, pathlib.Path]


def _search_params_file(folder: PathLike) -> Optional[pathlib.Path]:
    """searches for a exposure settings file in a folder

    folder:  directory to search
    returns: the path to the settings file or None
    """
    folder_path = pathlib.Path(folder)
    params_folder = folder_path / "Parameters"
    if not params_folder.is_dir():
        return None
    param_files = list(params_folder.glob("**/*.svexp"))
    if len(param_files) == 1:
        return param_files[0]
    else:
        return None


def _get_channel_data(channel_node: ElementType) -> Dict[str, Any]:
    """parses the information from an xml node of the channel settings

    channel_node:   the xml node of the channel settings
    returns:        dict with the information
    """
    # child.tag == "ChannelConfig1"
    exposure_id = int(channel_node.tag[-1])
    # channel_description == "[Cy3|Cy5] Green"
    description = channel_node.attrib["Description"]
    exposure_channel = description.rsplit(" ", 1)[-1]
    # floats can be used for exposure times, not only ints
    exposure_time = float(channel_node.attrib["ExposureTimeMs"])
    return {
        columns.EXPOSURE_ID: exposure_id,
        columns.PARAMETERS_CHANNEL: exposure_channel.lower(),
        columns.PARAMETERS_TIME: exposure_time,
    }


def _parse_measurement_params(params_file: PathLike) -> pandas.DataFrame:
    """parses the cannel informations from a settings file

    params_file: path to the settings file
    returns:     pandas DataFrame with the parsed information
    """
    file_path = pathlib.Path(params_file)
    with file_path.open("r") as file_handle:
        tree = ElementTree.parse(file_handle)
        data = [_get_channel_data(child) for child in tree.find("Channels")]
    return pandas.DataFrame(data)


def get_measurement_params(folder: PathLike) -> Optional[pandas.DataFrame]:
    """searches the settings file and returns the parameters

    folder: path to the folder with the measurement data
    returns: pandas DataFrame with the parsed parameters or None
    """
    params_file = _search_params_file(folder)
    if params_file is not None:
        return _parse_measurement_params(params_file)
    return None


def add_measurement_parameters(
    measurement: pandas.DataFrame, folder: PathLike
) -> pandas.DataFrame:
    """adds measurement params to the data frame, if they could be parsed

    The returned DataFrame will contain two more columns for parsed time and
    channel from the parameters file.

    If the parameters could not be found, parsed or do not match up with the
    measurement data, the additional collumns will contain NaN.

    measurement: the parsed measurement data
    returns:     the measurement data with parameters added
    """
    params = get_measurement_params(folder)
    if params is not None:
        params_exposures = params[columns.EXPOSURE_ID].unique()
        data_exposures = measurement[columns.EXPOSURE_ID].unique()
        if set(data_exposures) == set(params_exposures):
            return measurement.merge(
                params, how="left", on=columns.EXPOSURE_ID
            )

    # only executing if the parameters were not merged to the data frame
    measurement[columns.PARAMETERS_CHANNEL] = numpy.nan
    measurement[columns.PARAMETERS_TIME] = numpy.nan
    return measurement
