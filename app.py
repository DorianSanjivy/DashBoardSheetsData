import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import matplotlib.pyplot as plt

def get_data_from_gsheet(json_file, sheet_url):
    # Setup the credentials
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_file, scope)
    client = gspread.authorize(creds)

    # Open the Google Sheet using its URL
    sheet = client.open_by_url(sheet_url).sheet1
    data = sheet.get_all_records()

    return pd.DataFrame(data)

st.title('Google Sheets Data Visualization with Streamlit')

# Read data from Google Sheet
json_file = 'ageless-union-400617-cb593b8312e6.json' # Update this with the path to your downloaded .json file
sheet_url = 'https://docs.google.com/spreadsheets/d/13L7R6ORr7507D1p67usZX2UGnQ0P82Ufa1xp82TmHW0/edit#gid=0' # Update this with the URL of your Google Sheet
df = get_data_from_gsheet(json_file, sheet_url)

# Display data
st.write(df)

# Example plotting: Let's assume you have 'X' and 'Y' columns in your data to plot
st.write('Simple Plot')
fig, ax = plt.subplots()
ax.plot(df['X'], df['Y'])
st.pyplot(fig)


