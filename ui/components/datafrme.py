import streamlit as st
import pandas as pd

def display_dataframe(df: pd.DataFrame, title: str = None):
    """
    Display a pandas DataFrame in Streamlit with optional title.

    Args:
        df (pd.DataFrame): The DataFrame to display.
        title (str, optional): The title of the DataFrame. Defaults to None.
    """
    if title:
        st.subheader(title)
    st.dataframe(df, use_container_width=True, hide_index=True)

def display_dataframe_details(df: pd.DataFrame, title: str = None, 
                            columns: list = None, type_filter: str = None):
    """
    Display a pandas DataFrame in Streamlit with optional title, specific columns, and type filter.

    Args:
        df (pd.DataFrame): The DataFrame to display.
        title (str, optional): The title of the DataFrame. Defaults to None.
        columns (list, optional): List of column names to display. Defaults to None (all columns).
        type_filter (str, optional): Value to filter the 'Type' column. Defaults to None (no filter).
    """
    if title:
        st.subheader(title)
    
    # Create a copy to avoid modifying the original DataFrame
    filtered_df = df.copy()
    
    # Apply type filter if provided and 'Type' column exists
    if type_filter and 'Type' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['Type'] == type_filter]
    
    # Select columns to display
    if columns:
        # Only include columns that exist in the DataFrame
        display_columns = [col for col in columns if col in filtered_df.columns]
    else:
        display_columns = filtered_df.columns.tolist()
    
    # Create a display DataFrame with formatted dates
    display_df = filtered_df[display_columns].copy()
    
    # Format datetime columns
    for col in display_columns:
        if pd.api.types.is_datetime64_any_dtype(display_df[col]):
            # Convert datetime to dd/mm/yy string
            display_df[col] = pd.to_datetime(display_df[col]).dt.strftime('%d/%m/%y')
        elif pd.api.types.is_object_dtype(display_df[col]):
            # Attempt to parse as date and convert to dd/mm/yy if possible
            try:
                parsed_dates = pd.to_datetime(display_df[col], errors='coerce')
                # Only convert if at least one valid date was found
                if not parsed_dates.isna().all():
                    display_df[col] = parsed_dates.dt.strftime('%d/%m/%y')
            except:
                pass  # Keep original values if conversion fails
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)