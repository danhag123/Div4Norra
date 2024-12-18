import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import pandas as pd

# Base URL of the league page
base_url = 'https://www.profixio.com/fx/serieoppsett.php?t=SBTF_SERIE_AVD17203&k=LS17203&p=1'

# Dictionary to store team and player position counts
teams_data = defaultdict(lambda: defaultdict(lambda: {1: 0, 2: 0, 3: 0, 4: 0}))

def scrape_match_details(details_url):
    """Scrape individual match details page to extract player positions for the first four individual matches."""
    response = requests.get(details_url)
    if response.status_code != 200:
        return  # Skip if the request failed

    soup = BeautifulSoup(response.text, 'html.parser')

    team_ths = soup.find_all('th', colspan="2")
    if len(team_ths) != 2:
        return  # Skip if we don't find exactly 2 team names

    team_a = team_ths[0].text.strip()
    team_b = team_ths[1].text.strip()

    player_divs = soup.find_all('div', id=lambda x: x and x.startswith('txtnavn_'))[:8]
    if not player_divs:
        return

    for div in player_divs:
        player_name = div.text.strip()
        div_id = div['id']
        team = div_id[-2]
        pos_num = int(div_id[-1])

        if team == 'A':
            teams_data[team_a][player_name][pos_num] += 1
        elif team == 'B':
            teams_data[team_b][player_name][pos_num] += 1

def scrape_main_page():
    """Scrape the main page and find all match detail links."""
    response = requests.get(base_url)
    if response.status_code != 200:
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    details_links = soup.find_all('a', href=lambda x: x and 'serieoppsett_viskamper_rapport.php' in x)
    
    for link in details_links:
        details_url = 'https://www.profixio.com/fx/' + link['href']
        scrape_match_details(details_url)

def convert_to_dataframe():
    """Convert the teams_data dictionary to a pandas DataFrame."""
    data = []
    for team, players in teams_data.items():
        for player, positions in players.items():
            row = {
                'Lag': team,
                'Spelare': player,
                'Position 1': positions[1],
                'Position 2': positions[2],
                'Position 3': positions[3],
                'Position 4': positions[4],
            }
            data.append(row)
    return pd.DataFrame(data)

# Scrape the data
scrape_main_page()

# Convert to DataFrame
df = convert_to_dataframe()

# Save the DataFrame to a CSV file
df.to_csv("player_data.csv", index=False)

print("Data saved to player_data.csv")
