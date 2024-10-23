import streamlit as st
import pandas as pd

# Assuming df is your DataFrame from the scraping code
df = pd.read_csv("player_data.csv")  # Or directly use the df if in memory

# Streamlit app
st.title('Uppställningar Division 4 Norra 2024-25')

# List of teams for selection
teams = df['Lag'].unique()

# Sidebar for team selection
team_selected = st.sidebar.selectbox('Välj lag:', teams)

# Display the player stats for the selected team
st.header(f'Statistik för {team_selected}')

# Filter data for the selected team
team_data = df[df['Lag'] == team_selected]

# Display the table of players and their position stats
st.write(team_data[['Spelare', 'Position 1', 'Position 2', 'Position 3', 'Position 4']])

# Option to download the data as CSV
st.download_button("Ladda ner lagets statistik som CSV", team_data.to_csv(index=False), "team_stats.csv")