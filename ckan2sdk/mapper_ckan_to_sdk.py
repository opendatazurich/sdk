""" 
CKAN - CLEAN - SDK
"""

import pandas as pd
import libs.cleaner as cleaner
from libs.ckan_api import call_api
# from mapping import *
from interface.sdk import SDK

# 0. Call Api and fetch CKAN metadata
pdf = call_api(limit=1000)

# 1. Clean CKAN dataset. i.e. author -> dept. & dienstab.
pdf_cleaned_author = cleaner.split_dept_da(pdf['author'])
pdf = pd.concat([pdf,pdf_cleaned_author], axis=1)

res = cleaner.fuzzymatch_dep_da(pdf_cleaned_author, departement="author_dept", dienstabteilung="author_da", min_simularity=0.8)
pdf = pd.concat([pdf,res], axis=1)

pdf_cleaned_timerange = cleaner.split_timerange(pdf['timeRange'])
pdf = pd.concat([pdf,pdf_cleaned_timerange], axis = 1)
# pdf = pdf[['timeRange','temporalStart', 'temporalEnd' ]]

# writing out test output
pdf['name_prefix'] = pdf['name'].str.extract(r'([^_]*)')
pdf = pdf[['name','name_prefix','author', 'author_dept', 'author_da','author_dept_gs','author_da_gs', 'timeRange','temporalStart', 'temporalEnd' ]]
pdf = pdf[pdf['name_prefix'] != 'geo']

pdf.to_excel("cleaning_ckan_tocheck.xlsx", index=False)

# 2. Rename CKAN columns to SDK
pdf_sdk = pdf.rename(columns=MAPPING_CLEAN_TO_SDK)


# sdk_columns = [mapping_clean_to_sdk[value] for value in mapping_clean_to_sdk]
sdk_columns = SDK.__annotations__
for _, row in pdf_sdk.iterrows():

    item = SDK(**{key: row[key] for key in sdk_columns}).to_json()

    print(item)
