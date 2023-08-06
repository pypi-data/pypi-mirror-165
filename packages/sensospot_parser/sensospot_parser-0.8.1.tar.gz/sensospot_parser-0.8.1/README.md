Sensospot Data Parser
=====================

Parsing the numerical output from [SensoSpot][sensospot] microarray analysis.

The [SensoSpot][sensospot] microarray analyzer is an automated fluorescence microscope with an image analysis software for detecting and measuring microarrays. The original name of the product was "FLAIR" by the company Sensovation, that was later acquired by Miltenyi. 

There is no affiliation on my side regarding Sensovation or Miltenyi, I just use the product and needed a way to make the data available for further analysis.


## Example:

```python

    import sensospot_parser

    # read the raw data of a folder
    raw_data = sensospot_parser.parse_folder(<path to results directory>)

    sorted(raw_data.columns) == [
        'Analysis.Name', 
        'Bkg.Area', 'Bkg.Mean', 'Bkg.Median', 'Bkg.StdDev', 'Bkg.Sum', 
        'Exposure.Id', 
        'Parameters.Channel', 'Parameters.Time', 
        'Pos.Id', 'Pos.Nom.X', 'Pos.Nom.Y', 'Pos.X', 'Pos.Y', 
        'Spot.Area', 'Spot.Diameter', 'Spot.Found', 'Spot.Mean', 'Spot.Median', 
        'Spot.Saturation', 'Spot.StdDev', 'Spot.Sum', 
        'Well.Column', 'Well.Name', 'Well.Row'
    ]
```

## Constants

There is a `columns` module available, providing constans that define the column names.

```python

    import sensospot_parser

    sensospot_parser.columns.ANALYSIS_NAME == "Analysis.Name"
```


## Avaliable public functions:

 - **parse_folder(path_to_folder)**
   Searches the folder for parsable Sensospot .csv files, parses them into one 
   big pandas data frame and will add additional meta data from parameters folder, 
   if it is present.
- **parse_file(path_to_csv_file)**
   Parses a Sensospot csv file into a pandas data frame and will add some additional
   meta data from the file name. Is internally also used by `parse_folder()`


## CLI

For the (propably) most important function, there is even a cli command
```sh
Usage: sensospot_parse [OPTIONS] SOURCE

Arguments:
  SOURCE:             Folder with Sensospot measurement

Options:
  -o, --outfile TEXT  Output file name, use a dash '-' for stdout, default:
                      'collected_data.csv'
  -q, --quiet         Ignore Sanity Check
  -r, --recurse       Recurse into folders one level down
  --help              Show this message and exit.
```

## Development

To install the development version of Sensovation Data Parser:

    git clone https://git.cpi.imtek.uni-freiburg.de/holgi/sensospot_data.git

    # create a virtual environment and install all required dev dependencies
    cd sensospot_data
    make devenv

To run the tests, use `make tests` (failing on first error) or `make coverage` for a complete report.


[sensospot]: https://www.miltenyi-imaging.com/products/sensospot