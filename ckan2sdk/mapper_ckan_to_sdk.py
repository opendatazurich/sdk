""" 
CKAN - CLEAN - SDK
"""

import pandas as pd
import libs.cleaner as cleaner
from libs.ckan_api import call_api
from interface.sdk import SDK
import mapping as mapping

# 0. Call Api and fetch CKAN metadata
pdf = call_api(limit=1500)

# 1. Clean CKAN dataset. i.e. author -> dept. & dienstab.
pdf_author = cleaner.split_dept_da(pdf['author'])
pdf_author = cleaner.fuzzymatch_dep_da(pdf_author, departement="author_dept", dienstabteilung="author_da", min_simularity=0.8)
pdf = pd.concat([pdf,pdf_author], axis=1) # concat to pdf

pdf['updateInterval'] = cleaner.unlist_first_element(pdf['updateInterval'])

pdf_cleaned_timerange = cleaner.split_timerange(pdf['timeRange'])
pdf = pd.concat([pdf,pdf_cleaned_timerange], axis = 1)
pdf['temporalStart'] = cleaner.date_to_unixtime(pdf['temporalStart'])
pdf['temporalEnd'] = cleaner.date_to_unixtime(pdf['temporalEnd'])

pdf['dateLastUpdated'] = pd.Series(cleaner.extract_date(pdf['dateLastUpdated']))
pdf['dateLastUpdated'] = cleaner.date_to_unixtime(pdf['dateLastUpdated'])
pdf['dateFirstPublished'] = pd.Series(cleaner.extract_date(pdf['dateFirstPublished']))
pdf['dateFirstPublished'] = cleaner.date_to_unixtime(pdf['dateFirstPublished'])

pdf['groups'] = cleaner.extract_keys(pdf=pdf['groups'], key_to_extract="name", new_key_name="group")

pdf['filter_tag'] = cleaner.create_filter_variable(pdf=pdf, matching_set={'sasa','geodaten'})

pdf['tags'] = cleaner.extract_keys(pdf=pdf['tags'], key_to_extract="name", new_key_name="tag")

pdf['attributes'] = cleaner.clean_attributes(pdf['sszFields'])

# 2. Subset data (e.g. no geo datasets / no SSZ datasets etc.)
# pdf['filter_tag'] = cleaner.create_filter_variable(pdf=pdf, matching_set={'sasa','geodaten'})
# pdf = pdf[pdf['filter_tag']==False] # only entries which do not match defined matching_set


# 2.X Subset of Testdata (defined by Marco)
test_datasets = ["sid_stapo_hundebestand_od1001",
                 "sid_wipo_gastwirtschaftsbetriebe",
                 # "ted_taz_verkehrszaehlungen_werte_fussgaenger_velo", # Metadata in CKAN need to be adapted for matching with grobstruktur
                 "vbz_fahrgastzahlen_ogd",
                 "gud_ds_altersbefragung",
                 "ugz_meteodaten_tagesmittelwerte",
                 "ewz_stromabgabe_netzebenen_stadt_zuerich",
                 "sd_sod_sozialhilfequote",
                 "parlamentsdienste_paris_api",
                 "prd_sar_schauspielhaus_repertoire",
                 "zt_nachtleben"]

pdf_sdk = pdf[pdf['name'].isin(test_datasets)]

# 3. Rename CKAN columns to SDK
pdf_sdk = pdf_sdk[mapping.MAPPING_CLEAN_TO_SDK.keys()]
pdf_sdk = pdf_sdk.rename(columns=mapping.MAPPING_CLEAN_TO_SDK)

# X. Testexport for Nils
pdf_sdk.to_json("testexport_10datasets.json", orient='records', default_handler=str)

# X. Testexport for Marco
subset = ['name','author','author_dept_gs','author_da_gs', 'timeRange','temporalStart', 'temporalEnd','filter_tag']
pdf = pdf[subset]
pdf.to_excel("cleaning_ckan_tocheck_240610.xlsx", index=False)

# X. Testexport for attributes for checks
pdf_attributes = cleaner.create_attributes_export(pdf)
pdf_attributes = pd.merge(pdf_attributes, pdf[['name','author_dept_gs','author_da_gs','name_prefix']], how='left', on=['name'])
pdf_attributes = pdf_attributes[pdf_attributes['name_prefix'] != 'geo']

from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE
pdf_attributes['attr_descr'] = [ILLEGAL_CHARACTERS_RE.sub(r'',i) for i in pdf_attributes['attr_descr']]
pdf_attributes.to_excel("attributes_testexport.xlsx", index=False)

# sdk_columns = [mapping_clean_to_sdk[value] for value in mapping_clean_to_sdk]
sdk_columns = SDK.__annotations__
for _, row in pdf_sdk.iterrows():
    item = SDK(**{key: row[key] for key in sdk_columns}).to_json()
    print(item)

