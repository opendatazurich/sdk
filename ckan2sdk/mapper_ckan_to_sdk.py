""" 
CKAN - CLEAN - SDK
"""

import pandas as pd
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE
import libs.cleaner as cleaner
from libs.ckan_api import call_api
from libs.exports import *
from interface.sdk import SDK
import mapping as mapping
from filter_org import *

# constants
CKAN_BASE_URL = "https://data.stadt-zuerich.ch"
GROUP_SEPERATOR = "\n" # the groups in the excel cell are seperated by this

# 0. Call Api and fetch CKAN metadata to pdf
pdf = call_api(CKAN_BASE_URL, limit=1500)

# 1. Clean CKAN dataset. i.e. author -> dept. & dienstab.
pdf_author = cleaner.split_dept_da(pdf['author']) # splitting author
pdf_author = cleaner.fuzzymatch_dep_da(pdf_author, departement="author_dept", dienstabteilung="author_da", min_simularity=0.8) # fuzzy match author_dept and author_da to grobstruktur
pdf = pd.concat([pdf,pdf_author], axis=1) # concat to pdf
print("Qualitätssicherung. Keine Dienstabteilung gefunden für diese Data Owner: ...")
print(pdf.loc[pdf["author_da_gs"].isna(),"author"].sort_values().unique())
print("-"*100)

# datenlieferant -> dept. & dienstab.
pdf_datenlieferant = cleaner.split_dept_da(pdf['url']) # splitting author
pdf_datenlieferant = cleaner.fuzzymatch_dep_da(pdf_datenlieferant, departement="url_dept", dienstabteilung="url_da", min_simularity=0.8) # fuzzy match author_dept and author_da to grobstruktur
pdf["datenlieferant"] = pdf_datenlieferant["url_da_gs"] + ", " + pdf_datenlieferant["url_dept_gs"] 
print("Qualitätssicherung. Keine Dienstabteilung gefunden für diese Datenlieferanten (verwende Original): ...")
print(pdf.loc[pdf["datenlieferant"].isna(),"url"].sort_values().unique())
print("-"*100)
# fill not matched values with original
pdf["datenlieferant"] = pdf["datenlieferant"].fillna(pdf['url'])

pdf['updateInterval'] = cleaner.unlist_first_element(pdf['updateInterval'])  # unlist field updateInterval
pdf['updateInterval'] = pdf['updateInterval'].replace(mapping.SDK_EXCEL_UPDATE_INTERVALL)

# SDK readable licence
pdf['license_id'] = pdf['license_id'].replace(mapping.SDK_EXCEL_LICENCE)

pdf_cleaned_timerange = cleaner.split_timerange(pdf['timeRange']) # split field timeRange
pdf = pd.concat([pdf,pdf_cleaned_timerange], axis = 1) # concat newly created fields to pdf
# pdf['temporalStart'] = cleaner.date_to_unixtime(pdf['temporalStart']) # change to unix time
# pdf['temporalEnd'] = cleaner.date_to_unixtime(pdf['temporalEnd']) # change to unix time

pdf['dateLastUpdated'] = pd.Series(cleaner.extract_date(pdf['dateLastUpdated']))
# pdf['dateLastUpdated'] = cleaner.date_to_unixtime(pdf['dateLastUpdated'])
pdf['dateFirstPublished'] = pd.Series(cleaner.extract_date(pdf['dateFirstPublished']))
# pdf['dateFirstPublished'] = cleaner.date_to_unixtime(pdf['dateFirstPublished'])

pdf['groups'] = cleaner.extract_keys(pdf=pdf['groups'], key_to_extract="display_name", new_key_name="group")
pdf["groups"] = pdf["groups"].apply(cleaner.flatten_json,field="group", sep=GROUP_SEPERATOR)
# group string contain invisible characters. Remove them
pdf["groups"] = pdf["groups"].apply(cleaner.remove_invisible, keep=(GROUP_SEPERATOR))

# filter variable for unwanted datasets
# True sind die, die wir nicht wollen
pdf['filter_tag'] = (
    # wir wollen keine Geodaten
    pdf['tags'].apply(cleaner.contains_excluded_tags, tags_to_exclude=["geodaten"]) |
    # wir wollen keine DataOwner, die nicht in der Stadt sind
    pdf['author_da_gs'].isna() | 
    # wir wollen SASA, aber nicht, wenn SSZ oder BVA die Owner sind
    (pdf['tags'].apply(cleaner.contains_excluded_tags, tags_to_exclude=["sasa"]) & pdf["author_da_gs"].isin(["Statistik Stadt Zürich (SSZ)", "Bevölkerungsamt (BVA)"]))
)

pdf['tags'] = cleaner.extract_keys(pdf=pdf['tags'], key_to_extract="name", new_key_name="tag")
pdf["tags"] = pdf["tags"].apply(cleaner.flatten_json, field="tag", sep="\n")

pdf['attributes'] = cleaner.clean_attributes(pdf['sszFields'])

# add name_prefix
pdf['name_prefix'] = pdf['name'].str.split('_',expand=True)[0]


# 2. Subset data (e.g. no geo datasets / no SSZ datasets etc.) > set filter variable
pdf = pdf[pdf['filter_tag']==False] # only entries which do not match defined matching_set

# 2.1 filter data for onboarding workshops

pdf = pdf[(pdf['author_da_gs'].isin(AUTHOR_DA_GS_LIST))|(pdf['author_dept_gs'].isin(AUTHOR_DEPT_GS_LIST))]

# add OGD catalogue url
pdf["ogd_dataset_url"] = CKAN_BASE_URL + "/dataset/" +pdf["name"]


# Spezial distributions for SDK Import Excel
pdf["dist_type"] = "OGD"
pdf["dist_of"] = pdf["title"]
pdf["dist_name"] = "OGD"
pdf["dist_format"] = "CSV"


pdf_sdk = pdf

# 3. Rename CKAN columns to SDK
pdf_sdk = pdf_sdk[pdf_sdk.columns.intersection(mapping.MAPPING_CLEAN_TO_SDK.keys())] # subsetting cols. Comment out if you want all cols
pdf_sdk = pdf_sdk.rename(columns=mapping.MAPPING_CLEAN_TO_SDK)
# add empty columns on the left for Attributskollektion (to be filled by data owners)
empty_col_names = ["SDK Datenbestand-Sammlung", "SDK Datenbestand", "SDK Datensatz-Sammlung"]
for col in empty_col_names:
    pdf_sdk.insert(0, col, pd.NA)


# 4. Testexports
output_dir = "output"
# 4.1 Testexport for Nils (Initialimport)
# testexport_json(pdf_sdk, "testexport_10datasets.json", output_dir)
export_to_excel(pdf_sdk, "initialimport_datasets.xlsx", output_dir)


# 4.3 Testexport for attributes for checks
pdf_attributes = cleaner.create_attributes_export(pdf)
pdf_attributes = pd.merge(pdf_attributes, pdf[['name','title','author_dept_gs','author_da_gs','name_prefix']], how='left', on=['name'])
# replace illegal chars for excel
pdf_attributes['attr_descr'] = [ILLEGAL_CHARACTERS_RE.sub(r'',i) for i in pdf_attributes['attr_descr']]
# rename col names according to mapping
pdf_attributes = pdf_attributes.rename(columns=mapping.MAPPING_CLEAN_TO_SDK)
# rename für SDK Excel
pdf_attributes = pdf_attributes.rename(columns={"Name": "Bestandteil von"})
# add sorting for SDK Excel
pdf_attributes["Nr"] = pdf_attributes.groupby("Bestandteil von").cumcount().add(1)

# add empty column on the left for Attributskollektion (to be filled by data owners)
#pdf_attributes['Attributskollektion'] = pd.NA
pdf_attributes.insert(0, 'Attributskollektion', pd.NA)


########## Hardcoded fpr testimport. DO NOT USE IN PROD!!!!!
pdf_sdk["Sammlung"] = "Präsidialdepartement/Statistik Stadt Zürich (SSZ)/Test-Datenbestand"
pdf_attributes["Besteht aus"] = "/Semantik/StatZone/StatZoneCd"
########## 

export_to_excel(pdf_attributes, "initialimport_attribute.xlsx", output_dir)

export_to_excel_sdk_style(pdf_sdk, pdf_attributes,
                          dataset_cols=mapping.SDK_EXCEL_DATASET_COLNAMES, 
                          attribute_cols=mapping.SDK_EXCEL_ATTRIBUTES_COLNAMES, 
                          distributions_cols=mapping.SDK_EXCEL_DISTRIBUTIONS_COLNAMES,
                          filename="initialimport.xlsx", org_col="author_da_gs", output_dir=output_dir)


