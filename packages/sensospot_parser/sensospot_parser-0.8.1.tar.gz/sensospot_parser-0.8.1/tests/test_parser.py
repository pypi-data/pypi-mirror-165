""" Stub file for testing the project """


import numpy
import pytest

from .conftest import EXAMPLE_DIR_WO_PARAMS, EXAMPLE_DIR_WITH_PARAMS


@pytest.mark.parametrize(
    "sub_dir, file_name",
    [
        (
            EXAMPLE_DIR_WO_PARAMS,
            "160218_SG2-013-001_Regen1_Cy3-100_1_A1_1.csv",
        ),
        (
            EXAMPLE_DIR_WITH_PARAMS,
            "160210_SG2-010-001_Regen_cy3100_1_A1_1.csv",
        ),
    ],
)
def test_parse_csv(example_dir, sub_dir, file_name):
    from sensospot_parser.parser import _parse_csv

    result = _parse_csv(example_dir / sub_dir / file_name)

    columns = {
        " ID ": numpy.int64,
        "Pos.X": numpy.int64,
        "Pos.Y": numpy.int64,
        "Bkg.Mean": float,
        "Spot.Mean": float,
        "Bkg.Median": float,
        "Spot.Median": float,
        "Bkg.StdDev": float,
        "Spot.StdDev": float,
        "Bkg.Sum": numpy.int64,
        "Spot.Sum": numpy.int64,
        "Bkg.Area": numpy.int64,
        "Spot.Area": numpy.int64,
        "Spot.Sat. (%)": numpy.int64,
        "Found": numpy.bool_,
        "Pos.Nom.X": numpy.int64,
        "Pos.Nom.Y": numpy.int64,
        "Dia.": numpy.int64,
        "Rect.": str,
        "Contour": object,  # ignore the type of contour
    }

    assert set(result.columns) == set(columns.keys())
    assert len(result[" ID "].unique()) == 100
    assert len(result) == 100
    for column, value_type in columns.items():
        assert isinstance(result[column][0], value_type)


def test_parse_csv_no_array(example_dir):
    from sensospot_parser.parser import _parse_csv

    result = _parse_csv(example_dir / "no_array_A1_1.csv")

    assert len(result) == 1
    assert result[" ID "][0] == 0


@pytest.mark.parametrize(
    "input, expected", [("", "."), ("..,", "."), (".,,", ","), ("..,,", ".")]
)
def test_guess_decimal_separator_returns_correct_separator(input, expected):
    from io import StringIO

    from sensospot_parser.parser import _guess_decimal_separator

    handle = StringIO(f"header\n{input}\n")
    result = _guess_decimal_separator(handle)

    assert result == expected


def test_guess_decimal_separator_rewinds_handle():
    from io import StringIO

    from sensospot_parser.parser import _guess_decimal_separator

    handle = StringIO("\n".join(["header", "data_line"]))
    _guess_decimal_separator(handle)

    assert next(handle) == "header\n"


def test_well_regex_ok():
    from sensospot_parser.parser import REGEX_WELL

    result = REGEX_WELL.match("AbC123")

    assert result["row"] == "AbC"
    assert result["column"] == "123"


@pytest.mark.parametrize("input", ["", "A", "1", "1A", "-1", "A-"])
def test_well_regex_no_match(input):
    from sensospot_parser.parser import REGEX_WELL

    result = REGEX_WELL.match(input)

    assert result is None


@pytest.mark.parametrize(
    "filename, expected",
    [("A1_1.csv", ("A", 1, 1)), ("test/measurement_1_H12_2", ("H", 12, 2))],
)
def test_extract_measurement_info_ok(filename, expected):
    from sensospot_parser.parser import _extract_measurement_info

    result = _extract_measurement_info(filename)

    assert result == expected


@pytest.mark.parametrize("filename", ["wrong_exposure_A1_B", "no_well_XX_1"])
def test_extract_measurement_info_raises_error(filename):
    from sensospot_parser.parser import _extract_measurement_info

    with pytest.raises(ValueError):
        _extract_measurement_info(filename)


def test_cleanup_data_columns():
    from pandas import DataFrame

    from sensospot_parser.parser import _cleanup_data_columns

    columns = ["Rect.", "Contour", " ID ", "Found", "Dia."]
    data = {col: [i] for i, col in enumerate(columns)}
    data_frame = DataFrame(data=data)

    result = _cleanup_data_columns(data_frame)

    assert set(result.columns) == {"Pos.Id", "Spot.Found", "Spot.Diameter"}
    assert result["Pos.Id"][0] == 2
    assert result["Spot.Found"][0] == 3
    assert result["Spot.Diameter"][0] == 4


def test_parse_file(example_file):
    from sensospot_parser.parser import parse_file

    result = parse_file(example_file)

    columns = {
        "Pos.Id",
        "Pos.X",
        "Pos.Y",
        "Bkg.Mean",
        "Spot.Mean",
        "Bkg.Median",
        "Spot.Median",
        "Bkg.StdDev",
        "Spot.StdDev",
        "Bkg.Sum",
        "Spot.Sum",
        "Bkg.Area",
        "Spot.Area",
        "Spot.Saturation",
        "Spot.Found",
        "Pos.Nom.X",
        "Pos.Nom.Y",
        "Spot.Diameter",
        "Well.Name",
        "Well.Row",
        "Well.Column",
        "Exposure.Id",
        "Analysis.Name",
    }

    assert set(result.columns) == columns
    assert result["Well.Name"][0] == "A01"
    assert result["Well.Row"][0] == "A"
    assert result["Well.Column"][0] == 1
    assert result["Exposure.Id"][0] == 1
    assert result["Analysis.Name"][0] == "mtp_wo_parameters"


def test_parse_file_raises_error(example_dir):
    from sensospot_parser.parser import parse_file

    csv_file = (
        example_dir / EXAMPLE_DIR_WITH_PARAMS / "should_raise_value_error.csv"
    )

    with pytest.raises(ValueError):
        parse_file(csv_file)


def test_parse_file_silenced_returns_data_frame(example_file):
    from sensospot_parser.parser import _parse_file_silenced

    result = _parse_file_silenced(example_file)

    assert result["Well.Row"][0] == "A"
    assert result["Well.Column"][0] == 1
    assert result["Exposure.Id"][0] == 1


def test_parse_file_silenced_returns_none_on_error(example_dir):
    from sensospot_parser.parser import _parse_file_silenced

    csv_file = (
        example_dir / EXAMPLE_DIR_WITH_PARAMS / "should_raise_value_error.csv"
    )

    result = _parse_file_silenced(csv_file)

    assert result is None


@pytest.mark.parametrize(
    "file_list",
    [
        [
            "160218_SG2-013-001_Regen1_Cy3-100_1_A1_1.csv",
            "160218_SG2-013-001_Regen1_Cy3-100_1_A1_2.csv",
        ],
        ["160218_SG2-013-001_Regen1_Cy3-100_1_A1_1.csv"],
    ],
)
def testparse_multiple_files_ok(example_dir, file_list):
    from sensospot_parser.parser import parse_multiple_files

    sub_dir = example_dir / EXAMPLE_DIR_WO_PARAMS
    files = [sub_dir / file for file in file_list]

    data_frame = parse_multiple_files(files)
    print(data_frame["Exposure.Id"].unique())

    assert len(data_frame) == 100 * len(files)
    assert len(data_frame["Exposure.Id"].unique()) == len(files)


def testparse_multiple_files_empty_file_list():
    from sensospot_parser.parser import parse_multiple_files

    with pytest.raises(ValueError):
        parse_multiple_files([])


def testparse_multiple_files_empty_array(example_dir):
    from sensospot_parser.parser import parse_multiple_files

    files = [example_dir / "no_array_A1_1.csv"]

    data_frame = parse_multiple_files(files)
    print(data_frame["Exposure.Id"].unique())

    assert len(data_frame) == 1


def test_find_csv_files(example_dir):
    from sensospot_parser.parser import find_csv_files

    result = list(find_csv_files(example_dir / EXAMPLE_DIR_WITH_PARAMS))

    assert len(result) == (36 * 3) + 1  # 36 wells, 3 exposure + one error file
    assert all(str(item).endswith(".csv") for item in result)
    assert all(not item.stem.startswith(".") for item in result)


def test_parse_folder(example_dir):
    from sensospot_parser.parser import parse_folder

    data_frame = parse_folder(example_dir / EXAMPLE_DIR_WITH_PARAMS)

    assert len(data_frame) == 36 * 3 * 100
    assert len(data_frame["Well.Row"].unique()) == 3
    assert len(data_frame["Well.Column"].unique()) == 12
    assert len(data_frame["Exposure.Id"].unique()) == 3
    assert len(data_frame["Pos.Id"].unique()) == 100
    assert len(data_frame["Parameters.Channel"].unique()) == 2
    assert len(data_frame["Parameters.Time"].unique()) == 3


def test_sanity_check_ok(example_dir):
    from sensospot_parser.parser import _sanity_check, parse_multiple_files

    sub_dir = example_dir / EXAMPLE_DIR_WO_PARAMS
    file_list = [
        "160218_SG2-013-001_Regen1_Cy3-100_1_A1_1.csv",
        "160218_SG2-013-001_Regen1_Cy3-100_1_A1_2.csv",
    ]
    files = [sub_dir / file for file in file_list]
    data_frame = parse_multiple_files(files)

    result = _sanity_check(data_frame)

    assert len(result) == len(data_frame)


def test_sanity_check_raises_value_error(example_dir):
    from sensospot_parser.parser import _sanity_check, parse_multiple_files

    sub_dir = example_dir / EXAMPLE_DIR_WO_PARAMS
    file_list = [
        "160218_SG2-013-001_Regen1_Cy3-100_1_A1_1.csv",
        "160218_SG2-013-001_Regen1_Cy3-100_1_A1_2.csv",
    ]
    files = [sub_dir / file for file in file_list]
    data_frame = parse_multiple_files(files)
    data_frame = data_frame.drop(data_frame.index[1])

    with pytest.raises(ValueError):
        _sanity_check(data_frame)
