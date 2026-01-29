"""
Contains all mappings that are needed
"""

# Dict key is 'CLEAN key' and dict value is 'SDK key'
MAPPING_CLEAN_TO_SDK = {
    "author_email": None,
    "creator_user_id": None,
    "dataQuality": "Informationen oder Risiken, die bei der Nutzung zu beachten sind", 
    "dataType": None,
    "dateFirstPublished": "Erst-Veröffentlichungsdatum OGD",
    "dateLastUpdated": "Aktualisierungsdatum OGD",
    "id": None,
    "isopen": None,
    "legalInformation": "Rechtsgrundlagen", # derivedFrom (label)
    "license_id": "Lizenz", 
    "license_title": None,
    "license_url": None,
    "maintainer": None, # "OGD_maintainer",
    "maintainer_email": None, # "OGD_maintainerEmail",
    "metadata_created": None,
    "metadata_modified": None,
    "name": "Package Name", 
    "notes": "Beschreibung",
    "num_resources": None,
    "num_tags": None,
    "organization": None,
    "owner_org": None,
    "private": None,
    "spatialRelationship": "Geographisches Gebiet",
    "sszBemerkungen": "Weitere Bemerkungen zur Nutzung", 
    "sszFields": None,
    "state": None,
    "temporalStart": "Zeitraum - von",
    "temporalEnd": "Zeitraum - bis",
    "title": "Name",
    "type": None,
    "updateInterval": "Aktualisierungszyklus",
    # "url": "DIST-CP-OGDLIF",
    "datenlieferant": "Datenlieferant", # fuzzy matching
    "version": None,
    "extras": None,
    "groups": "OGD-Kategorie",
    "resources": None,
    "tags": "Schlüsselwörter",
    "relationships_as_subject": None,
    "relationships_as_object": None,
    "attributes": "attributes",
    "author_dept_gs":"author_dept_gs", # not actually a field in SDK > for matching grobstruktur
    "author_da_gs":"author_da_gs", # not actually a field in SDK > for matching grobstruktur
    "ogd_dataset_url": "ogd_dataset_url",
    "attr_spoken": "Fachlicher Attributname",
    "attr_descr": "Beschreibung",
    "attr_tech": "Technischer Feldname",
}

# keep only entries where value is not None
MAPPING_CLEAN_TO_SDK = {key: value for key, value in MAPPING_CLEAN_TO_SDK.items() if value is not None}
