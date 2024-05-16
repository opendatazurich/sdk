""" 
CKAN - CLEAN - SDK
"""
import pandas as pd
import libs.cleaner as cleaner
from libs.ckan_api import call_api
from mapping import *
from interface.sdk import SDK

pdf = call_api(limit=1000)

# 1. Clean CKAN dataset. i.e. author -> dept. & dienstab.
pdf_cleaned_author = cleaner.split_dept_da(pdf['author'])
pdf = pd.concat([pdf,pdf_cleaned_author], axis=1)


pdf_cleaned_datenlieferant = cleaner.split_dept_da(pdf['url'])

pdf_cleaned_timerange = cleaner.split_timerange(pdf['timeRange'])
pdf = pd.concat([pdf,pdf_cleaned_timerange], axis = 1)


# writing out test output
# pdf['name_prefix'] = pdf['name'].str.extract(r'([^_]*)')
# pdf = pdf[['name','name_prefix','author', 'author_dept', 'author_da', 'author_org','timeRange','temporalStart','temporalEnd']]
# pdf.to_excel("cleaning_ckan_test.xlsx")

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

    item = SDK(**{key: row[key] for key in sdk_columns}).to_json()

    print(item)
