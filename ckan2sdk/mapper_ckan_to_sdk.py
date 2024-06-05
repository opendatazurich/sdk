""" 
CKAN - CLEAN - SDK
"""
import re
import pandas as pd
import libs.cleaner as cleaner
from libs.ckan_api import call_api
from interface.sdk import SDK

import ckan2sdk.libs.
import libs.mapping as mapping

# 0. Call Api and fetch CKAN metadata
pdf = call_api(limit=1500)

# 1. Clean CKAN dataset. i.e. author -> dept. & dienstab.
pdf_author = cleaner.split_dept_da(pdf['author'])
pdf_author = cleaner.fuzzymatch_dep_da(pdf_author, departement="author_dept", dienstabteilung="author_da", min_simularity=0.8)
pdf = pd.concat([pdf,pdf_author], axis=1) # concat to pdf

pdf_cleaned_timerange = cleaner.split_timerange(pdf['timeRange'])
pdf = pd.concat([pdf,pdf_cleaned_timerange], axis = 1)

# TODO
# - cleaning groups
# - cleaning urls

# 2. Subset data (e.g. no geo datasets / no SSZ datasets etc.)
pdf['filter_tag'] = cleaner.create_filter_variable(pdf=pdf, matching_set={'sasa','geodaten'})
pdf = pdf[pdf['filter_tag']==False] # only entries which do not match defined matching_set

# 3. Rename CKAN columns to SDK
pdf_sdk = pdf.rename(columns=MAPPING_CLEAN_TO_SDK)

# check differences
# {*MAPPING_CLEAN_TO_SDK.keys()}.difference({*pdf.columns})
# {*pdf.columns}.difference({*MAPPING_CLEAN_TO_SDK.keys()})



# X. Export for checks
pdf_attributes = cleaner.create_attributes_export(pdf)
pdf_attributes = pd.merge(pdf_attributes, pdf[['name','author_dept_gs','author_da_gs','name_prefix']], how='left', on=['name'])
pdf_attributes = pdf_attributes[pdf_attributes['name_prefix'] != 'geo']

from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE
# pdf_attributes['attr_descr'] = pdf_attributes['attr_descr'].astype(str)
pdf_attributes['attr_descr'] = [ILLEGAL_CHARACTERS_RE.sub(r'',i) for i in pdf_attributes['attr_descr']]
pdf_attributes.to_excel("attributes_testexport.xlsx", index=False)

# Test export dataset-metadata
pdf['filter_tag'] = cleaner.create_filter_variable(pdf=pdf, matching_set={'sasa','geodaten'})
subset = ['name','name_prefix','author','author_dept_gs','author_da_gs', 'timeRange','temporalStart', 'temporalEnd','filter_tag']
pdf = pdf[subset]
pdf.to_excel("cleaning_ckan_tocheck.xlsx", index=False)


# sdk_columns = [mapping_clean_to_sdk[value] for value in mapping_clean_to_sdk]
sdk_columns = SDK.__annotations__
for _, row in pdf_sdk.iterrows():

    item = SDK(**{key: row[key] for key in sdk_columns}).to_json()

    print(item)
