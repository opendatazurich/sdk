"""
Contains filter variables for organization (Dienstabteilung, Departement)
Use names from _data/grobstruktur.json
"""

# Dienstabteilung/Organisationseinheit
AUTHOR_DA_GS_LIST = [
    "Amt für Zusatzleistungen zur AHV/IV (AZL)",
    "Bevölkerungsamt (BVA)",
    "Dienstabteilung Verkehr (DAV)",
    "Entsorgung + Recycling Zürich (ERZ)",
    "Elektrizitätswerk der Stadt Zürich (ewz)",
    # "Immobilien Stadt Zürich (IMMO)",
    "Organisation und Informatik (OIZ)", # no datasets not sure, if string correct
    "Sportamt (SPA)",
    # "Schulamt (SAM)",
    # "Tiefbauamt (TAZ)",
    # "Umwelt- und Gesundheitsschutz (UGZ)",
    "Verkehrsbetriebe (VBZ)",
    # "Wasserversorgung (WVZ)",
    # "Soziale Einrichtungen und Betriebe (SEB)",
]

# Departement
AUTHOR_DEPT_GS_LIST = [
    # "Sozialdepartement",
]


# 2.X Subset of Testdata (defined by Marco)
TEST_DATASETS = ["sid_stapo_hundebestand_od1001",
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