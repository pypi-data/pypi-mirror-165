""" Column name definitions """

# original, unmodified column names
POS_X = "Pos.X"
POS_Y = "Pos.Y"
POS_NOM_X = "Pos.Nom.X"
POS_NOM_Y = "Pos.Nom.Y"
BKG_SUM = "Bkg.Sum"
BKG_AREA = "Bkg.Area"
BKG_MEAN = "Bkg.Mean"
BKG_MEDIAN = "Bkg.Median"
BKG_STDDEV = "Bkg.StdDev"
SPOT_SUM = "Spot.Sum"
SPOT_AREA = "Spot.Area"
SPOT_MEAN = "Spot.Mean"
SPOT_MEDIAN = "Spot.Median"
SPOT_STDDEV = "Spot.StdDev"

# replacement column names
POS_ID = "Pos.Id"
SPOT_FOUND = "Spot.Found"
SPOT_DIAMETER = "Spot.Diameter"
SPOT_SATURATION = "Spot.Saturation"

# some csv columns are just named poorly
CSV_RENAME_MAP = {
    " ID ": POS_ID,
    "Found": SPOT_FOUND,
    "Dia.": SPOT_DIAMETER,
    "Spot.Sat. (%)": SPOT_SATURATION,
}

# meta data extracted from filename and path
ANALYSIS_NAME = "Analysis.Name"
EXPOSURE_ID = "Exposure.Id"
WELL_NAME = "Well.Name"
WELL_ROW = "Well.Row"
WELL_COLUMN = "Well.Column"

# parsed measurement parameter information (optional, from parameters folder)
PARAMETERS_TIME = "Parameters.Time"
PARAMETERS_CHANNEL = "Parameters.Channel"


PARSED_DATA_COLUMN_SET = {
    ANALYSIS_NAME,
    WELL_NAME,
    WELL_ROW,
    WELL_COLUMN,
    EXPOSURE_ID,
    POS_X,
    POS_Y,
    POS_ID,
    POS_NOM_X,
    POS_NOM_Y,
    BKG_SUM,
    BKG_AREA,
    BKG_MEAN,
    BKG_MEDIAN,
    BKG_STDDEV,
    SPOT_SUM,
    SPOT_AREA,
    SPOT_MEAN,
    SPOT_FOUND,
    SPOT_MEDIAN,
    SPOT_STDDEV,
    SPOT_DIAMETER,
    SPOT_SATURATION,
    PARAMETERS_CHANNEL,
    PARAMETERS_TIME,
}

# list of columns to ensure a pandas numeric type
NUMERIC_COLUMNS = {
    POS_ID,
    WELL_COLUMN,
    EXPOSURE_ID,
    POS_X,
    POS_Y,
    POS_NOM_X,
    POS_NOM_Y,
    SPOT_SUM,
    BKG_SUM,
    BKG_MEAN,
    BKG_MEDIAN,
    BKG_STDDEV,
    SPOT_MEAN,
    SPOT_MEDIAN,
    SPOT_STDDEV,
    SPOT_DIAMETER,
    SPOT_SATURATION,
}


# set of columns where values are directly dependent on exposure time
EXPOSURE_DEPENDENT_COLUMNS = {
    BKG_SUM,
    BKG_MEAN,
    BKG_MEDIAN,
    BKG_STDDEV,
    SPOT_SUM,
    SPOT_MEAN,
    SPOT_MEDIAN,
    SPOT_STDDEV,
}

# common indexes
INDEX_COLUMNS_WELL = (
    ANALYSIS_NAME,
    WELL_NAME,
    WELL_ROW,
)

INDEX_COLUMNS_POS = (
    ANALYSIS_NAME,
    WELL_NAME,
    WELL_ROW,
    POS_ID,
)
