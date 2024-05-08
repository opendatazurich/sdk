import pandas as pd
import re
from datetime import datetime
from mapping import *

def clean_tags(pdf: pd.DataFrame) -> pd.DataFrame: 
    return pdf

def split_author(pdf: pd.DataFrame) -> pd.DataFrame:
    """
    Splitting column 'author' in order to extract the departement and dienstabteilung

    The function splits the column author (metadata field from ckan) and extracts the deparement and dienstabteilung as well as the organisational unit.
    The extracted fields will get assigned to new columns.

    Args:
        pdf (pandas dataFrame): Pandas dataFrame as returned by call_api() function

    Returns:
        pd.DataFrame: A pandas DataFrame containing extracted fields as separate columns.
    """
    # splitting dataframe
    pdf_author = pd.DataFrame([i.split(",") for i in pdf], columns=["c0","c1","c2","c3","c4","c5"])

    # counting commas and splitting by commans
    pdf_commas = pd.DataFrame([i.count(",") for i in pdf],columns=["commas"])
    pdf_author = pd.concat([pdf_author,pdf_commas], axis=1)

    # assign values to 'dataowner_departement' and 'author_da'
    pdf_author.loc[pdf_author['commas'] == 5, 'author_dept'] = pdf_author['c5']
    pdf_author.loc[pdf_author['commas'] == 4, 'author_dept'] = pdf_author['c4']
    pdf_author.loc[pdf_author['commas'] == 3, 'author_dept'] = pdf_author['c3']
    pdf_author.loc[pdf_author['commas'] == 2, 'author_dept'] = pdf_author['c2']
    pdf_author.loc[pdf_author['commas'] == 1, 'author_dept'] = pdf_author['c1']
    pdf_author.loc[pdf_author['commas'] == 0, 'author_dept'] = pdf_author['c0']

    pdf_author.loc[pdf_author['commas'] == 5, 'author_da'] = pdf_author['c4']
    pdf_author.loc[pdf_author['commas'] == 4, 'author_da'] = pdf_author['c3']
    pdf_author.loc[pdf_author['commas'] == 3, 'author_da'] = pdf_author['c2']
    pdf_author.loc[pdf_author['commas'] == 2, 'author_da'] = pdf_author['c1']
    pdf_author.loc[pdf_author['commas'] == 1, 'author_da'] = pdf_author['c0']
    pdf_author.loc[pdf_author['commas'] == 0, 'author_da'] = None

    # trimming whitespace
    pdf_author['author_dept'] = pdf_author['author_dept'].str.strip()
    pdf_author['author_da'] = pdf_author['author_da'].str.strip()

    # dropping columns
    pdf_author.drop(["commas","c0","c1","c2","c3","c4","c5"], inplace=True, axis=1)

    # assigning author_org / cleaning author_dept and author_da
    pdf_author.loc[pdf_author['author_dept'].isin(MAPPING_DEPT_DA.keys()),'author_org'] = "Stadt Zürich"
    pdf_author.loc[~pdf_author['author_dept'].isin(MAPPING_DEPT_DA.keys()),'author_org'] = pdf_author['author_dept']
    pdf_author.loc[~pdf_author['author_dept'].isin(MAPPING_DEPT_DA.keys()),'author_dept'] = None
    pdf_author.loc[~pdf_author['author_da'].isin([item for sublist in MAPPING_DEPT_DA.values() for item in sublist]),'author_da'] = None

    return pdf_author

def split_timerange(pdf: pd.DataFrame) -> pd.DataFrame:
    """
    Splitting column 'timeRange' in order to extract the temporalStart and temporalEnd

    The function splits the column timeRange (metadata field from ckan) and extracts the temporalStart and temporalEnd.
    The extracted fields will get assigned to new columns.

    Args:
        pdf (pandas dataFrame): Pandas dataFrame as returned by call_api() function

    Returns:
        pd.DataFrame: A pandas DataFrame containing extracted fields as separate columns.
    """

    pdf_temporalStartEnd = pd.DataFrame()

    for i in range(len(pdf)):

        i_string = pdf.iloc[i]
        i_string = re.sub(r'\s+', '', i_string) # trimming all whitespace
        i_string = re.sub(r'–', '-', i_string) # replace hyphen with dash

        # matching exactly 4 digits
        if re.search(r'(^\d{4}$)', i_string):

            i_temp = re.search(pattern=r'(^\d{4}$)', string = i_string).group()
            i_temp = '31.12.' + i_temp
            i_temporalStart = i_temp
            i_temporalEnd = i_temp

        # matching single 'full' date format
        elif re.search(r'(^\d{2}\.\d{2}\.\d{4}$)', i_string):

            i_temp = re.search(pattern=r'(^\d{2}\.\d{2}\.\d{4}$)', string = i_string).group()
            i_temporalStart = i_temp
            i_temporalEnd = i_temp

        # matching everything with a dash
        elif re.search(r'-', i_string):

            i_temporalStart = re.search(pattern=r'^.*(?=-)', string=i_string).group()
            if re.search(r'(^\d{4}$)', i_temporalStart):
                i_temporalStart = re.search(pattern=r'(^\d{4}$)', string = i_temporalStart).group()
                i_temporalStart = '31.12.' + i_temporalStart
            elif re.search(r'(^\d{2}\.\d{2}\.\d{4}$)', i_temporalStart):
                i_temporalStart = re.search(pattern=r'(^\d{2}\.\d{2}\.\d{4}$)', string = i_temporalStart).group()
            else:
                i_temporalStart = None

            i_temporalEnd = re.search(pattern=r'(?<=-).+', string = i_string).group()
            if re.search(r'(^\d{4}$)', i_temporalEnd):
                i_temporalEnd = re.search(pattern=r'(^\d{4}$)', string = i_temporalEnd).group()
                i_temporalEnd = '31.12.' + i_temporalEnd
            elif re.search(r'(^\d{2}\.\d{2}\.\d{4}$)', i_temporalEnd):
                i_temporalEnd = re.search(pattern=r'(^\d{2}\.\d{2}\.\d{4}$)', string = i_temporalEnd).group()
            else:
                i_temporalEnd = None

        else:
            i_temporalStart = None
            i_temporalEnd = None


        i_pdf_temporalStartEnd = pd.DataFrame({'temporalStart': [i_temporalStart], 'temporalEnd': [i_temporalEnd]})
        pdf_temporalStartEnd = pd.concat([pdf_temporalStartEnd, i_pdf_temporalStartEnd])
        pdf_temporalStartEnd.reset_index(drop=True, inplace=True)

    return pdf_temporalStartEnd

def split_name(pdf: pd.DataFrame) -> pd.DataFrame:
    """
    Splitting column 'timeRange' in order to extract the temporalStart and temporalEnd

    The function splits the column timeRange (metadata field from ckan) and extracts the temporalStart and temporalEnd.
    The extracted fields will get assigned to new columns.

    Args:
        pdf (pandas dataFrame): Pandas dataFrame as returned by call_api() function

    Returns:
        pd.DataFrame: A pandas DataFrame containing extracted fields as separate columns.
    """


    return pdf
