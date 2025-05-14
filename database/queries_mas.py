import sys
import os
import pandas as pd
from pandas.tseries.offsets import MonthEnd
from contextlib import contextmanager
from datetime import datetime
import streamlit as st 


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.db_connection import get_db_connection
db_name="MAS"



@contextmanager
def db_cursor(db_name):
    """Context manager for database connection handling"""
    conn = None
    try:
        conn = get_db_connection(db_name)
        cursor = conn.cursor()
        yield cursor
    except Exception as e:
        print(f"Database error: {e}")
        raise
    finally:
        if conn:
            conn.close()







def execute_query_to_dataframe(query, db_name="MAS"):
    """Execute a SQL query and return results as a DataFrame"""
    with db_cursor(db_name) as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return pd.DataFrame([tuple(row) for row in rows], columns=columns)
    






def get_encaissemnet_prevu():
    query = """
    
SELECT 
    Code_Chantier,
    CASE 
        WHEN tiers.Tiers_Famille = 'intergroupe' THEN 'intergroupe'
        ELSE 'hors groupe'
    END as 'Famille',
    ANNEE,    MOIS01,    MOIS02,    MOIS03,    MOIS04,    MOIS05,    MOIS06,
    MOIS07,    MOIS08,    MOIS09,    MOIS10,    MOIS11,    MOIS12,    Type,
    XDATERECEP,    XDATERECEPD,    Tiers_code as Tiers_Type,    Tiers_RS 
FROM 
    XOBJFACT 
    INNER JOIN TIERS ON XOBJFACT.Code_Chantier = tiers.Tiers_code  
WHERE 
    ANNEE = YEAR(GETDATE())


    """
    return execute_query_to_dataframe(query)

def get_client_reel_encaissement():
    query = """
    

	SELECT 
        ISNULL(dbo.GetCours(
            CASE 
                WHEN reg_banque LIKE '%$%' THEN 'usd' 
                WHEN reg_banque LIKE '%€%' THEN 'eur'
            END, 
            ISNULL(reg_dateencaisse, Reg_DateEcheance), 
            'bct'
        ), 1) AS cours,
        idllig,
        Reg_DateEcheance AS 'date_opr',
        ISNULL(reg_dateencaisse, Reg_DateEcheance) AS 'date_valeur',
        ISNULL(Libelle, 'Encaissement Client') AS 'Libelle',
        ISNULL(num_piece, reg_ref) AS 'Num_piece',
        ISNULL(debit, 0) AS 'Debit',
        ISNULL(credit, reg_montant) AS 'Credit',
        ISNULL(banque, reg_banque) AS 'Banque',
        reg_num AS 'Piece',
        reglement.Tiers_RS,
        rp.RegParam_Libelle AS 'Nature',
        CASE 
            WHEN LOWER(tiers.tiers_famille) LIKE '%intergroupe%' THEN 'CLIENT INTERGROUPE'
            ELSE 'CLIENT HORS GROUPE'
        END AS Type
    FROM
        Reglement
        INNER JOIN regparam rp ON rp.RegParam_Code = reglement.RegParam_Code
        INNER JOIN Tiers ON tiers.tiers_code = reglement.tiers_code
        LEFT OUTER JOIN xrelevehistorique ON piece = reg_num
            AND credit BETWEEN reg_montant_devise - 100 AND reg_montant_devise + 100
    WHERE
        reg_tierstype = '01'
		
        AND month(Reg_DateEcheance) = month(getdate()) and year(Reg_DateEcheance) = year(getdate()) 
        AND reg_type <> 'Retenue'
        AND Reg_Status = 20
    ORDER BY
        reg_num ASC;


    """
    return execute_query_to_dataframe(query)



def get_enc_dec():
    query = """
    SELECT
        ISNULL(dbo.GetCours(
            CASE
                WHEN banque LIKE '%$%' THEN 'usd'
                WHEN banque LIKE '%€%' THEN 'eur'
            END,
            date_opr,
            'bct'
        ), 1) AS cours,
        *
    FROM
        nature_xr
    WHERE 
        month(date_opr)= month(getdate())
        AND year(date_opr)= year(getdate())
        AND type IN ('CLIENT INTERGROUPE', 'CLIENT HORS GROUPE')

    """
    return execute_query_to_dataframe(query)



def get_solde_clients():
    query = """
    EXEC dbo.SOLDECLIENT
    """
    return execute_query_to_dataframe(query)


def get_decaissement_frs():
    query = """
          SELECT 
    ISNULL(dbo.GetCours(
        CASE 
            WHEN reg_banque LIKE '%$%' THEN 'usd' 
            WHEN reg_banque LIKE '%€%' THEN 'eur'
        END, 
        ISNULL(reg_dateencaisse, Reg_DateEcheance), 
        'bct'
    ), 1) AS cours,
    
    Reg_DateEcheance AS 'date_opr',
    ISNULL(reg_dateencaisse, Reg_DateEcheance) AS 'date_valeur',
    

	Reg_Status,
   
   
    reg.Reg_Montant,reg.Reg_Devise_Cours,
    reg_num AS 'Piece',
    reg.Tiers_RS,
    rp.RegParam_Libelle AS 'Nature',
    CASE 
        WHEN LOWER(tiers.tiers_famille) LIKE '%intergroupe%' or LOWER(tiers.tiers_famille) like'%local%' THEN 'FOURNISSEUR INTERGROUPE'
		ELSE 'FOURNISSEUR HORS GROUPE'
        
    END AS Type
FROM
    Reglement reg
    INNER JOIN diversys div ON reg.reg_status = div.diversys_index AND   div.DiverSys_Type = '0901' 
    INNER JOIN regparam rp ON rp.RegParam_Code = reg.RegParam_Code and reg.Reg_TiersType='02' 
    INNER JOIN Tiers ON tiers.tiers_code = reg.tiers_code
    LEFT OUTER JOIN xrelevehistorique ON piece = reg_num
        AND credit BETWEEN reg_montant_devise - 100 AND reg_montant_devise + 100
WHERE
    
       month(Reg_DateEcheance) =month(getdate())
 AND year(Reg_DateEcheance) =YEAR(getdate()) 
	  AND
     Reg_Status IN (3, 4, 17) 


	
    """
    return execute_query_to_dataframe(query)


def get_cnss_mas():
    query = """
     SELECT 
        GRHRubVE_mois AS Mois,
        GRHRubVE_ex AS Annee,
        SUM( ((GRHRubV_Montant / 0.0968) * 8.535 / 100) + GRHRubV_Montant ) AS montant
    FROM 
        VSalaire
    WHERE 
        GRHRubVE_ex >= 2025
        AND GRHRub_Code = 'CNSSSA'
    GROUP BY 
        GRHRubVE_mois, GRHRubVE_ex
    ORDER BY 
        GRHRubVE_mois;
    """
    return execute_query_to_dataframe(query)

def get_salaire_mas():
    query = """
    SELECT
        GRHRubVE_mois AS Mois,
        GRHRubVE_ex AS Annee,
        SUM(GRHRubV_Montant) AS montant
    FROM 
        VSalaire  
    WHERE  
        GRHRubVE_ex >= 2025
        AND GRHRub_Code='SANET2'
    GROUP BY 
        GRHRubVE_mois, GRHRubVE_ex
    ORDER BY
        GRHRubVE_mois;
    """
    return execute_query_to_dataframe(query)




def get_steg():
    query="""


        select doc_num,doc_date,Doc_RS,Doc_valide,doc_devise_cours,doc_tht,Doc_TTTC,Doc_THT*Doc_Devise_Cours as 'Montant' 
        from document
        where doc_type ='facsteg'
        and year(doc_date)= year(getdate())
        and month(doc_date)= month(getdate()) 
        and day(getdate())>=day(doc_date)

        """
    return execute_query_to_dataframe(query)


def get_sonede():
    query="""


        
    select  doc_num,doc_date,Doc_RS,Doc_valide,doc_devise_cours,doc_tht,Doc_TTTC,Doc_THT*Doc_Devise_Cours as 'Montant' 
    from document 
    where doc_type ='fafo' and Tiers_code='FS013' 
    and year(doc_date)= year(getdate())
    and month(doc_date)= month(getdate()) 
    and day(getdate())>=day(doc_date)

        """
    return execute_query_to_dataframe(query)



# def get_cnss_mas():
#     query = """
#     SELECT 
#         GRHRubVE_mois AS Mois,
#         GRHRubVE_ex AS Annee,
#         SUM( ((GRHRubV_Montant / 0.0968) * 8.535 / 100) + GRHRubV_Montant ) AS Cnss_P_S
#     FROM 
#         VSalaire
#     WHERE 
#         GRHRubVE_ex >= 2025
#         AND GRHRub_Code = 'CNSSSA'
#     GROUP BY 
#         GRHRubVE_mois, GRHRubVE_ex
#     ORDER BY 
#         GRHRubVE_mois;
#     """
#     return execute_query_to_dataframe(query)

# def get_salaire_mas():
#     query = """
#     SELECT
#         GRHRubVE_mois AS Mois,
#         GRHRubVE_ex AS Annee,
#         SUM(GRHRubV_Montant) AS salaire
#     FROM 
#         VSalaire  
#     WHERE  
#         GRHRubVE_ex >= 2025
#         AND GRHRub_Code='SANET2'
#     GROUP BY 
#         GRHRubVE_mois, GRHRubVE_ex
#     ORDER BY
#         GRHRubVE_mois;
#     """
#     return execute_query_to_dataframe(query)
# def combine_financial_data(df_encaissement_client,enc_dec_df, cnss_df, salaire_df):
#     # Make copies to avoid modifying original dataframes
#     enc_dec = enc_dec_df.copy()
#     cnss = cnss_df.copy()
#     salaire = salaire_df.copy()
#     encaissement_client = df_encaissement_client.copy()
    
#     # Rename columns to consistent names
#     cnss = cnss.rename(columns={'GRHRubVE_ex': 'Annee', 'GRHRubVE_mois': 'Mois'})
#     salaire = salaire.rename(columns={'GRHRubVE_ex': 'Annee', 'GRHRubVE_mois': 'Mois'})
    
#     # Remove the duplicate renaming of date columns for encaissement_client
#     # They're already properly named from get_client_encaissement()

#     # Filter data to only include 2025 and later
#     min_date = datetime(2025, 1, 1)
    
#     # Process encaissement/decaissement data
#     enc_dec['date_opr'] = pd.to_datetime(enc_dec['date_opr'])
#     enc_dec['date_valeur'] = pd.to_datetime(enc_dec['date_valeur'])
#     enc_dec = enc_dec[enc_dec['date_opr'] >= min_date]
    
#     # Process client encaissement data - no renaming needed
#     encaissement_client['date_opr'] = pd.to_datetime(encaissement_client['date_opr'])
#     encaissement_client['date_valeur'] = pd.to_datetime(encaissement_client['date_valeur'])
#     encaissement_client = encaissement_client[encaissement_client['date_opr'] >= min_date]

#     # Rest of your function remains the same...
#     def standardize_type(df):
#         # First ensure Type is string type and clean it
        
#         df['Type'] = df['Type'].astype(str).str.strip().str.upper()
#         # Fill remaining NAs or empty strings
#         df['Type'] = df['Type'].replace(['', 'NAN', 'NONE'], 'NON DEFINIS')
#         df['Type'] = df['Type'].fillna('NON DEFINIS')
        
        
#         supplier_mask = (
#             df['Nature'].str.strip().str.startswith('Réglement Fournisseur', na=False) | 
#             df['Nature'].str.strip().str.startswith('Reglement Fournisseur', na=False)
#         ) & (
#             df['Type'].isna() | 
#             (df['Type'].str.strip() == '') |
#             (df['Type'].str.strip().str.upper() == 'NAN') |
#             (df['Type'].str.strip().str.upper() == 'NONE')
#         )
        
#         # Apply standardization
#         df.loc[supplier_mask, 'Type'] = 'EXPLOITATION'
#         df.loc[df['Type'].str.strip().str.upper() == 'EXPLOITATION', 'Type'] = 'EXPLOITATION'
        
#         #
#         return df

#     enc_dec = standardize_type(enc_dec)
#     encaissement_client = standardize_type(encaissement_client)

#     # Function to create additional rows
#     def create_additional_rows(source_df, amount_col, label, type_name, tiers):
#         rows = []
#         for _, row in source_df.iterrows():
#             eom_date = pd.to_datetime(f"{int(row['Annee'])}-{int(row['Mois'])}-01") + MonthEnd(1)
#             if eom_date >= min_date:
#                 rows.append({
#                     'cours': 1.00000000,
#                     'idllig': None,
#                     'date_opr': eom_date,
#                     'date_valeur': eom_date,
#                     'Libelle': label,
#                     'Num_piece': None,
#                     'Debit': row[amount_col],
#                     'Credit': 0.0,
#                     'Banque': None,
#                     'Piece': None,
#                     'Tiers_RS': tiers,
#                     'Nature': None,
#                     'Type': type_name,
#                     'date_combo': eom_date.date()  # Store as date only
#                 })
#         return pd.DataFrame(rows)

#     # Create additional rows
#     cnss_rows = create_additional_rows(cnss, 'Cnss_P_S', 'Paiement CNSS', 'CNSS', 'CNSS')
#     salaire_rows = create_additional_rows(salaire, 'salaire', 'Paiement Salaires', 'SALAIRE', 'SALARIES')

#     # Add date_combo to original data (as date only)
#     enc_dec['date_combo'] = enc_dec['date_opr'].dt.date
#     encaissement_client['date_combo'] = encaissement_client['date_opr'].dt.date

#     # Combine all data
#     combined_df = pd.concat(
#         [encaissement_client, enc_dec, cnss_rows, salaire_rows],
#         ignore_index=True
#     )

#     # Sort by operation date and filter to >= 2025
#     combined_df = combined_df[combined_df['date_opr'] >= min_date]
#     combined_df = combined_df.sort_values('date_opr').reset_index(drop=True)
    
#     # Ensure date_combo is the last column
#     cols = [col for col in combined_df.columns if col != 'date_combo'] + ['date_combo']
#     combined_df = combined_df[cols]

#     return combined_df





# def combine_decaissement_data(enc_dec_df, cnss_df, salaire_df):
#     # Make copies to avoid modifying original dataframes
#     enc_dec = enc_dec_df.copy()
#     cnss = cnss_df.copy()
#     salaire = salaire_df.copy()
    
    
#     # Rename columns to consistent names
#     cnss = cnss.rename(columns={'GRHRubVE_ex': 'Annee', 'GRHRubVE_mois': 'Mois'})
#     salaire = salaire.rename(columns={'GRHRubVE_ex': 'Annee', 'GRHRubVE_mois': 'Mois'})
    
#     # Remove the duplicate renaming of date columns for encaissement_client
#     # They're already properly named from get_client_encaissement()

#     # Filter data to only include 2025 and later
#     min_date = datetime(2025, 1, 1)
    
#     # Process encaissement/decaissement data
#     enc_dec['date_opr'] = pd.to_datetime(enc_dec['date_opr'])
#     enc_dec['date_valeur'] = pd.to_datetime(enc_dec['date_valeur'])
#     enc_dec = enc_dec[enc_dec['date_opr'] >= min_date]
    
#     # Process client encaissement data - no renaming needed
    

#     # Rest of your function remains the same...
#     def standardize_type(df):
#         # First ensure Type is string type and clean it
        
#         df['Type'] = df['Type'].astype(str).str.strip().str.upper()
#         # Fill remaining NAs or empty strings
#         df['Type'] = df['Type'].replace(['', 'NAN', 'NONE'], 'NON DEFINIS')
#         df['Type'] = df['Type'].fillna('NON DEFINIS')
        
        
#         supplier_mask = (
#             df['Nature'].str.strip().str.startswith('Réglement Fournisseur', na=False) | 
#             df['Nature'].str.strip().str.startswith('Reglement Fournisseur', na=False)
#         ) & (
#             df['Type'].isna() | 
#             (df['Type'].str.strip() == '') |
#             (df['Type'].str.strip().str.upper() == 'NAN') |
#             (df['Type'].str.strip().str.upper() == 'NONE')
#         )
        
#         # Apply standardization
#         df.loc[supplier_mask, 'Type'] = 'EXPLOITATION'
#         df.loc[df['Type'].str.strip().str.upper() == 'EXPLOITATION', 'Type'] = 'EXPLOITATION'
        
#         #
#         return df

#     enc_dec = standardize_type(enc_dec)


#     # Function to create additional rows
#     def create_additional_rows(source_df, amount_col, label, type_name, tiers):
#         rows = []
#         for _, row in source_df.iterrows():
#             eom_date = pd.to_datetime(f"{int(row['Annee'])}-{int(row['Mois'])}-01") + MonthEnd(1)
#             if eom_date >= min_date:
#                 rows.append({
#                     'cours': 1.00000000,
#                     'idllig': None,
#                     'date_opr': eom_date,
#                     'date_valeur': eom_date,
#                     'Libelle': label,
#                     'Num_piece': None,
#                     'Debit': row[amount_col],
#                     'Credit': 0.0,
#                     'Banque': None,
#                     'Piece': None,
#                     'Tiers_RS': tiers,
#                     'Nature': None,
#                     'Type': type_name,
#                     'date_combo': eom_date.date()  # Store as date only
#                 })
#         return pd.DataFrame(rows)

#     # Create additional rows
#     cnss_rows = create_additional_rows(cnss, 'Cnss_P_S', 'Paiement CNSS', 'CNSS', 'CNSS')
#     salaire_rows = create_additional_rows(salaire, 'salaire', 'Paiement Salaires', 'SALAIRE', 'SALARIES')

#     # Add date_combo to original data (as date only)
#     enc_dec['date_combo'] = enc_dec['date_opr'].dt.date
   

#     # Combine all data
#     combined_df = pd.concat(
#         [enc_dec, cnss_rows, salaire_rows],
#         ignore_index=True
#     )

#     # Sort by operation date and filter to >= 2025
#     combined_df = combined_df[combined_df['date_opr'] >= min_date]
#     combined_df = combined_df.sort_values('date_opr').reset_index(drop=True)
    
#     # Ensure date_combo is the last column
#     cols = [col for col in combined_df.columns if col != 'date_combo'] + ['date_combo']
#     combined_df = combined_df[cols]

#     return combined_df


# import logging


# # Configure logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     datefmt='%Y-%m-%d %H:%M:%S'
# )
# logger = logging.getLogger(__name__)

# # Assume these functions are defined elsewhere in queries.py

# def refresh_data():
#     """
#     Refreshes financial data by fetching, combining, and saving encaissement and decaissement data.
#     Clears Streamlit cache to ensure updated data is loaded in the app.
#     """
#     try:
#         # Fetch raw data
#         logger.info("Fetching financial data...")
#         enc_dec_df = get_enc_dec()
#         cnss_mas_df = get_cnss_mas()
#         salaire_mas_df = get_salaire_mas()
#         client_encaissement_df = get_client_encaissement()

#         # Combine encaissement data
#         logger.info("Combining encaissement data...")
#         combined_data = combine_financial_data(
#             enc_dec_df=enc_dec_df,
#             cnss_df=cnss_mas_df,
#             salaire_df=salaire_mas_df,
#             df_encaissement_client=client_encaissement_df
#         )

#         # Save encaissement data
#         encaissement_file = 'data/mas/combined_encaissement_data_mas.xlsx'
#         combined_data.to_excel(encaissement_file, index=False)
#         logger.info(f"Mas Encaissement data saved to {encaissement_file}")

#         # Combine decaissement data
#         logger.info("Combining decaissement data...")
#         decaissement_df = get_enc_dec()
#         combined_decaissement_data = combine_decaissement_data(
#             enc_dec_df=decaissement_df,
#             cnss_df=cnss_mas_df,
#             salaire_df=salaire_mas_df
#         )

#         # Save decaissement data
#         decaissement_file = 'data/mas/combined_decaissement_data_mas.xlsx'
#         combined_decaissement_data.to_excel(decaissement_file, index=False)
#         logger.info(f"Mas Decaissement data saved to {decaissement_file}")

#         # Log date ranges and sample data
#         for data, name in [(combined_data, "Encaissement"), (combined_decaissement_data, "Decaissement")]:
#             date_opr = pd.to_datetime(data['date_opr'])
#             min_date = date_opr.min().strftime('%d/%m/%Y')
#             max_date = date_opr.max().strftime('%d/%m/%Y')
#             logger.info(f"{name} date range: {min_date} to {max_date}")
#             logger.info(f"{name} first 5 rows:\n{data.head().to_string()}")

#         # Clear Streamlit cache to ensure app reloads fresh data
#         st.cache_data.clear()
#         logger.info("Streamlit cache cleared")

#     except Exception as e:
#         logger.error(f"Error refreshing financial data: {str(e)}")
#         raise


