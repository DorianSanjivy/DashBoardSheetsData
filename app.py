import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import matplotlib.pyplot as plt
import json

title_placeholder = st.empty()
players_placeholder = st.empty()
plays_placeholder = st.empty()
active_users_placeholder = st.empty()

chart_placeholder = st.empty()
active_users_chart_placeholder = st.empty()

def get_data_from_gsheet(json_file, sheet_url):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_file, scope)
    client = gspread.authorize(creds)
    
    sheet = client.open_by_url(sheet_url).sheet1
    data = sheet.get_all_values()  # Utilise get_all_values plutôt que get_all_records
    df = pd.DataFrame(data[1:], columns=data[0])  # Convertir les données en DataFrame en utilisant la première ligne comme noms de colonnes

    # Renommez les colonnes comme souhaité
    df.columns = ['timestamp', 'players', 'plays', 'active_users']
    
    return df

def plot_data(df):
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Plot for Plays
    fig1, ax1 = plt.subplots(figsize=(10,5))
    ax1.plot(df['timestamp'], df['plays'], marker='o', linestyle='-')
    ax1.set_ylim([15000, df['plays'].max() + 500]) # Setting Y-axis lower limit to 14000
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Plays')
    ax1.set_title('Number of Plays Over Time')
    chart_placeholder.pyplot(fig1)

    # Plot for Active Users
    fig2, ax2 = plt.subplots(figsize=(10,5))
    ax2.plot(df['timestamp'], df['active_users'], marker='o', linestyle='-')
    ax2.set_ylim([0, df['active_users'].max() + 5]) # Setting Y-axis lower limit to 0
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Active Users')
    ax2.set_title('Number of Active Users Over Time')
    active_users_chart_placeholder.pyplot(fig2)

st.title('Google Sheets Data Visualization with Streamlit')

# Read data from Google Sheet
json_file = 'ageless-union-400617-cb593b8312e6.json' # Update this with the path to your downloaded .json file
sheet_url = 'https://docs.google.com/spreadsheets/d/13L7R6ORr7507D1p67usZX2UGnQ0P82Ufa1xp82TmHW0/edit#gid=0' # Update this with the URL of your Google Sheet
df = get_data_from_gsheet(json_file, sheet_url)

if __name__ == "__main__":
    # Adaptez cette partie selon les données de votre Google Sheets
    players = len(df)
    plays = df['plays'].sum()
    active_users = df['active_users'].sum()

    title_placeholder.title("Webpage Data")
    players_placeholder.write(f"Players: {players}")
    plays_placeholder.write(f"Plays: {plays}")
    active_users_placeholder.write(f"Active Users: {active_users}")
  
    plot_data(df)


