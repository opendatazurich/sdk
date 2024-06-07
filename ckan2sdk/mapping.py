"""
Contains all mappings that are needed
"""

# Dict key is 'CLEAN key' and dict value is 'SDK key'
MAPPING_CLEAN_TO_SDK = {
    "author_email": None,
    "creator_user_id": None,
    "dataQuality": "OGD_dataquality",
    "dataType": None,
    "dateFirstPublished": "OGD_firstPub",
    "dateLastUpdated": "ACTDATE",
    "id": None,
    "isopen": None,
    "legalInformation": None,
    "license_id": None,
    "license_title": None,
    "license_url": None,
    "maintainer": "OGD_maintainer",
    "maintainer_email": "OGD_maintainerEmail",
    "metadata_created": None,
    "metadata_modified": None,
    "name": "package_name",
    "notes": "description",
    "num_resources": None,
    "num_tags": None,
    "organization": None,
    "owner_org": None,
    "private": None,
    "spatialRelationship": "spatial",
    "sszBemerkungen": "BESCHBEM",
    "sszFields": None,
    "state": None,
    "temporalStart": "temporalStart",
    "temporalEnd": "temporalEnd",
    "title": "label",
    "type": None,
    "updateInterval": "accrualPeriodicity",
    "url": "OGD_dataProvider",
    "version": None,
    "extras": None,
    "groups": "DCAT",
    "resources": None,
    "tags": None,
    "relationships_as_subject": None,
    "relationships_as_object": None,
    "attributes": "attributes"
}

# keep only entries where value is not None
MAPPING_CLEAN_TO_SDK = {key: value for key, value in MAPPING_CLEAN_TO_SDK.items() if value is not None}
