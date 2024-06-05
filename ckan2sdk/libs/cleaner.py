import pandas as pd
import re
from mapping import *
import jaro
import calendar
from datetime import datetime
import json

def clean_tags(pdf: pd.DataFrame) -> pd.DataFrame: 
    return pdf

def split_dept_da(pdf: pd.Series) -> pd.DataFrame:
    """
    Splitting column 'author' in order to extract the departement and dienstabteilung

    The function splits the column author (metadata field from ckan) and extracts the deparement and dienstabteilung as well as the organisational unit.
    The extracted fields will get assigned to new columns.

    Args:
        pdf (pandas Series): Pandas dataFrame as returned by call_api() function

    Returns:
        pd.DataFrame: A pandas DataFrame containing extracted fields as separate columns.
    """

    # defining output column names
    output_column_dept = pdf.name + "_dept"
    output_column_da = pdf.name + "_da"
    output_column_org = pdf.name + "_org"

    # splitting dataframe
    pdf_author = pd.DataFrame([i.split(",") for i in pdf], columns=["c0","c1","c2","c3","c4","c5"])

    # counting commas and splitting by commas
    pdf_commas = pd.DataFrame([i.count(",") for i in pdf],columns=["commas"])
    pdf_author = pd.concat([pdf_author,pdf_commas], axis=1)

    # assign values to 'dataowner_departement' and 'author_da'
    pdf_author.loc[pdf_author['commas'] == 5, output_column_dept] = pdf_author['c5']
    pdf_author.loc[pdf_author['commas'] == 4, output_column_dept] = pdf_author['c4']
    pdf_author.loc[pdf_author['commas'] == 3, output_column_dept] = pdf_author['c3']
    pdf_author.loc[pdf_author['commas'] == 2, output_column_dept] = pdf_author['c2']
    pdf_author.loc[pdf_author['commas'] == 1, output_column_dept] = pdf_author['c1']
    pdf_author.loc[pdf_author['commas'] == 0, output_column_dept] = pdf_author['c0']

    pdf_author.loc[pdf_author['commas'] == 5, output_column_da] = pdf_author['c4']
    pdf_author.loc[pdf_author['commas'] == 4, output_column_da] = pdf_author['c3']
    pdf_author.loc[pdf_author['commas'] == 3, output_column_da] = pdf_author['c2']
    pdf_author.loc[pdf_author['commas'] == 2, output_column_da] = pdf_author['c1']
    pdf_author.loc[pdf_author['commas'] == 1, output_column_da] = pdf_author['c0']
    pdf_author.loc[pdf_author['commas'] == 0, output_column_da] = None

    # trimming whitespace
    pdf_author[output_column_dept] = pdf_author[output_column_dept].str.strip()
    pdf_author[output_column_da] = pdf_author[output_column_da].str.strip()

    # dropping columns
    pdf_author.drop(["commas","c0","c1","c2","c3","c4","c5"], inplace=True, axis=1)

    # # assigning author_org / cleaning author_dept and author_da
    # pdf_author.loc[pdf_author[output_column_dept].isin(MAPPING_DEPT_DA.keys()),output_column_org] = "Stadt Zürich"
    # pdf_author.loc[~pdf_author[output_column_dept].isin(MAPPING_DEPT_DA.keys()),output_column_org] = pdf_author[output_column_dept]
    # pdf_author.loc[~pdf_author[output_column_dept].isin(MAPPING_DEPT_DA.keys()),output_column_dept] = None
    # pdf_author.loc[~pdf_author[output_column_da].isin([item for sublist in MAPPING_DEPT_DA.values() for item in sublist]),output_column_da] = None

    return pdf_author

def fuzzymatch_dep_da(pdf: pd.DataFrame, departement: str, dienstabteilung: str, min_simularity: float) -> list:
    """
    Fuzzy-matching column departement and dienstabteilung to given grobstruktur

    The function fuzzy matches the columns departement and dienstabteilung, as extractet by split_dept_da() to the names given by grobstruktur.json
    The matched fields will get assigned to new columns.

    Args:
        pdf (pandas dataFrame): Pandas dataFrame as returned by call_api() function
        departement (str): Name of 'departement' column in pdf
        dienstabteilung (str): Name of 'dienstabteilung' column in pdf
        min_simularity (float): Minimum distance which should get considered when comparing strings (Jaro-Winkler metric)

    Returns:
        pd.DataFrame: A pandas DataFrame containing extracted fields as separate columns.
    """
    grobstruktur = pd.read_json("_data/grobstruktur.json")
    match_list_dep = []
    match_list_da = []

    for i in range(len(pdf)):

        i_dep = pdf.iloc[i][departement]
        i_da = pdf.iloc[i][dienstabteilung]

        if i_dep is None:
            i_dep = ""
        if i_da is None:
            i_da = ""

        # matching departement
        matches_dep = [jaro.original_metric(i_dep, i) for i in grobstruktur['departement'].unique()]

        if max(matches_dep) < min_simularity:
            match_dep = None
            match_da = None
        else:
            matches_dep_max_ind = matches_dep.index(max(matches_dep))
            match_dep = grobstruktur['departement'].unique()[matches_dep_max_ind]

            subset_da = [*grobstruktur[grobstruktur['departement'] == match_dep]['dienstabteilung']]
            matches_da = [jaro.original_metric(i_da, i) for i in subset_da]

            if max(matches_da) < min_simularity:
                match_da = None
            else:
                match_da_max_ind = matches_da.index(max(matches_da))
                match_da = subset_da[match_da_max_ind]

        match_list_dep.append(match_dep)
        match_list_da.append(match_da)

    col_dep = departement + "_gs"
    col_da = dienstabteilung + "_gs"
    pdf = pd.DataFrame({col_dep: match_list_dep, col_da: match_list_da})

    return pdf

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

    # general cleaning
    pdf = [re.sub(r'bis', '-', i) for i in pdf] # replace 'bis' with '-'
    pdf = [re.sub(r'ab ', 'seit ', i) for i in pdf] # replace 'ab' with 'seit'
    pdf = [re.sub(r'–', '-', i) for i in pdf] # replace hyphen with dash
    pdf = [re.sub(r'\s+', '', i) for i in pdf] # trimming all whitespace

    # replacing month by number wiht a dot '.'
    month_mapping = {
        'Januar': '01.',
        'Februar': '02.',
        'März': '03.',
        'April': '04.',
        'Mai': '05.',
        'Juni': '06.',
        'Juli': '07.',
        'August': '08.',
        'September': '09.',
        'Oktober': '10.',
        'November': '11.',
        'Dezember': '12.'
    }

    pattern = re.compile(r'(' + '|'.join(month_mapping.keys()) + r')')
    def replace_month(match):
        return month_mapping[match.group(0)]
    pdf = [pattern.sub(replace_month, i) for i in pdf]

    # looping all entries
    for i in range(len(pdf)):

        i_string = pdf[i]

        i_temporalStart = pd.NaT
        i_temporalEnd = pd.NaT

        # matching YYYY > exactly/only 4 digits
        if re.search(r'(^\d{4}$)', i_string):

            i_temp = re.search(r'(^\d{4}$)', string = i_string).group()
            i_temporalStart = datetime(int(i_temp), 12, 31)
            i_temporalEnd = i_temporalStart

        # matching (D)D.(M)M.YYYY > a only single 'full' date format
        elif re.search(r'(^\d{1,2}\.\d{1,2}\.\d{4}$)', i_string):

            i_temp = re.search(r'(^\d{1,2}\.\d{1,2}\.\d{4}$)', string = i_string).group()
            day, month, year = map(int, i_temp.split('.'))
            i_temporalStart = datetime(year, month, day)
            i_temporalEnd = i_temporalStart

        # matching everything with a dash '-'
        elif re.search(r'-', i_string):

            # replace seit/ab with empty string (since we have a dash anyway)
            i_string = re.sub(r'(seit|Seit|ab)', '', i_string)
            # everything before the dash > temporalStart
            i_temporalStart = re.search(r'^.*(?=-)', string=i_string).group()

            # matching four digits (YYYY)
            if re.search(r'(^\d{4}$)', i_temporalStart):
                i_temporalStart = re.search(r'(^\d{4}$)', string = i_temporalStart).group()
                i_temporalStart = datetime(int(i_temporalStart), 1, 1)

            # matching (D)D.(M)M.YYYY
            elif re.search(r'(^\d{1,2}\.\d{1,2}\.\d{4}$)', i_temporalStart):
                i_temporalStart = re.search(r'(^\d{1,2}\.\d{1,2}\.\d{4}$)', string = i_temporalStart).group()
                day, month, year = map(int, i_temporalStart.split('.'))
                i_temporalStart = datetime(int(year), int(month), int(day))

            # matching (M|MM).YYYY
            elif re.search(r'(^\d{1,2}\.\d{4}$)', i_temporalStart):
                i_temporalStart = re.search(r'(^\d{1,2}\.\d{4}$)', string = i_temporalStart).group()
                month, year = map(int, i_temporalStart.split('.'))
                i_temporalStart = datetime(int(year), int(month), 1)

            else:
                i_temporalStart = pd.NaT

            # everything after the dash > temporalEnd
            i_temporalEnd = re.search(r'(?<=-).+', string = i_string).group()

            # matching (YYYY) four digits
            if re.search(r'(^\d{4}$)', i_temporalEnd):
                i_temporalEnd = re.search(r'(^\d{4}$)', string = i_temporalEnd).group()
                i_temporalEnd = datetime(int(i_temporalEnd), 12, 31)

            # matching DD.MM.YYYY
            elif re.search(r'(^\d{1,2}\.\d{1,2}\.\d{4}$)', i_temporalEnd):
                i_temporalEnd = re.search(r'(^\d{1,2}\.\d{1,2}\.\d{4}$)', string = i_temporalEnd).group()
                day, month, year = map(int, i_temporalEnd.split('.'))
                i_temporalEnd = datetime(int(year), int(month), int(day))

            # matching (M|MM).YYYY
            elif re.search(r'(^\d{1,2}\.\d{4}$)', i_temporalEnd):
                month, year = map(int, i_temporalEnd.split('.'))
                day = calendar.monthrange(year, month)[1]
                i_temporalEnd = datetime(year, month, day)

            else:
                i_temporalEnd = pd.NaT

        # matching 'seit YYYY.'
        elif re.search(r'(seit)\d{4}', i_string):
            i_temporalStart = re.search(pattern=r'(?<=(seit))\d{4}', string=i_string).group()
            i_temporalStart = datetime(int(i_temporalStart), 1,1)
            i_temporalEnd = pd.NaT

        # matching '(seit)(MM.YYYY)'
        elif re.search(r'(seit)(\d{2}\.\d{4})', i_string):
            i_temporalStart = re.search(pattern=r'(?<=(seit))\d{2}\.\d{4}', string=i_string).group()
            month, year = map(int, i_temporalStart.split('.'))
            i_temporalStart = datetime(int(year), int(month),1)
            i_temporalEnd = pd.NaT

        # matching '(seit)(DD.MM.YYYY)'
        elif re.search(r'(seit)(\d{2}\.\d{2}\.\d{4})', i_string):
            i_temporalStart = re.search(pattern=r'(?<=(seit))\d{2}\.\d{2}\.\d{4}', string=i_string).group()
            day, month, year = map(int, i_temporalStart.split('.'))
            i_temporalStart = datetime(int(year), int(month),int(day))
            i_temporalEnd = pd.NaT

        # else:
        #     i_temporalStart = pd.NaT
        #     i_temporalEnd = pd.NaT

        i_pdf_temporalStartEnd = pd.DataFrame({'temporalStart': [i_temporalStart], 'temporalEnd': [i_temporalEnd]})
        pdf_temporalStartEnd = pd.concat([pdf_temporalStartEnd, i_pdf_temporalStartEnd])
        pdf_temporalStartEnd.reset_index(drop=True, inplace=True)

    return pdf_temporalStartEnd

def create_attributes_export(pdf: pd.DataFrame) -> pd.DataFrame:
    """
    Creates export object containing all attributes

    Creates export object containing splited and cleaned attributes
    The function mainly splits the column 'sszFiels' which lists all attributes in a dictionary like way. Each attribute is described in three ways:
    - A technical name (corresponds to the actual column name)
    - A spoken name (short description of technical name)
    - A description (describes the attribute

    The output object holds each attributes in a separate row, identified by the dataset's name

    Args:
        pdf (pandas dataFrame): Pandas dataFrame as returned by call_api() function
        The pdf must contain the columns 'sszFields' and 'name'

    Returns:
        pd.DataFrame: A pandas DataFrame containing extracted and cleaned fields as separate columns.
    """
    # initialising empty Output-DataFrame
    pdf_attributes = pd.DataFrame()

    for i in range(len(pdf)):

        i_name = pdf.iloc[i]['name']
        i_attr = pdf.iloc[i]['sszFields']

        if i_attr != '':

            # read/evaluate string with list in list > gives back attr_spoken and attr_descr
            i_attr = pd.DataFrame(json.loads(i_attr), columns=['attr_spoken','attr_descr'])

            # read out attr_tech (word after last space) / clean extractet string
            # i_attr['attr_tech'] = [re.search(r'(?<=\s)[^\s]*$', string = i).group() if re.search(r'(?<=\s)[^\s]*$', string = i) else '' for i in i_attr['attr_spoken']]
            i_attr['attr_tech'] = [re.search(r'\(technisch:(.*)', string = i).group() if re.search(r'\(technisch:(.*)', string = i) else '' for i in i_attr['attr_spoken']]
            i_attr['attr_tech'] = [re.sub(r'\(technisch: ', '', i) if re.search(r'\(technisch: ', i) else '' for i in i_attr['attr_tech']] # replace closing paranthesis
            # i_attr['attr_tech'] = [re.sub(r'\)\b', '', i) if re.search(r'\)\b', i) else '' for i in i_attr['attr_tech']] # replace closing paranthesis
            i_attr['attr_tech'] = [re.sub(r'\)$', '', i) for i in i_attr['attr_tech']] # replace closing paranthesis

            # extract attr_spoken i.e. everything before last opening paranthesis / clean extractet string
            i_attr['attr_spoken'] = [re.search(r'^[^(]+', string = i).group() for i in i_attr['attr_spoken']]
            i_attr['attr_spoken'] = [re.sub(r'\s+', '', i) for i in i_attr['attr_spoken']]

        else:
            i_attr = pd.DataFrame({'attr_tech': [None],'attr_spoken': [None],'attr_spoken': [None]})

            # add identifier of attributes

        # adding name
        i_attr['name'] = i_name

        # concatenate and assign column type...
        pdf_attributes = pd.concat([pdf_attributes, i_attr])
        pdf_attributes['attr_descr'] = pdf_attributes['attr_descr'].astype(str)
        pdf_attributes['attr_tech'] = pdf_attributes['attr_tech'].astype(str)
        pdf_attributes['attr_spoken'] = pdf_attributes['attr_spoken'].astype(str)


    return pdf_attributes

def extract_name_prefix(pdf: pd.DataFrame) -> pd.DataFrame:
    """
    Extract name prefix

    The function extracts the prefix of the name (everything before the first '_'

    Args:
        pdf (pandas dataFrame): Pandas dataFrame as returned by call_api() function

    Returns:
        pd.DataFrame: A pandas DataFrame containing extracted field as separate columns.
    """

    pdf_name_prefix = pdf.str.extract(r'([^_]*)')
    pdf_name_prefix.columns = ['name_prefix']

    return pdf_name_prefix

def create_filter_variable(pdf: pd.DataFrame, matching_set = {'sasa','geodaten'}) -> pd.DataFrame:
    """
    Creates filter variable based on given set of strings    >>>   based on tags (which are in dictionary in pdf column) according to given set of strings

    The function creates a boolean filter variable based on given set of strings which match with tags in the tag column (which are stored as dictionary)

    Args:
        pdf (pandas dataFrame): Pandas dataFrame as returned by call_api() function

    Returns:
        list: List with boolean values indicating if matching set matches any tags dictionary or not
    """

    res_list = []
    for i in range(len(pdf)):

        i_tags = pdf.iloc[i]['tags']
        i_tags = {i['display_name'] for i in i_tags}
        if len(matching_set & i_tags) > 0:
            i_back = True
        else:
            i_back = False
        res_list.append(i_back)

    return(res_list)
