""" 
CKAN - CLEAN - SDK
"""
import libs.cleaner as cleaner
from libs.ckan_api import call_api
from mapping import MAPPING_CLEAN_TO_SDK
from libs.dataclasses.sdk import SDK

pdf = call_api(limit=100)

# 1. Clean CKAN dataset. i.e. author -> dept. & dienstab.

# TODO Clean CKAN dataframe
# pdf[['departement','dienstabteilung']] = pdf['author'].str.split(',',expand=True)

pdf['tags'] = cleaner.clean_tags(pdf['tags'])

# pdf['tags'] = pdf['tags'].apply(x)
# tags = [t for t in pdf['tags']]
# for tag in tags:
#     for t in tag:
#         print(t['name'])
#     break


# 2. Rename CKAN columns to SDK
pdf_sdk = pdf.rename(columns=MAPPING_CLEAN_TO_SDK)


# sdk_columns = [mapping_clean_to_sdk[value] for value in mapping_clean_to_sdk]
sdk_columns = SDK.__annotations__
for _, row in pdf_sdk.iterrows():

    item = SDK(**{key: row[key] for key in sdk_columns})

    print(item)
