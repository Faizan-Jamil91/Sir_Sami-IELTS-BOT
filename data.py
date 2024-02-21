import streamlit as st
import sqlite3
import pandas as pd
import os
import re

# Function to fetch data from SQLite database into DataFrame
def fetch_data_from_database():
    conn = sqlite3.connect('ielts.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user_data")
    rows = cursor.fetchall()

    df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])

    conn.close()
    return df

# Function to import data from CSV file into DataFrame
def import_data_from_csv(csv_file):
    df = pd.read_csv(csv_file)
    return df

# Function to export DataFrame to CSV file with unique phone numbers
def export_data_to_csv(df):
    # Check if 'phone_number' column exists in the DataFrame
    if 'phone' in df.columns:
        # Remove duplicates based on the phone number column
        df_unique = df.drop_duplicates(subset='phone')
        
        file_path = "exported_data.csv"
        df_unique.to_csv(file_path, index=False)
        return file_path
    else:
        st.error("The 'phone_number' column does not exist in the DataFrame.")

# Main Streamlit code
st.title('Data Import and Export')

# Option to import data from CSV file
csv_file = st.file_uploader("Upload CSV file", type=['csv'])

if csv_file is not None:
    st.write("Imported CSV data:")
    df_csv = import_data_from_csv(csv_file)
    st.write(df_csv)

# Fetch data from database and display in DataFrame
st.subheader('Data from SQLite Database:')
df_db = fetch_data_from_database()

# Search option
search_query = st.text_input("Search by name or any other attribute:")

if search_query:
    regex = re.compile(search_query, re.IGNORECASE)
    df_db = df_db[df_db.apply(lambda row: any(regex.search(str(cell)) for cell in row), axis=1)]

st.write(df_db)

# Option to export DataFrame to CSV file
if st.button('Export Data to CSV'):
    file_path = export_data_to_csv(df_db)
    st.success(f'Data exported successfully!')

    # Create a download link for the exported file
    st.download_button(
        label="Download CSV file",
        data=open(file_path, 'rb').read(),
        file_name='exported_data.csv',
        mime='text/csv'
    )

# Remove the exported file if it exists
if os.path.exists("exported_data.csv"):
    os.remove("exported_data.csv")
