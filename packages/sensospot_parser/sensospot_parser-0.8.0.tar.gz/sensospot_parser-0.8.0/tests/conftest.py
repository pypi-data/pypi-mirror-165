""" test fixtures """

from pathlib import Path

import pandas
import pytest

EXAMPLE_DIR_WO_PARAMS = "mtp_wo_parameters"
EXAMPLE_DIR_WITH_PARAMS = "mtp_with_parameters"


@pytest.fixture(scope="session")
def example_dir(request):
    root_dir = Path(request.config.rootdir)
    yield root_dir / "example_data"


@pytest.fixture
def example_file(example_dir):
    data_dir = example_dir / EXAMPLE_DIR_WO_PARAMS
    yield data_dir / "160218_SG2-013-001_Regen1_Cy3-100_1_A1_1.csv"


@pytest.fixture
def exposure_df():
    from pandas import DataFrame

    yield DataFrame(data={"Exposure.Id": [1, 2, 3]})


@pytest.fixture
def normalization_data_frame():
    from sensospot_parser.columns import RAW_DATA_NORMALIZATION_MAP

    overflow_test_values = [
        (1, 1, 1, 50, 1, 0),
        (1, 1, 2, 50, 1, 2),
        (1, 1, 3, 50, 1, 2),
        (1, 1, 4, 50, 1, 0),
        (1, 1, 1, 25, 2, 0),
        (1, 1, 2, 25, 2, 0),
        (1, 1, 3, 25, 2, 2),
        (1, 1, 4, 25, 2, 2),
        (1, 1, 1, 10, 3, 0),
        (1, 1, 2, 10, 3, 0),
        (1, 1, 3, 10, 3, 2),
        (1, 1, 4, 10, 3, 0),
        (1, 2, 1, 50, 10, 0),
        (1, 2, 2, 50, 10, 0),
        (1, 2, 3, 50, 10, 0),
        (1, 2, 4, 50, 10, 0),
        (1, 2, 1, 25, 20, 0),
        (1, 2, 2, 25, 20, 0),
        (1, 2, 3, 25, 20, 2),
        (1, 2, 4, 25, 20, 2),
        (1, 2, 1, 10, 30, 0),
        (1, 2, 2, 10, 30, 0),
        (1, 2, 3, 10, 30, 2),
        (1, 2, 4, 10, 30, 0),
        (2, 1, 1, 50, 100, 0),
        (2, 1, 2, 50, 100, 0),
        (2, 1, 3, 50, 100, 0),
        (2, 1, 4, 50, 100, 0),
        (2, 1, 1, 25, 200, 0),
        (2, 1, 2, 25, 200, 0),
        (2, 1, 3, 25, 200, 2),
        (2, 1, 4, 25, 200, 2),
        (2, 1, 1, 10, 300, 0),
        (2, 1, 2, 10, 300, 0),
        (2, 1, 3, 10, 300, 2),
        (2, 1, 4, 10, 300, 0),
    ]
    overflow_test_keys = [
        "Well.Row",
        "Well.Column",
        "Pos.Id",
        "Exposure.Time",
        "Value",
        "Saturation",
    ]
    overflow_test_data = [
        dict(zip(overflow_test_keys, v)) for v in overflow_test_values
    ]
    data_frame = pandas.DataFrame(overflow_test_data)
    data_frame["Exposure.Channel"] = "Cy5"

    for value_column in RAW_DATA_NORMALIZATION_MAP.keys():
        data_frame[value_column] = data_frame["Value"]

    yield data_frame


@pytest.fixture(scope="session")
def parsed_data_frame_with_params(example_dir):
    from sensospot_parser.parser import parse_folder

    return parse_folder(example_dir / EXAMPLE_DIR_WITH_PARAMS)


@pytest.fixture(scope="session")
def parsed_data_frame_without_params(example_dir):
    from sensospot_parser.parser import parse_folder

    return parse_folder(example_dir / EXAMPLE_DIR_WO_PARAMS)


@pytest.fixture
def data_frame_with_params(parsed_data_frame_with_params):
    return parsed_data_frame_with_params.copy()


@pytest.fixture
def data_frame_without_params(parsed_data_frame_without_params):
    return parsed_data_frame_without_params.copy()
