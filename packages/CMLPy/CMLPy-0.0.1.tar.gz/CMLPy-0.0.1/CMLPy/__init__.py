import pandas as pd

def rename_columns(df, additional_names=None):
    """
    Rename columns in a dataframe based on a pre-made dictionary.
    """
    rename_dict = {
        # Identifiers
        'id': 'ID',
        'name': 'Name',
        'desc_': 'Description',
        'desc2': 'Description 2',
        'category': 'Category',
        'cref': 'Customer',
        'stcode': 'Stock Code',
        'altcode': 'Alternative Code',
        'barcode': 'Barcode',
        'category': 'Category',
        'ptype': 'Product Type',
        'pgroup': 'Product Group',
        # Price and levels
        'tradeprice_1': 'Trade Price',
        'costsup1': 'Supplier Cost',
        'retprcround': 'Retail Price',
    }
    
    # Add additional names if provided
    if additional_names is not None:
        rename_dict.update(additional_names)
    
    # Rename columns
    df.rename(columns=rename_dict, inplace=True)
    
    # Return the dataframe
    return df
