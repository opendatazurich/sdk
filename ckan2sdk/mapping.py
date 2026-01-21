"""
Contains all mappings that are needed
"""

# Dict key is 'CLEAN key' and dict value is 'SDK key'
MAPPING_CLEAN_TO_SDK = {
    "author_email": None,
    "creator_user_id": None,
    "dataQuality": "DS-CP-DSWIRN", 
    "dataType": None,
    "dateFirstPublished": "DIST-CP-OGDEVD",
    "dateLastUpdated": "DIST-CP-OGDAD",
    "id": None,
    "isopen": None,
    "legalInformation": "Rechtsgrundlage", # derivedFrom (label)
    "license_id": "DIST-CP-OGDLIZ", 
    "license_title": None,
    "license_url": None,
    "maintainer": None, # "OGD_maintainer",
    "maintainer_email": None, # "OGD_maintainerEmail",
    "metadata_created": None,
    "metadata_modified": None,
    "name": "DIST-CP-OGDPACKNAME", 
    "notes": "description",
    "num_resources": None,
    "num_tags": None,
    "organization": None,
    "owner_org": None,
    "private": None,
    "spatialRelationship": "spatial",
    "sszBemerkungen": "DS-CP-DSWIBN", 
    "sszFields": None,
    "state": None,
    "temporalStart": "temporalStart",
    "temporalEnd": "temporalEnd",
    "title": "label",
    "type": None,
    "updateInterval": "accrualPeriodicity",
    # "url": "DIST-CP-OGDLIF",
    "datenlieferant": "DIST-CP-OGDLIF", # fuzzy matching
    "version": None,
    "extras": None,
    "groups": "DIST-CP-OGDKAT",
    "resources": None,
    "tags": "tags",
    "relationships_as_subject": None,
    "relationships_as_object": None,
    "attributes": "attributes",
    "author_dept_gs":"author_dept_gs", # not actually a field in SDK > for matching grobstruktur
    "author_da_gs":"author_da_gs", # not actually a field in SDK > for matching grobstruktur
    "ogd_dataset_url": "ogd_dataset_url",
    "attr_spoken": "label",
    "attr_descr": "description",
    "attr_tech": "CPS-CP-TFN",
}

# keep only entries where value is not None
MAPPING_CLEAN_TO_SDK = {key: value for key, value in MAPPING_CLEAN_TO_SDK.items() if value is not None}
