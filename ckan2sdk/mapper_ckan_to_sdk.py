""" 
CKAN - CLEAN - SDK
"""
import re

import pandas as pd
import libs.cleaner as cleaner
from libs.ckan_api import call_api
from interface.sdk import SDK

# 0. Call Api and fetch CKAN metadata
pdf = call_api(limit=1000)

# 1. Clean CKAN dataset. i.e. author -> dept. & dienstab.
pdf_author = cleaner.split_dept_da(pdf['author'])
pdf_author = cleaner.fuzzymatch_dep_da(pdf_author, departement="author_dept", dienstabteilung="author_da", min_simularity=0.8)
pdf = pd.concat([pdf,pdf_author], axis=1) # concat to pdf

pdf_cleaned_timerange = cleaner.split_timerange(pdf['timeRange'])
pdf = pd.concat([pdf,pdf_cleaned_timerange], axis = 1)

pdf_name_prefix = cleaner.extract_name_prefix(pdf['name'])
pdf = pd.concat([pdf,pdf_name_prefix], axis = 1)

# 2. Rename CKAN columns to SDK
# pdf_sdk = pdf.rename(columns=MAPPING_CLEAN_TO_SDK)

# 3. Subset data (e.g. no geo datasets / no SSZ datasets etc.)
# ...

# Test export attributes
pdf_attributes = cleaner.create_attributes_export(pdf)
pdf_attributes = pd.merge(pdf_attributes, pdf[['name','author_dept_gs','author_da_gs','name_prefix']], how='left', on=['name'])
pdf_attributes = pdf_attributes[pdf_attributes['name_prefix'] != 'geo']

from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE
# pdf_attributes['attr_descr'] = pdf_attributes['attr_descr'].astype(str)
pdf_attributes['attr_descr'] = [ILLEGAL_CHARACTERS_RE.sub(r'',i) for i in pdf_attributes['attr_descr']]
pdf_attributes.to_excel("attributes_testexport.xlsx", index=False)

# Test export dataset-metadata
subset = ['name','name_prefix','author','author_dept_gs','author_da_gs', 'timeRange','temporalStart', 'temporalEnd']
pdf = pdf[subset]
pdf = pdf[pdf['name_prefix'] != 'geo']
pdf.to_excel("cleaning_ckan_tocheck.xlsx", index=False)


# sdk_columns = [mapping_clean_to_sdk[value] for value in mapping_clean_to_sdk]
sdk_columns = SDK.__annotations__
for _, row in pdf_sdk.iterrows():

    item = SDK(**{key: row[key] for key in sdk_columns}).to_json()

    print(item)
