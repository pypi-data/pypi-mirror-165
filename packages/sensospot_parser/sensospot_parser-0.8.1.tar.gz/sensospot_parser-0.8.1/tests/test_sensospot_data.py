""" testing the __ini__ file """


def test_import_api():
    from sensospot_parser import main  # noqa: F401
    from sensospot_parser import columns  # noqa: F401
    from sensospot_parser import parse_file  # noqa: F401
    from sensospot_parser import parse_folder  # noqa: F401
