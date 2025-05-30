import streamlit as st
from api.nba_data import get_player_stats

@st.cache_data
def load_data(name):
    return get_player_stats(name)



page = st.sidebar.selectbox("Select a page", ["Find a player", "Compare Players", "You vs Pro"])

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
    nba_player = st.text_input("Which NBA Player: ")
    
    