# SDK

![poetry](https://img.shields.io/static/v1?label=package%20manager&message=poetry&color=blue)
![code style](https://img.shields.io/static/v1?label=code%20style&message=flask8&color=green)
![code style](https://img.shields.io/static/v1?label=contributers&message=3&color=red)

This project contains the mapper from CKAN to SDK (ckan2sdk)

## Prerequisites

Before you begin, ensure you have met the following requirements:

* You have installed the latest version of `poetry`

## Project Setup

Make sure poetry in installed correctly ->  `poetry --version`

Next, run
```bash
poetry install  # to install all dependencies
poetry shell    # to enter poetry environment
flake8 --append-config .flake8 # appends user defined formatting rules to flake8 default set
``` 

## sdk2ckan

Not done here, but in *OGD-Pipeline* on CMP (managed by Banian).

## ckan2sdk

The script takes metadata from OGD catalog and formats an Excel file that can be imported into SDK (dataspot). This is used for the *Initialimport* of OGD metadata in SDK.

**Usage**
Execute main script [mapping.py](ckan2sdk/mapper_ckan_to_sdk.py). The script:

- creates Excel Exports by organization (Dienstabteilung/Organisationseinheit)
- filters certain organizations for pioneer group
- excludes unwanted datasets (geo data oder ssz data)
- adds "Datenlieferant" in SDK format
- change field mapping to match the names of the SDK

**Parameters an helper scripts**
- [mapping.py](ckan2sdk/mapping.py): Contains all mappings that are needed, like column and value mappings for CKAN-SDK, or columns to export
- [filter_org.py](ckan2sdk/filter_org.py): Contains filter variables for organization (*Dienstabteilung*, *Departement*). Use names from [grobstruktur.json](_data/grobstruktur.json)
- [grobstruktur.json](_data/grobstruktur.json): Maps *Dienstabteilung* and *Departement* in correct spelling for SDK
- [ckan_api.py](ckan2sdk/libs/ckan_api.py): Helper functions for CKAN-API
- [cleaner.py](ckan2sdk/libs/cleaner.py): Helper functions for data cleaning and fuzzy-matching
- [exports.py](ckan2sdk/libs/exports.py): Helper functions for excel exports

### Existing scripts

#### [Exporting CKAN to DKUEL](https://github.com/opendatazurich/opendatazurich.github.io/blob/master/automation/ckan_to_dkuel.py)
Export CKAN metadata to CSVs for DK-ÜL import

Reads out metadata and does some reformating of certain ckan fields (attributes, date)

#### [Extractting CKAN attributes](https://github.com/opendatazurich/opendatazurich.github.io/blob/master/automation/ckan_attributes.py)
Extract STZH CKAN attributes to csv

#### [Mapping CKAN Organisation to ORGANIZATIONAL UNITS](https://github.com/opendatazurich/ckan-reporting-stzh/blob/master/ckan-reporting-stzh.py)
Mapping Metadata of Datenlieferant / Dataowner

## Contributors

* [@DonGoginho](mailto:marco.sieber@zuerich.ch) 👨‍💻 
* [@alexanderguentert](mailto:alexander.guentert@zuerich.ch) 👨‍💻
* [@debugair](mailto:stefan.kaspar@banian.ch) 👨‍💻
* [@lbo-dvlp](mailto:lorenz.bosshardt@zuerich.ch) 👨‍💻 Former Contributor
* [@NielsHellinga](mailto:niels.hellinga@banian.ch) 👨‍💻 Former Contributor
