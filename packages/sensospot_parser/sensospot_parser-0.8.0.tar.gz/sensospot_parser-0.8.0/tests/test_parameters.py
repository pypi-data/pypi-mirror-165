import pandas

from .conftest import EXAMPLE_DIR_WO_PARAMS, EXAMPLE_DIR_WITH_PARAMS


def test_search_params_file_ok(example_dir):
    from sensospot_parser.parameters import _search_params_file

    result = _search_params_file(example_dir / EXAMPLE_DIR_WITH_PARAMS)

    assert result.suffix == ".svexp"


def test_search_params_file_no_parameters_folder(example_dir):
    from sensospot_parser.parameters import _search_params_file

    result = _search_params_file(example_dir / EXAMPLE_DIR_WO_PARAMS)

    assert result is None


def test_ssearch_measurement_params_file_parameters_file(tmpdir):
    from sensospot_parser.parameters import _search_params_file

    params_dir = tmpdir / "Parameters"
    params_dir.mkdir()

    result = _search_params_file(tmpdir)

    assert result is None


def test_parse_channel_info(example_dir):
    from sensospot_parser.parameters import (
        _search_params_file,
        _parse_measurement_params,
    )

    params = _search_params_file(example_dir / EXAMPLE_DIR_WITH_PARAMS)
    result = _parse_measurement_params(params)

    expected = pandas.DataFrame(
        {
            "Exposure.Id": [1, 2, 3],
            "Parameters.Channel": ["green", "red", "red"],
            "Parameters.Time": [100.0, 150.0, 15.0],
        }
    )

    assert result.equals(expected)


def test_get_measurement_params_file_found(example_dir):
    from sensospot_parser.parameters import get_measurement_params

    result = get_measurement_params(example_dir / EXAMPLE_DIR_WITH_PARAMS)

    expected = pandas.DataFrame(
        {
            "Exposure.Id": [1, 2, 3],
            "Parameters.Channel": ["green", "red", "red"],
            "Parameters.Time": [100.0, 150.0, 15.0],
        }
    )

    assert result.equals(expected)


def test_get_measurement_params_file_not_found(example_dir):
    from sensospot_parser.parameters import get_measurement_params

    result = get_measurement_params(example_dir / EXAMPLE_DIR_WO_PARAMS)

    assert result is None


def test_add_measurement_parameters_with_params_file(exposure_df, example_dir):
    from sensospot_parser.parameters import add_measurement_parameters

    folder = example_dir / EXAMPLE_DIR_WITH_PARAMS
    exposure_df = add_measurement_parameters(exposure_df, folder)

    expected = [(1, "green", 100), (2, "red", 150), (3, "red", 15)]
    for exposure_id, channel, time in expected:
        mask = exposure_df["Exposure.Id"] == exposure_id
        example_row = exposure_df.loc[mask].iloc[0]
        assert example_row["Parameters.Channel"] == channel
        assert example_row["Parameters.Time"] == time


def test_add_measurement_parameters_without_params_file(
    exposure_df, example_dir
):
    from sensospot_parser.parameters import add_measurement_parameters

    folder = example_dir / EXAMPLE_DIR_WO_PARAMS
    exposure_df = add_measurement_parameters(exposure_df, folder)

    for exposure_id in range(1, 4):
        mask = exposure_df["Exposure.Id"] == exposure_id
        one_exposure_data_frame = exposure_df.loc[mask]
        assert one_exposure_data_frame["Parameters.Channel"].hasnans
        assert one_exposure_data_frame["Parameters.Time"].hasnans
