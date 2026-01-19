import pandas as pd
import os
import re

def testexport_json(df: pd.DataFrame, filename="testexport_datasets.json", output_dir: str = "."):
    # 4.1 Testexport for Nils (Initialimport)
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, filename)
    print('write json', path)
    df.to_json(path, orient='records', default_handler=str)


def export_to_excel(df: pd.DataFrame, filename="initialimport.xlsx", output_dir: str = "."):
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, filename)
    print("write excel", path)
    df.to_excel(path, index=False)

def export_to_excel_by_org(df_dataset: pd.DataFrame, df_attribues: pd.DataFrame, filename="initialimport.xlsx", org_col="author_da_gs", output_dir: str = "."):
    """
    Creates an excel file for every unique organization (e.g. dienstabteilung)
    which contains a sheet for datasets and attribues
    
    :param df_dataset: df with dataset info. Needs to have a org_col
    :type df_dataset: pd.DataFrame
    :param df_attribues: df with attribues info. Needs to have a org_col
    :type df_attribues: pd.DataFrame
    :param filename: End of the filename (gets a prefix from org_col)
    :param org_col: Column name the specifies the dienstabteilung
    """
    
    if org_col not in df_dataset.columns:
        raise ValueError(f"Column '{org_col}' missing in df_dataset.")
    if org_col not in df_attribues.columns:
        raise ValueError(f"Column '{org_col}' missing in df_attribues.")
    
    
    # Hilfsfunktion: Dateinamen-sicherer Org-String
    def _sanitize_filename_part(s: str) -> str:
        s = s.strip()
        # Ungültige Dateisystem-Zeichen ersetzen
        s = re.sub(r'[\\/*?:"<>|]+', "_", s)
        # Windows-reservierte Namen vermeiden
        reserved = {"CON", "PRN", "AUX", "NUL"} | {f"COM{i}" for i in range(1, 10)} | {f"LPT{i}" for i in range(1, 10)}
        if s.upper() in reserved:
            s = f"_{s}_"
        # Nicht-leer
        return s if s else "org"

    os.makedirs(output_dir, exist_ok=True)

    written_files = []

    orgs = df_dataset[org_col].unique()
    for org in orgs:
        org_safe = _sanitize_filename_part(str(org))
        filename_org = f"{org_safe}_{filename}"
        path = os.path.join(output_dir, filename_org)
        df_dataset_org = df_dataset[df_dataset[org_col]==org]
        df_attribues_org = df_attribues[df_attribues[org_col]==org]
        print("write", path)
        with pd.ExcelWriter(path, engine="openpyxl") as writer:
            df_dataset_org.to_excel(writer, sheet_name="datasets", index=False)
            df_attribues_org.to_excel(writer, sheet_name="attributes", index=False)
        written_files.append(path)

    return written_files



if __name__ == "__main__":

    df_dataset = pd.DataFrame({"author_da_gs": ["Tiefbauamt (TAZ)", "Verkehrsbetriebe (VBZ)", "Verkehrsbetriebe (VBZ)", "Entsorgung + Recycling Zürich (ERZ)"]})
    export_to_excel_by_org(df_dataset, pd.DataFrame())