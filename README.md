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

TODO

## ckan2sdk

The ckan2sdk project contains .... TODO

### Existing scripts

#### [Exporting CKAN to DKUEL](https://github.com/opendatazurich/opendatazurich.github.io/blob/master/automation/ckan_to_dkuel.py)
Export CKAN metadata to CSVs for DK-ÜL import

Reads out metadata and does some reformating of certain ckan fields (attributes, date)

#### [Extractting CKAN attributes](https://github.com/opendatazurich/opendatazurich.github.io/blob/master/automation/ckan_attributes.py)
Extract STZH CKAN attributes to csv

#### [Mapping CKAN Organisation to ORGANIZATIONAL UNITS](https://github.com/opendatazurich/ckan-reporting-stzh/blob/master/ckan-reporting-stzh.py)
Mapping Metadata of Datenlieferant / Dataowner

## Contributors

* [@Marco](mailto:) 👨‍💻 
* [@Lorenz](mailto:) 👨‍💻 
* [@NielsHellinga](mailto:niels.hellinga@banian.ch) 👨‍💻 Data Engineer
