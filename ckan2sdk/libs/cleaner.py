import os

import pandas as pd

def clean_tags(pdf: pd.DataFrame) -> pd.DataFrame: 
    return pdf

def split_author(pdf: pd.DataFrame) -> pd.DataFrame:

    # splitting dataframe
    pdf_author = pd.DataFrame([i.split(",") for i in pdf["author"]], columns=["c0","c1","c2","c3","c4","c5"])

    # counting commas and splitting by commans
    pdf_commas = pd.DataFrame([i.count(",") for i in pdf["author"]],columns=["commas"])
    pdf_author = pd.concat([pdf_author,pdf_commas], axis=1)

    # assign values to 'dataowner_departement' and 'author_da'
    pdf_author.loc[pdf_author['commas'] == 0, 'author_dept'] = None
    pdf_author.loc[pdf_author['commas'] == 1, 'author_dept'] = pdf_author['c1']
    pdf_author.loc[pdf_author['commas'] == 2, 'author_dept'] = pdf_author['c2']
    pdf_author.loc[pdf_author['commas'] > 2, 'author_dept'] = None

    pdf_author.loc[pdf_author['commas'] == 0, 'author_da'] = None
    pdf_author.loc[pdf_author['commas'] == 1, 'author_da'] = pdf_author['c0']
    pdf_author.loc[pdf_author['commas'] == 2, 'author_da'] = pdf_author['c1']
    pdf_author.loc[pdf_author['commas'] > 2, 'author_da'] = None

    # trimming whitespace
    pdf_author['author_dept'] = pdf_author['author_dept'].str.strip()
    pdf_author['author_da'] = pdf_author['author_da'].str.strip()

    pdf_author = pd.concat([pdf_author,pdf], axis=1)
    pdf_author.drop(["commas","c0","c1","c2","c3","c4","c5"], inplace=True, axis=1)

    # These entries will get checked and (if necessary) cleaned in the original metadata source
    # pdf_author_check = pdf_author[(~pdf_author['author_dept'].isin(MAPPING_DEPT_DA.keys())) & (~pdf_author['author_da'].isin([item for sublist in MAPPING_DEPT_DA.values() for item in sublist]))]
    # pdf_author_check.to_excel("check_ogd.xlsx")

    # filtering
    pdf = pdf_author[(pdf_author['author_dept'].isin(MAPPING_DEPT_DA.keys())) & (pdf_author['author_da'].isin([item for sublist in MAPPING_DEPT_DA.values() for item in sublist]))]

    return pdf





