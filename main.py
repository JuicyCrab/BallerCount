import streamlit as st
import pandas as pd 
from api.nba_data import get_player_stats

@st.cache_data
def load_data(name):
    return get_player_stats(name)



page = st.sidebar.selectbox("Select a page", ["Personal Stats","Find a player", "Compare Players", "You vs Pro"])


if page =="Personal Stats":
    st.subheader("Personal Stats")
    with st.form("my_form"):
        date_input = st.date_input("Date")
        age = st.number_input("Enter your age", min_value=0)
        games_played = st.number_input("Games played", min_value=0)
        total_minutes = st.number_input("Minutes played", min_value=0)

        stat_fields = [
            ("Field Goals Attempted", "fg_attempted"),
            ("Field Goals Made", "fg_made"),
            ("3PT Attempted", "three_pt_attempted"),
            ("3PT Made", "three_pt_made"),
            ("Free Throws Attempted", "ft_attempted"),
            ("Free Throws Made", "ft_made"),
            ("Rebounds", "rebounds"),
            ("Assists", "assists"),
            ("Steals", "steals"),
            ("Blocks", "blocks"),
            ("Turnovers", "turnovers"),
            ("Fouls", "fouls"),
            ("Points", "points")
        ]

        inputs = {}
        for label, key in stat_fields:
            inputs[key] = st.number_input(label, min_value=0)

        submit = st.form_submit_button("Submit")

    if submit:

        def safe_divide(n, d):
            return round(n / d, 2) if d else 0.0

        st.session_state.personal_stats = {
            "Date": date_input,
            "Age": age,
            "GP": games_played,
            "Min": total_minutes,
            "FG%": safe_divide(inputs["fg_made"], inputs["fg_attempted"]),
            "FG3%": safe_divide(inputs["three_pt_made"], inputs["three_pt_attempted"]),
            "FT%": safe_divide(inputs["ft_made"], inputs["ft_attempted"]),
            "REB": inputs["rebounds"],
            "Assists": inputs["assists"],
            "STL": inputs["steals"],
            "BLK": inputs["blocks"],
            "TOV": inputs["turnovers"],
            "Fouls": inputs["fouls"],
            "PTS": inputs["points"]
        }
        st.success("Stats saved")

        df = pd.DataFrame(st.session_state.personal_stats,index=[0])
        new_df = df.style.highlight_max(axis=0, color='yellow')
        st.dataframe(new_df)
    
if page == "Find a player":
    st.title("NBA Player")
    player1 = st.text_input("Enter the player's full name to see stats: ")
    df = load_data(player1)

    if df is None:
        st.error(f"There are no stats for {player1}")
    else:
        st.dataframe(df)


if page == "Compare Players":
    st.title("NBA Players")
    player_compare_1 = st.text_input("Enter a player")
    player_compare_2 = st.text_input("Enter another player")
    stats1 = load_data(player_compare_1)
    stats2 = load_data(player_compare_2)
        
    if player_compare_1 and player_compare_2:
        col1,col2 = st.columns(2)
        if stats1 is None:
            st.error(f"No data for {player_compare_1}")
        
        if stats2 is None:
            st.error(f"No data for {player_compare_2}")
        
        else:
            with col1:
                st.subheader(f"{player_compare_1} Stats")
                st.dataframe(stats1, use_container_width=True)
                
            with col2:
                st.subheader(f"{player_compare_2} Stats")
                st.dataframe(stats2,use_container_width=True)
            

if page == "You vs Pro":
    st.title("You vs Pro")
    col1,col2 = st.columns(2)
    with col1:
        nba_player = st.text_input("Which NBA Player: ")
        df = load_data(nba_player)
        if df is None:
            st.error("Invalid Player")
        else:
            df = df.drop(columns=['GS','FGM','FGA','FG3M', 'FG3A', 'FTM', 'FTA','OREB','DREB'])
            subset_cols = df.columns[1:]
            new_df =df.style.highlight_max(subset=subset_cols, color='green')
            st.dataframe(new_df)
        
    with col2:
        st.subheader("Your stats")
        if "personal_stats" in st.session_state:
            df = pd.DataFrame(st.session_state.personal_stats, index=[0])
            highlighted_df = df.style.highlight_max(subset=df.columns[1:],color="yellow")
            st.dataframe(highlighted_df)
        else:
            st.warning("Please fill out your personal stats first")
            
                
                
            

        
        