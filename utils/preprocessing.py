import pandas as pd


def transform_data_to_quarterly(data):
    """
    Transforms the JSON data into a list of dictionaries with the format:
    ['company_website', 'quarter', 'number_of_visits'].
    
    Parameters:
    - data: JSON object containing meta information and visits data.
    
    Returns:
    - A list of dictionaries with 'company_website', 'quarter', and 'number_of_visits'.
    """
    
    # Extract relevant data
    company_website = data['meta']['request']['domain']
    visits_data = data['visits']
    
    # Convert visits data to a DataFrame
    df = pd.DataFrame(visits_data)
    
    # Convert 'date' column to datetime and calculate the quarter
    df['date'] = pd.to_datetime(df['date'])
    df['quarter'] = df['date'].dt.to_period('Q')
    
    # Aggregate visits by quarter
    quarterly_data = df.groupby('quarter')['visits'].sum().reset_index()
    quarterly_data.rename(columns={'visits': 'number_of_visits'}, inplace=True)
    
    # Add company_website column
    quarterly_data['company_website'] = company_website
    
    # Reorder columns
    result = quarterly_data[['company_website', 'quarter', 'number_of_visits']]
    
    # Convert to list of dictionaries
    result_list = result.to_dict(orient='records')
    
    return result_list


def preprocess_pdl_enrichment(data):

    # Attempt to create a DataFrame with the main JSON structure
    df_enrich = pd.DataFrame([data])  # Wrap in a list to create a single-row DataFrame
    
    # Extract additional fields if present in the 'location' key
    if 'location' in data:
        df_enrich['country'] = data['location'].get('country', None)
        df_enrich['locality'] = data['location'].get('locality', None)
    else:
        df_enrich['country'] = None
        df_enrich['locality'] = None

    return df_enrich

def preprocess_predict_leads_details(data):
    return data['data'][0]['attributes']

def preprocess_financing(data):
    return data['data']


def preprocess_harmonic(data):
    """
    Extracts unique investors name from the Harmonic harmonic_details table .
    
    Parameters:
    - funding_data: Dictionary containing funding information including investors.
    
    Returns:
    - A list of unique names from the investors.
    """
    # Extract the list of investors
    funding_data = data["funding"]
    investors = funding_data.get("investors", [])
    
    # Extract unique names using a set for deduplication
    unique_names = {investor.get("name") for investor in investors if "name" in investor}

    urn = data['requested_entity_urn']
    
    # Convert the set back to a list
    return list(unique_names), urn
