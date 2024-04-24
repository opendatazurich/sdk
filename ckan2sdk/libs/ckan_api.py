import pandas as pd


def call_api(limit: int = None) -> pd.DataFrame:
    """
    Fetches data from the Stadt Zürich data portal API and returns it as a pandas DataFrame.

    The function constructs a URL for the API endpoint based on the provided `limit` parameter,
    which specifies the maximum number of rows to retrieve. If `limit` is None, all available data
    is retrieved from the API. The function sends a request to the API and retrieves the data in
    JSON format. It converts the JSON data into a pandas DataFrame and returns it.

    Args:
        limit (int, optional): The maximum number of rows to retrieve from the API. If None, all available data is retrieved.
            Defaults to None.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the retrieved data.
    """

    # api settings
    ckanurl = "https://data.stadt-zuerich.ch"

    # packetsearch liefert alle Attribute, resp. das ganze Datenmodell
    queryapi = f"{ckanurl}/api/3/action/package_search"

    if limit:
        queryapi += f"?rows={limit}"

    pdf = pd.read_json(queryapi)
    pdf = pd.DataFrame(pdf["result"]["results"])

    return pdf
