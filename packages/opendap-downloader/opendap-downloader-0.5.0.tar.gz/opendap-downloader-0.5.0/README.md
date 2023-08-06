# OPeNDAP downloader

Library to facilitate data downloads from OPeNDAP services configured with a file size limitation.  

This module will check if your requested file has a size under or above the file size limitation. If the size is under this limit, the file will be downloaded. Otherwise, the module will split the file (over time coordinates) in many files respecting the size limitation and download them. If `output-file` option is given, all the downloaded files will be concatenated into one and then be removed.


## Installation

With `pip`:

```
pip install opendap-downloader
```

## Usage

### Command Line Interface (CLI)

Check-out usage and examples:

```
> opendap-downloader --help
Usage: opendap_downloader.py [OPTIONS]

  Downloads OPeNDAP dataset as NetCDF files taking into account the server
  data query limit.

  Example:

    opendap-downloader --dataset-url https://nrt.cmems-du.eu/thredds/dodsC/METOFFICE-GLO-SST-L4-NRT-OBS-SST-V2 --variable analysed_sst --variable sea_ice_fraction --temporal-subset 2021-01-01 2021-01-02 --geographical-subset 0.0 0.1 0.0 0.1

    opendap-downloader -u https://nrt.cmems-du.eu/thredds/dodsC/METOFFICE-GLO-SST-L4-NRT-OBS-SST-V2 -v analysed_sst -v sea_ice_fraction -t 2021-01-01 2021-01-02 -g 0.0 0.1 0.0 0.1  

Options:
  -u, --dataset-url TEXT          The full OPeNDAP dataset URL  [required]
  -v, --variable TEXT             Specify dataset variables
  -g, --geographical-subset <FLOAT RANGE FLOAT RANGE FLOAT RANGE FLOAT RANGE>...
                                  The geographical subset as minimal latitude,
                                  maximal latitude, minimal longitude and
                                  maximal longitude
  -t, --temporal-subset <DATETIME DATETIME>...
                                  The temporal subset as start datetime and
                                  end datetime
  -d, --depth-range <FLOAT RANGE FLOAT RANGE>...
                                  The depth range in meters, if depth is a dataset
                                  coordinate
  -o, --output-path PATH          The destination path for the downloaded
                                  files. Default is the current directory
                                  [required]
  -f, --output-file PATH          Concatenate the downloaded data in the given
                                  file name (under the output path)
  -l, --login TEXT
  --password TEXT
  --help
```

## Contribute

Follow [these instructions](CONTRIBUTING.md).
