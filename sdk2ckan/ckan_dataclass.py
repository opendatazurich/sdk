"""
For reference: This is the current dataclass used for export - SDK to CKAN
"""
from dataclasses import dataclass, field
from typing import List, Optional

#
# CKAN Dataset
#
@dataclass
class Attribute:
    id: str
    name: str
    required: str = ""
    cardinality: str = ""

@dataclass
class Literals:
    id: str
    label: str
    code: Optional[str]
    shortText: Optional[str]
    stereotype: Optional[str]

@dataclass
class CKANDataset:
    id: str
    department: str
    service_department: str
    datenbestand: str
    dataQuality: Optional[str]
    dateFirstPublished: Optional[int]
    dateLastUpdated: Optional[int]
    # license_id: Optional[str]
    # license_title: Optional[str]
    # license_url: Optional[str]
    maintainer: Optional[str]
    maintainer_email: Optional[str]
    name: Optional[str]
    notes: Optional[str]
    spatialRelationship: Optional[str]
    sszBemerkungen: Optional[str]
    # sszFields: Optional[str]
    timeRange: Optional[str]
    timeRange: Optional[str]
    title: Optional[str]
    updateInterval: Optional[str]
    url: Optional[str]
    # extras: Optional[str]
    groups: Optional[str]
    tags: Optional[str]
    attributes: List[Attribute] = field(default_factory=list)
    legalInformation: List[Literals] = field(default_factory=list)