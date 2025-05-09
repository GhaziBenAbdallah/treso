import pandas as pd
import os
import sys
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def french_type_decimal(value: float) -> str:
    return f"{value:.2f}"





# def get_data_objectif_month(df: pd.DataFrame, month: int, year: int) -> pd.DataFrame:
 
#     # Validate month input
#     if not 1 <= month <= 12:
#         raise ValueError("Month must be between 1 and 12.")

#     # Format month column name (e.g., MOIS06)
#     month_col = f"MOIS{month:02d}"

#     # Define required columns
#     required_columns = ['Code_Chantier', 'ANNEE', month_col, 'Type', 'Tiers_code', 'Tiers_RS']

#     # Check if all required columns exist in DataFrame
#     missing_cols = [col for col in required_columns if col not in df.columns]
#     if missing_cols:
#         raise KeyError(f"Missing columns in DataFrame: {', '.join(missing_cols)}")

#     # Filter DataFrame:
#     # - ANNEE matches the specified year
#     # - MOIS{nb_month} is not null
#     filtered_df = df[(df['ANNEE'] == year) & (df[month_col].notnull())].copy()

#     # Select only the required columns
#     filtered_df = filtered_df[required_columns]

#     # # Rename the month column to 'Montant'
#     # filtered_df = filtered_df.rename(columns={month_col: 'Montant'})

#     return filtered_df

# def calculate_decaissement_type(MAS: pd.DataFrame, type_str: str, start_date=None, end_date=None) -> float:
#     MAS['date_opr'] = pd.to_datetime(MAS['date_opr'], errors='coerce')

#     if not start_date or not end_date:
#         current_year = datetime.today().year
#         start_date = datetime(current_year, 1, 1)
#         end_date = datetime(current_year, 12, 31)

#     filtered_df = MAS[
#         (MAS['date_opr'] >= start_date) &
#         (MAS['date_opr'] <= end_date) &
#         (MAS['Type'] == type_str)
#     ]

#     calcul = (filtered_df['Debit'] * filtered_df['cours']).sum()
#     return abs(calcul)


# def calculate_decaissement_type_percentage(MAS: pd.DataFrame, type_str: str, start_date=None, end_date=None) -> float:
#     total = calculate_decaissement_mesures(MAS, start_date, end_date)
#     type_amount = calculate_decaissement_type(MAS, type_str, start_date, end_date)
#     if total == 0:
#         return 0.0
#     return (type_amount / total) * 100


# def get_cumul_year_total(df: pd.DataFrame, start_date=None, end_date=None) -> float:
#     df['date_opr'] = pd.to_datetime(df['date_opr'], errors='coerce')

#     if not start_date or not end_date:
#         current_year = datetime.today().year
#         start_date = datetime(current_year, 1, 1)
#         end_date = datetime(current_year, 12, 31)

#     df_year = df[
#         (df['date_opr'] >= start_date) &
#         (df['date_opr'] <= end_date)
#     ]

#     cumul_encaissement = (df_year['Debit'] * df_year['cours']).sum()
#     return abs(cumul_encaissement)


# def calculate_encaissement_type_cumul(MAS: pd.DataFrame, type_str: str, start_date=None, end_date=None) -> float:
#     MAS['date_opr'] = pd.to_datetime(MAS['date_opr'], errors='coerce')

#     if not start_date or not end_date:
#         current_year = datetime.today().year
#         start_date = datetime(current_year, 1, 1)
#         end_date = datetime(current_year, 12, 31)

#     filtered_df = MAS[
#         (MAS['Type'] == type_str) &
#         (MAS['date_opr'] >= start_date) &
#         (MAS['date_opr'] <= end_date)
#     ]

#     cumul_encaissement = (filtered_df['Debit'] * filtered_df['cours']).sum()
#     return abs(cumul_encaissement)


# # Example usage




# def calculate_cumul_decaissement_year(MAS: pd.DataFrame) -> float:
    
#     # Get current year dates
#     current_year = datetime.today().year
#     start_date = datetime(current_year, 1, 1)
#     end_date = datetime(current_year, 12, 31)
    
#     # Filter for current year
#     MAS['date_opr'] = pd.to_datetime(MAS['date_opr'], errors='coerce')
#     yearly_data = MAS[
#         (MAS['date_opr'] >= start_date) & 
#         (MAS['date_opr'] <= end_date)
#     ]
    
#     # Calculate sum of (Credit * cours)
#     cumul = (yearly_data['Debit'] * yearly_data['cours']).sum()
    
#     return abs(cumul)


# def calculate_cumul_decaissement_year_type(MAS: pd.DataFrame, type_str: str = None) -> float:
#     """
#     Calculate yearly cumulative encaissement, optionally filtered by type
    
#     Args:
#         MAS: DataFrame containing financial data
#         type_str: Optional type filter (e.g., 'EXPLOITATION')
    
#     Returns:
#         float: Absolute sum of (Credit * cours) for the current year
#     """
#     current_year = datetime.today().year
#     start_date = datetime(current_year, 1, 1)
#     end_date = datetime(current_year, 12, 31)
    
#     MAS['date_opr'] = pd.to_datetime(MAS['date_opr'], errors='coerce')
    
#     # Base filter for date range
#     mask = (
#         (MAS['date_opr'] >= start_date) & 
#         (MAS['date_opr'] <= end_date)
#     )
    
#     # Add type filter if specified
#     if type_str:
#         mask &= (MAS['Type'] == type_str)
    
#     filtered_df = MAS[mask]
#     cumul = (filtered_df['Debit'] * filtered_df['cours']).sum()
    
#     return abs(cumul)

# Function to extract specific columns for a given month and year
def extract_prevu_enc_month_year_data(df: pd.DataFrame, month: int, year: int) -> pd.DataFrame:
    df.to_csv("data/mas/enc_prevu_ig_hg.csv")
    # Validate month input
    if not 1 <= month <= 12:
        raise ValueError("Month must be between 1 and 12.")
  
    # Format month column name (e.g., MOIS06)
    month_col = f"MOIS{month:02d}"
    
    # Define required columns
    required_columns = ['Code_Chantier','Famille' ,'ANNEE', month_col, 'Type']

    # Check if all required columns exist in DataFrame
   

    # Filter DataFrame:
    # - ANNEE matches the specified year
    # - MOIS{nb_month} is not null
    filtered_df = df[(df['ANNEE'] == year) & (df[month_col].notnull())].copy()
    # filtered_df[filtered_df['Famille'] == 'integroupe']
    # Select only the required columns
    filtered_df = filtered_df[required_columns]

    result_ig = filtered_df[filtered_df['Famille'] == 'intergroupe'][month_col].sum()

    result_hg = filtered_df[filtered_df['Famille'] == 'hors groupe'][month_col].sum()
    # # Rename the month column to 'Montant'
    # filtered_df = filtered_df.rename(columns={month_col: 'Montant'})
    
    return result_ig,result_hg




def calculate_enc_reel_type(MAS: pd.DataFrame, type_str: str) -> float:
    MAS['date_opr'] = pd.to_datetime(MAS['date_opr'], errors='coerce')
    MAS.to_csv("data/mas/enc_reel_ig_hg.csv")
    filtered_df = MAS[(MAS['Type'] == type_str)]
    
    

    calcul = (filtered_df['Credit'] * filtered_df['cours']).sum()
    
    return abs(calcul)

# def calculate_enc_reel_type(MAS: pd.DataFrame, type_str: str, month: int, year: int) -> float:
#     MAS['date_opr'] = pd.to_datetime(MAS['date_opr'], errors='coerce')

   
    
    

#     filtered_df = MAS[
#         (MAS['date_opr'].dt.month == year) &
#         (MAS['date_opr'].dt.month == month) &
#         (MAS['Type'] == type_str)
#     ]

#     calcul = (filtered_df['Credit'] * filtered_df['cours']).sum()
#     return abs(calcul)