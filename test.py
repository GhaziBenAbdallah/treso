# import pandas as pd

# from datetime import datetime


# from database.queries_mas import get_encaissemnet_prevu ,get_client_reel_encaissement


# current_month = datetime.now().month
# current_year=datetime.now().year
# # Function to extract specific columns for a given month and year
# def extract_specific_month_year_data(df: pd.DataFrame, month: int, year: int) -> pd.DataFrame:
#     """
#     Extract rows from a DataFrame for a specific month and year, returning only
#     the columns Code_Chantier, ANNEE, Montant, Type, Tiers_code, Tiers_RS.
#     The MOIS{nb_month} column is renamed to 'Montant'.

#     Args:
#         df (pd.DataFrame): Input DataFrame with columns including ANNEE, MOIS01-MOIS12,
#                            Code_Chantier, Type, Tiers_code, Tiers_RS.
#         month (int): Month number (1-12) to filter (e.g., 6 for MOIS06).
#         year (int): Year to filter (e.g., 2025).

#     Returns:
#         pd.DataFrame: Filtered DataFrame with columns Code_Chantier, ANNEE, Montant,
#                       Type, Tiers_code, Tiers_RS.

#     Raises:
#         ValueError: If month is not between 1 and 12.
#         KeyError: If required columns are not in the DataFrame.
#     """
#     # Validate month input
#     if not 1 <= month <= 12:
#         raise ValueError("Month must be between 1 and 12.")

#     # Format month column name (e.g., MOIS06)
#     month_col = f"MOIS{month:02d}"

#     # Define required columns
#     required_columns = ['Code_Chantier','Famille' ,'ANNEE', month_col, 'Type',  'Tiers_RS']

#     # Check if all required columns exist in DataFrame
#     missing_cols = [col for col in required_columns if col not in df.columns]
#     if missing_cols:
#         raise KeyError(f"Missing columns in DataFrame: {', '.join(missing_cols)}")

#     # Filter DataFrame:
#     # - ANNEE matches the specified year
#     # - MOIS{nb_month} is not null
#     filtered_df = df[(df['ANNEE'] == year) & (df[month_col].notnull())].copy()
#     # filtered_df[filtered_df['Famille'] == 'integroupe']
#     # Select only the required columns
#     filtered_df = filtered_df[required_columns]

#     result_ig = filtered_df[filtered_df['Famille'] == 'intergroupe'][month_col].sum()

#     result_hg = filtered_df[filtered_df['Famille'] == 'hors groupe'][month_col].sum()
#     # # Rename the month column to 'Montant'
#     # filtered_df = filtered_df.rename(columns={month_col: 'Montant'})

#     return filtered_df,result_ig,result_hg





# def calculate_enc_reel_type(MAS: pd.DataFrame, type_str: str) -> float:
#     MAS['date_opr'] = pd.to_datetime(MAS['date_opr'], errors='coerce')

#     filtered_df = MAS[(MAS['Type'] == type_str)]

#     calcul = (filtered_df['Credit'] * filtered_df['cours']).sum()
#     return filtered_df.head(1),abs(calcul)

# # Example usage
# if __name__ == "__main__":
#     # Sample DataFrame creation for testing
#     data = {
#         'Code_Chantier': ['CH001', 'CH002', 'CH003'],
#         'Famille':['intergroupe','intergroupe','hors groupe'],
#         'ANNEE': [2025, 2025, 2025],
#         'MOIS01': [1000.0, None, 500.0],
#         'MOIS02': [None, 2000.0, None],
#         'MOIS03': [None, None, None],
#         'MOIS04': [None, None, None],
#         'MOIS05': [158258, 2, 999999],
#         'MOIS06': [1500.0, None, None],
#         'MOIS07': [None, None, None],
#         'MOIS08': [None, None, None],
#         'MOIS09': [299, None, 70000],
#         'MOIS10': [None, None, None],
#         'MOIS11': [None, None, None],
#         'MOIS12': [None, None, None],
#         'Type': ['Type1', 'Type2', 'Type3'],
#         'XDATERECEP': ['2025-01-15', '2025-02-20', '2024-01-10'],
#         'XDATERECEPD': ['2025-01-20', '2025-02-25', '2024-01-15'],
#         'Tiers_code': ['T001', 'T002', 'T003'],
#         'Tiers_Type': ['Client', 'Supplier', 'Client'],
#         'Tiers_RS': ['Company A', 'Company B', 'Company C']
#     }
#     df = get_encaissemnet_prevu()
#     month=current_month
#     year=current_year
#     df_enc_reel= get_client_reel_encaissement()
#     # Extract data for June (MOIS06) 2025
#     try:
#         resuldf,result_ig,result_hg = extract_specific_month_year_data(df, month, year=2025)
#         print(resuldf)
#         print(result_ig)
#         print(result_hg)
#         credit,reel_ig=calculate_enc_reel_type(df_enc_reel,"CLIENT HORS GROUPE")
#         print("#######################")
#         print(credit)
#         print("*-*-*-*-*-*-*--*-*--")
#         print(df_enc_reel)
#         print(f"************\n {reel_ig}")
#     except (ValueError, KeyError) as e:
#         print(f"Error: {e}")

import pyodbc
print(pyodbc.drivers())
