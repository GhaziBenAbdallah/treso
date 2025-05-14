import pandas as pd



df= pd.read_excel("data/t.xlsx")


print(df.head())


somme= df['SOLDECAUTION12'].sum()

# somme_reg= df['SOLDERG'].sum()

# somme_cau=somme= df['SOLDECAUTION'].sum()

def calculate_client_balance(df):
    """
    Calculate the total balance from specified columns in the DataFrame.
    
    Parameters:
    df (pandas.DataFrame): DataFrame containing the required columns
    
    Returns:
    float: Sum of specified columns for the first row, or None if columns are missing
    """
    # List of columns to sum
    columns = [
        'Solde03', 'SOLDERG03', 'Solde06', 'SOLDERG06', 
        'Solde12', 'SOLDERG12', 'SOLDERGAc', 'SoldeAc'
         
    ]
    
    # Check if all required columns exist in the DataFrame
    missing_columns = [col for col in columns if col not in df.columns]
    if missing_columns:
        print(f"Warning: The following columns are missing from the DataFrame: {missing_columns}")
        # Optionally, you can return None or handle missing columns differently
        # For now, we'll proceed by ignoring missing columns
    
    # Calculate the sum of specified columns for the first row
    try:
        total = df[columns].sum()
        return total
    except Exception as e:
        print(f"Error calculating sum: {e}")
        return None

# somme_df=calculate_client_balance(df)

# print(somme_df)
# print(somme_reg)
# print(somme_cau)

solde=df["SoldeAc"].sum()+df["SOLDERGAc"].sum() +df['SOLDECAUTIONAc'].sum()

print(solde)


import pandas as pd

def calculate_client_balance_sum(df):
    """
    Calculate the total balance by summing specified columns across all rows and adding them together.
    
    Parameters:
    df (pandas.DataFrame): DataFrame containing the required columns
    
    Returns:
    float: Sum of the sums of specified columns, or None if critical errors occur
    """
    # List of columns to sum
    columns = [
        'Solde03', 'SOLDERG03', 'Solde06', 'SOLDERG06', 
        'Solde12', 'SOLDERG12', 'SOLDERGAc', 'SoldeAc',
        'IMPACC', 'IMP03', 'IMP06', 'IMP12', 'debit_credit'
    ]
    
    # Check for missing columns
    missing_columns = [col for col in columns if col not in df.columns]
    if missing_columns:
        print(f"Warning: The following columns are missing from the DataFrame: {missing_columns}")
        # Proceed with available columns
    
    # Filter available columns
    available_columns = [col for col in columns if col in df.columns]
    
    if not available_columns:
        print("Error: No specified columns found in the DataFrame.")
        return None
    
    try:
        # Sum each column across all rows and then sum the results
        total = sum(df[col].sum() for col in available_columns)
        return total
    except Exception as e:
        print(f"Error calculating sum: {e}")
        return None

# Example usage

    # Calculate the balance
result = calculate_client_balance_sum(df)
if result is not None:
    print(f"Total Client Balance (sum of column sums): {result}")