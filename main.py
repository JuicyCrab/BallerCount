import streamlit as st
from api.nba_data import get_player_stats

st.title("NBA Player Stats")
player_name = st.text_input("Enter the player's full name to see stats: ")


@st.cache_data
def load_data(name):
    return get_player_stats(name)

if player_name:
    df = load_data(player_name)

    if df is None:
        st.warning(f"There are no stats for {player_name}")
    else:
        df.rename(columns={
            'SEASON_ID': 'Season',
            'TEAM_ABBREVIATION': 'Team',
            'PLAYER_AGE': 'Age'
        }, inplace=True)
        st.dataframe(df)



