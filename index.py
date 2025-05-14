
# import streamlit as st
# import pandas as pd
# import datetime
# from database.queries_mas import get_encaissemnet_prevu ,get_client_reel_encaissement
# from mesures.mesures_mas import extract_prevu_enc_month_year_data,calculate_enc_reel_type



# # Utility function to format float values with two decimal places
# def french_type_decimal(value: float) -> str:
#     return f"{value:.2f}"

# # Utility function to format numbers with French-style thousands separator
# def format_montant_fr(n):
#     try:
#         if isinstance(n, float) and n.is_integer():
#             n = int(n)
#         elif isinstance(n, float):
#             n = round(n)
#         return f"{n:,}".replace(",", " ")
#     except (TypeError, ValueError):
#         return str(n)

# # Main function for the treasury dashboard
# def tresorrerie_mas():
#     # --------------------------- Page Configuration -----------------------------
#     # Set Streamlit page layout to wide for better use of screen space
#     st.set_page_config(layout="wide")

#     # --------------------------- Header Section --------------------------------
#     # Create a header with logo and title
#     with st.container():
#         with st.container(border=False):
#             col1, col2 = st.columns([0.8, 10])
#             with col1:
#                 with st.container(border=False):
#                     # Display company logo
#                     st.image("img/mas.png")
#             with col2:
#                 with st.container(border=True):
#                     # Display page title
#                     st.title("Trésorrerie - 2025")

#     # --------------------------- Date Filter Section ---------------------------
#     # Setup date filters for year and month selection
#     current_year = datetime.datetime.now().year
#     current_month = datetime.datetime.now().month

#     with st.container():
#         col_year, col_month, col_refresh = st.columns(3)
#         with col_year:
#             # Year selection dropdown
#             year_options = list(range(2025, current_year + 1))
#             selected_year = st.selectbox("Année", year_options, index=len(year_options)-1, key="year_select")
        
#         with col_month:
#             # Month selection dropdown, limited to completed months for current year
#             month_names = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", 
#                            "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
#             if selected_year == current_year:
#                 month_options = list(range(1, current_month))
#             else:
#                 month_options = list(range(1, 13))
#             month_display_options = ["Tous les mois"] + [month_names[i-1] for i in month_options]
#             selected_month = st.selectbox("Mois", month_display_options, index=0, key="month_select")
        
#         with col_refresh:
#             # Button to refresh data and clear cache
#             if st.button("Actualiser les données"):
#                 st.cache_data.clear()
#                 st.rerun()

#     # --------------------------- Data Loading Function -------------------------
#     # Cached function to load and preprocess Excel data
#     @st.cache_data
#     def load_data(path):
#         df = pd.read_excel(path)
#         df['date_combo'] = pd.to_datetime(df['date_combo'])
#         return df

#     # --------------------------- Encaissement Section --------------------------
#     # Display encaissement data with global and detailed views
#     with st.expander("Encaissement"):
#         df_prevu_enc=get_encaissemnet_prevu()
#         df_reel_enc=get_client_reel_encaissement()
#         prevu_ig,prevu_hg=extract_prevu_enc_month_year_data(df_prevu_enc,current_month,current_year)
#         reel_enc_ig= calculate_enc_reel_type(df_reel_enc,"CLIENT INTERGROUPE")

#         reel_enc_hg =calculate_enc_reel_type(df_reel_enc,"CLIENT HORS GROUPE")





#         tab_encaissement1, tab_encaissement2 = st.tabs(["Vue Globale", "Détails"])
#         with tab_encaissement1:
#             with st.container(border=True):
#                 col1, col2 = st.columns(2)
#                 with col1:
#                     with st.container(border=False):
#                         # Header for encaissement table with styled Prévu and Réalisé
#                         st.markdown(
#                             """
#                             <div style="display: flex; border-radius: 10px; overflow: hidden; font-weight: bold;">
#                                 <div style="flex: 2; background-color: rgb(52 131 73 / 70%); text-align: center; color: white; padding: 10px;">ENCAISSEMENT</div>
#                                 <div style="flex: 1; background-color: #e0f2f1; text-align: center; color: black; padding: 10px; border-radius: 10px; margin: 0 5px;">Prévu</div>
#                                 <div style="flex: 1; background-color: #e0f2f1; text-align: center; color: black; padding: 10px; border-radius: 10px;">Réalisé</div>
#                             </div>
#                             """,
#                             unsafe_allow_html=True
#                         )
#                         col_prev_enc1,col_prev_enc2, col_reel= st.columns (3)
#                         with col_prev_enc1:
#                             with st.container(border=False):
#                                 st.write("   \n")
#                                 st.markdown(f"**Intergroupe**")
#                                 st.write("   \n")
#                                 st.markdown(f"**Hors groupe**")
#                         with col_prev_enc2:
#                             st.write("   \n")
#                             st.markdown(f"**{format_montant_fr(prevu_ig)}**")
#                             st.write("   \n")
#                             st.markdown(f"**{format_montant_fr(prevu_hg)}**")
#                         with col_reel :
#                             st.write("   \n")
#                             st.markdown(f"**{format_montant_fr(reel_enc_ig)}**")
#                             st.write("   \n")
#                             st.markdown(f"**{format_montant_fr(reel_enc_hg)}**")


                
#                 with col2:
#                     with st.container(border=False):
#                         col1_prev_entete, col2_prev_entete = st.columns(2)    
#                         with col1_prev_entete:
#                             # Remarque 1 header
#                             st.markdown(
#                                 """
#                                 <div style="display: flex; border-radius: 10px; overflow: hidden; font-weight: bold;">
#                                     <div style="flex: 1; background-color: #e0f2f1; text-align: center; color: black; padding: 10px; border-radius: 10px;">Remarque 1</div>
#                                 </div>
#                                 """,
#                                 unsafe_allow_html=True
#                             )



                        
#                         with col2_prev_entete:
#                             # Remarque 2 header
#                             st.markdown(
#                                 """
#                                 <div style="display: flex; border-radius: 10px; overflow: hidden; font-weight: bold;">
#                                     <div style="flex: 1; background-color: #e0f2f1; text-align: center; color: black; padding: 10px; border-radius: 10px;">Remarque 2</div>
#                                 </div>
#                                 """,
#                                 unsafe_allow_html=True
#                             )
        
#         with tab_encaissement2:
#             with st.container(border=True):
#                 # Detailed view for encaissement
#                 st.subheader("Détails des Encaissements")

#     # --------------------------- Décaissement Sections -------------------------
#     # Display décaissement data for various categories
#     def display_decaissement_section(title, labels):
#         with st.expander(title):
#             with st.container(border=True):
#                 tab_decaissement1, tab_decaissement2 = st.tabs(["Vue Globale", "Détails"])
                
#                 with tab_decaissement1:
#                     col1_dec, col2_dec = st.columns(2)
#                     with col1_dec:
#                         with st.container(border=False):
#                             # Header for décaissement table with styled Prévu and Réalisé
#                             st.markdown(
#                                 """
#                                 <div style="display: flex; border-radius: 10px; overflow: hidden; font-weight: bold;">
#                                     <div style="flex: 2; background-color: rgb(52 131 73 / 70%); text-align: center; color: white; padding: 10px;">LIBELLE</div>
#                                     <div style="flex: 1; background-color: #e0f2f1; text-align: center; color: black; padding: 10px; border-radius: 10px; margin: 0 5px;">Prévu</div>
#                                     <div style="flex: 1; background-color: #e0f2f1; text-align: center; color: black; padding: 10px; border-radius: 10px;">Réalisé</div>
#                                 </div>
#                                 """,
#                                 unsafe_allow_html=True
#                             )
#                             with st.container(border=False):
#                                 st.write("   \n")
#                                 for label in labels:
#                                     st.markdown(f"**{label}**")
                        
#                     with col2_dec:
#                         with st.container(border=False):
#                             col1_prev_entete, col2_prev_entete = st.columns(2)    
#                             with col1_prev_entete:
#                                 # Remarque 1 header
#                                 st.markdown(
#                                     """
#                                     <div style="display: flex; border-radius: 10px; overflow: hidden; font-weight: bold;">
#                                         <div style="flex: 1; background-color: #e0f2f1; text-align: center; color: black; padding: 10px; border-radius: 10px;">Remarque 1</div>
#                                     </div>
#                                     """,
#                                     unsafe_allow_html=True
#                                 )
                                
#                             with col2_prev_entete:
#                                 # Remarque 2 header
#                                 st.markdown(
#                                     """
#                                     <div style="display: flex; border-radius: 10px; overflow: hidden; font-weight: bold;">
#                                         <div style="flex: 1; background-color: #e0f2f1; text-align: center; color: black; padding: 10px; border-radius: 10px;">Remarque 2</div>
#                                     </div>
#                                     """,
#                                     unsafe_allow_html=True
#                                 )
                
#                 with tab_decaissement2:
#                     with st.container(border=True):
#                         # Detailed view for décaissement
#                         st.subheader("Détails des Décaissements")

#     # Define and display each décaissement section
#     display_decaissement_section(
#         "Décaissement Fournisseur Intergroupe",
#         ["Fournisseur Intergroupe à prévoir", "Fournisseur Intergroupe Engagé"]
#     )
#     display_decaissement_section(
#         "Décaissement Fournisseur Horsgroupe",
#         ["Fournisseur Horsgroupe à prévoir", "Fournisseur Horsgroupe Engagé"]
#     )
#     display_decaissement_section(
#         "Décaissement Charge Fix",
#         ["STEG", "SONEDE", "LOCATION"]
#     )
#     display_decaissement_section(
#         "Salaire",
#         ["SALAIRE NET", "CNSS ECHEANCE", "CNSS A PREVOIR"]
#     )
#     display_decaissement_section(
#         "Etat et taxe",
#         ["NON DEFINIS"]
#     )
#     display_decaissement_section(
#         "Autre charge Décaissé",
#         ["NON DEFINIS"]
#     )

#     # --------------------------- Summary Section -------------------------------
#     # Display summary with augmentation totals
#     with st.container(border=True):
#         col_label, col_sum = st.columns(2)
#         with col_label:
#             st.write("\n")
#             for _ in range(4):
#                 st.markdown("**AUGMENTATION**")
#         with col_sum:
#             st.write("\n")
#             st.markdown("*TOTAL*")

# # Entry point for the script
# if __name__ == "__main__":
#     tresorrerie_mas()
import streamlit as st
import pandas as pd
import datetime
from database.queries_mas import get_encaissemnet_prevu, get_client_reel_encaissement,get_solde_clients,get_decaissement_frs,get_cnss_mas,get_salaire_mas,get_steg,get_sonede
from mesures.mesures_mas import extract_prevu_enc_month_year_data, calculate_enc_reel_type,calculate_solde_client,calculate_decaissement_type,calculate_cnss_salaire_type,calculate_steg,calculate_sonede

# Utility functions remain the same
def french_type_decimal(value: float) -> str:
    return f"{value:.2f}"

def format_montant_fr(n):
    try:
        if isinstance(n, float) and n.is_integer():
            n = int(n)
        elif isinstance(n, float):
            n = round(n)
        return f"{n:,}".replace(",", " ")
    except (TypeError, ValueError):
        return str(n)

# Main function for the treasury dashboard
def tresorrerie_mas():
    # --------------------------- Page Configuration -----------------------------
    st.set_page_config(layout="wide")
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month
    

    # French month names
    french_months = [
        "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
        "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"
    ]

    # Get current month name in French
    current_month_str = french_months[current_month - 1]

    
    # --------------------------- Header Section --------------------------------
    with st.container():
        with st.container(border=False):
            col1, col2 = st.columns([0.8, 10])
            with col1:
                with st.container(border=False):
                    st.image("img/mas.png")
            with col2:
                
                with st.container(border=True):
                    st.title(f"Trésorrerie - {current_month_str} - {current_year}")

    # --------------------------- Date Filter Section ---------------------------
    

    with st.container():
        col_year, col_month, col_refresh = st.columns(3)
        with col_year:
            year_options = list(range(2025, current_year + 1))
            selected_year = st.selectbox("Année", year_options, index=len(year_options)-1, key="year_select")
        
        with col_month:
            month_names = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", 
                         "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
            if selected_year == current_year:
                month_options = list(range(1, current_month))
            else:
                month_options = list(range(1, 13))
            month_display_options = ["Tous les mois"] + [month_names[i-1] for i in month_options]
            selected_month = st.selectbox("Mois", month_display_options, index=0, key="month_select")
        
        # with col_refresh:
        #     if st.button("Actualiser les données"):
        #         st.cache_data.clear()
        #         st.rerun()

    # --------------------------- Unified Header -------------------------------
    with st.container():
        st.markdown(
            """
            <div style="display: flex; border-radius: 10px; overflow: hidden; font-weight: bold; margin-bottom: 10px;">
                <div style="flex: 2; background-color: rgb(52 131 73 / 70%); text-align: center; color: white; padding: 10px;">LIBELLE</div>
                <div style="flex: 1; background-color: #e0f2f1; text-align: center; color: black; padding: 10px;">Prévu</div>
                <div style="flex: 1; background-color: #e0f2f1; text-align: center; color: black; padding: 10px;">Réalisé</div>
                <div style="flex: 1; background-color: #e0f2f1; text-align: center; color: black; padding: 10px;">Remarque 1</div>
                <div style="flex: 1; background-color: #e0f2f1; text-align: center; color: black; padding: 10px;">Remarque 2</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # --------------------------- Data Loading -------------------------
    @st.cache_data
    def load_data(path):
        df = pd.read_excel(path)
        df['date_combo'] = pd.to_datetime(df['date_combo'])
        return df

    # --------------------------- Encaissement Section --------------------------
    def display_encaissement():
        df_prevu_enc = get_encaissemnet_prevu()
        # df_prevu_enc=pd.read_csv("data/mas/enc_prevu_ig_hg.csv")
        # df_reel_enc = get_client_reel_encaissement()
        df_reel_enc = pd.read_csv("data/mas/enc_reel_ig_hg.csv")
        df_solde_clt=pd.read_csv("data/mas/solde_client.csv")
        prevu_ig, prevu_hg = extract_prevu_enc_month_year_data(df_prevu_enc, current_month, current_year)
        
        reel_enc_ig = calculate_enc_reel_type(df_reel_enc, "CLIENT INTERGROUPE")
        reel_enc_hg = calculate_enc_reel_type(df_reel_enc, "CLIENT HORS GROUPE")
        solde_clt_ig = calculate_solde_client(df_solde_clt,"intergroupe")
        solde_clt_hg = calculate_solde_client(df_solde_clt,"hors groupe")
        
        with st.expander(f"Encaissement |  Prévu: {format_montant_fr(prevu_ig + prevu_hg)} | Réalisé: {format_montant_fr(reel_enc_ig + reel_enc_hg)}"):
            with st.container():
                cols = st.columns(7)
                cols[0].markdown("**Intergroupe**")
                cols[1].write("   ")
                cols[2].write("   ")
                cols[3].markdown(f"**{format_montant_fr(prevu_ig)}**")
                cols[4].markdown(f"**{format_montant_fr(reel_enc_ig)}**")
                cols[5].markdown(f"**{format_montant_fr(solde_clt_ig)}**") # Remarque 1
                cols[6].markdown("0")  # Remarque 2

                cols[0].markdown("**Hors groupe**")
                cols[1].write("   ")
                cols[2].write("   ")
                cols[3].markdown(f"**{format_montant_fr(prevu_hg)}**")
                cols[4].markdown(f"**{format_montant_fr(reel_enc_hg)}**")
                cols[5].markdown(f"**{format_montant_fr(solde_clt_hg)}**")  # Remarque 1
                cols[6].markdown("0")  # Remarque 2

    display_encaissement()

    # --------------------------- Décaissement Sections -------------------------
    def display_decaissement_section(title, items):
    # Calculate totals for the expander label
        total_prevu = sum(item.get('prevu', 0) for item in items)
        total_realise = sum(item.get('realise', 0) for item in items)

        with st.expander(f"{title} | Prévu: {format_montant_fr(total_prevu)} | Réalisé: {format_montant_fr(total_realise)}"):
            for item in items:
                cols = st.columns(7)
                cols[0].markdown(f"**{item['label']}**")
                cols[1].write("")  # Empty column for spacing
                cols[2].write("")  # Empty column for spacing
                cols[3].markdown(f"**{format_montant_fr(item.get('prevu', 0))}**")
                cols[4].markdown(f"**{format_montant_fr(item.get('realise', 0))}**")
                cols[5].markdown("0")  # Remarque 1
                cols[6].markdown("0")  # Remarque 2

    # Define decaissement sections with sample data (replace with your actual data)
    df_decaissement = get_decaissement_frs()
    dec_frs_ig_ap = calculate_decaissement_type(df_decaissement, "FOURNISSEUR INTERGROUPE", [3, 4])
    dec_frs_ig_engage = calculate_decaissement_type(df_decaissement, "FOURNISSEUR INTERGROUPE", [17])
    dec_frs_hg_ap = calculate_decaissement_type(df_decaissement, "FOURNISSEUR HORS GROUPE", [3, 4])
    dec_frs_hg_engage = calculate_decaissement_type(df_decaissement, "FOURNISSEUR HORS GROUPEE", [17])
    df_cnss=get_cnss_mas()
    cnss_a= calculate_cnss_salaire_type(df_cnss,'CNSS')
    df_salaire=get_salaire_mas()
    salaire= calculate_cnss_salaire_type(df_salaire,'SALAIRE') 
    
    df_steg=get_steg() 
    steg_reel=calculate_steg(df_steg)

    df_sonede=get_sonede()
    sonede_reel=calculate_sonede(df_sonede)
    print("-----------------------------------------------------------------------------")
    print(type(steg_reel)) 
    print(steg_reel)  # test=20

    decaissement_sections = [
        {
            "title": "Décaissement Fournisseur Intergroupe",
            "items": [
                {"label": "Fournisseur Intergroupe à prévoir", "prevu": 0, "realise": dec_frs_ig_ap},
                {"label": "Fournisseur Intergroupe Engagé", "prevu": 0, "realise": dec_frs_ig_engage}
            ]
        },
        {
            "title": "Décaissement Fournisseur Horsgroupe",
            "items": [
                {"label": "Fournisseur Horsgroupe à prévoir", "prevu": 0, "realise": dec_frs_hg_ap},
                {"label": "Fournisseur Horsgroupe Engagé", "prevu": 0, "realise": dec_frs_hg_engage}
            ]
        },
        {
            "title": "Décaissement Charge Fix",
            "items": [
                {"label": "STEG", "prevu": 0, "realise": round(steg_reel)},
                {"label": "SONEDE", "prevu": 0, "realise": round(sonede_reel)},
                {"label": "LOCATION", "prevu": 0, "realise": 0}
            ]
        },
        {
            "title": "Salaire",
            "items": [
                {"label": "SALAIRE NET", "prevu": 0, "realise": salaire},
                {"label": "CNSS ECHEANCE", "prevu": 0, "realise": 0},
                {"label": "CNSS A PREVOIR", "prevu": 0, "realise": cnss_a}
            ]
        },
        {
            "title": "Etat et taxe",
            "items": [
                {"label": "NON DEFINIS", "prevu": 0, "realise": 0}
            ]
        },
        {
            "title": "Autre charge Décaissé",
            "items": [
                {"label": "NON DEFINIS", "prevu": 0, "realise": 0}
            ]
        }
    ]

    for section in decaissement_sections:
        display_decaissement_section(section["title"], section["items"])

    # --------------------------- Summary Section -------------------------------
    with st.container(border=True):
        
        cols = st.columns(7)
        cols[0].markdown("**Augmentation / Diminition de la trésorerie**")
        cols[0].markdown("**Trésorerir début du Mois**")
        cols[0].markdown("**Trésorerir Fin du Mois**")
        cols[0].markdown("""**Augmentation / Diminition de la trésorerie**""")

        # Prévu
        cols[1].write(" ") 
        cols[1].markdown(" ")
        cols[1].markdown(" ")
        cols[1].markdown(" ") 
        cols[2].write(" ") 
        cols[2].markdown(" ")
        cols[2].markdown(" ")
        cols[2].markdown(" ")  
        # space 
        cols[3].markdown("**0**")
        cols[3].markdown("**0**")
        cols[3].markdown("**0**") 
        cols[3].markdown("**0**")
        # Réalisé                             
        cols[4].markdown("**0**")
        cols[4].markdown("**0**") 
        cols[4].markdown("**0**")
        cols[4].markdown("**0**") 
        cols[5].markdown("0")  
        cols[5].markdown("0") 
        cols[5].markdown("0") 
        cols[5].markdown("0")     # Remarque 1
        cols[6].markdown("0")   
        cols[6].markdown("0")
        cols[6].markdown("0")
        cols[6].markdown("0")   # Remarque 2

if __name__ == "__main__":
    tresorrerie_mas()