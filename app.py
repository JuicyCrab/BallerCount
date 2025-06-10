import streamlit as st
import pandas as pd 
import numpy as np
from api.nba_data import get_player_stats
import db.auth 
from db.database import Stats 



if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
    
@st.cache_data
def load_data(name):
    return get_player_stats(name)

db.auth.create_users_table()

if not st.session_state.logged_in:
    st.title("Welcome to BallerCount")
    choice = st.selectbox('Login/SignUp', ['Login', 'SignUp'])

    if choice == 'Login':
        email = st.text_input("Username")
        password = st.text_input("Password", type='password')
        if st.button('Login'):
            if db.auth.login_user(email, password):
                st.session_state.logged_in = True
                st.session_state.username = email
                st.success("Logged in!")
                st.rerun()
            else:
                st.error("Invalid credentials")

    else:
        email = st.text_input("Enter an username")
        password = st.text_input("Create a password", type='password')
        reenter_password = st.text_input("Re-enter the password", type='password')
        if password != reenter_password:
            st.warning("The passwords are different")
        elif st.button("Create my account"):
            if db.auth.register_user(email, password):
                st.success("Account created! Please log in.")
            else:
                st.error("Username already exists.")
else:
    st.sidebar.write(f"👤 Logged in as {st.session_state.username}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

    page = st.sidebar.selectbox("Select a page", ["Login/Signup","Personal Stats","Find a player", "Compare Players", "You vs Pro"])

    if page == "Login/Signup":
        st.title("Welcome to BallerCount")
        choice = st.selectbox('Login/SignUp',['Login', 'SignUp'])
        
        if choice == 'Login':
            email = st.text_input("Email")
            password = st.text_input("Password", type='password')
            st.button('Login')
            
        else:
            email = st.text_input("Enter an email")
            password = st.text_input("Create a password",type='password')
            reenter_password = st.text_input("re-enter the password", type='password')
            if password is not reenter_password:
                st.warning("The passwords are different")
            else: 
                if st.button("Create my account"):
                    pass 

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

            data = {
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

            # Save to DB
            stats_db = Stats()
            stats_db.insert_stats(
                st.session_state.username,
                str(data["Date"]),
                data["Age"],
                data["GP"],
                data["Min"],
                data["FG%"],
                data["FG3%"],
                data["FT%"],
                data["REB"],
                data["Assists"],
                data["STL"],
                data["BLK"],
                data["TOV"],
                data["Fouls"],
                data["PTS"]
            )
            stats_db.close()

            st.success("Stats saved")

            st.session_state.personal_stats_data = pd.DataFrame(data,index=[0])
            st.session_state.personal_stats_styler = st.session_state.personal_stats_data.style.highlight_max(axis=0, color='yellow')
            st.dataframe(st.session_state.personal_stats_styler)

    if page == "Find a player":
        st.title("NBA Player")
        player1 = st.text_input("Enter the player's full name to see stats: ")
        df = load_data(player1)

        if df is None:
            st.error(f"There are no stats for {player1}")
        else:
            df = df.replace(0,np.nan)
            best_stats = df.style.highlight_max(subset=df.columns[2:],color='green', axis=0).highlight_min(subset=df.columns[2:], axis=0, color='red')
            st.dataframe(best_stats)
            st.title(f"{player1} Best and Worst Stats")
            col1,col2 = st.columns(2)
            min_and_max = pd.DataFrame({
                "max": df.max(),
                "min":df.min()
            })
            st.dataframe(min_and_max)

    if page == "Compare Players":
        st.title("NBA Players")
        player_compare_1 = st.text_input("Enter a player")
        player_compare_2 = st.text_input("Enter another player")
        stats1 = load_data(player_compare_1)
        stats2 = load_data(player_compare_2)
        col1,col2 = st.columns(2)
        if player_compare_1 and player_compare_2:
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
        with col1:
            min_max_player1 = pd.DataFrame({
                "max": stats1.max(),
                "min" : stats1.min()
            })
            st.dataframe(min_max_player1)
        with col2:
            min_max_player2 = pd.DataFrame({
                "max": stats2.max(),
                "min": stats2.min()
            })
            st.dataframe(min_max_player2)


    if page == "You vs Pro":
        st.title("You vs Pro")
        col1, col2 = st.columns(2)
        
        with col1:
            nba_player = st.text_input("Which NBA Player: ")
            df = load_data(nba_player)
            if df is None:
                st.error("Invalid Player")
            else:
                df = df.drop(columns=['GS','FGM','FGA','FG3M', 'FG3A', 'FTM', 'FTA','OREB','DREB'])
                subset_cols = df.columns[1:]
                st.session_state.pro_player_data = df[subset_cols]
                st.session_state.pro_player_style = df.style.highlight_max(subset=subset_cols, color='green')
                st.dataframe(st.session_state.pro_player_style)
    
        with col2:
            st.subheader("Your stats")
            # Load all personal stats from session or DB as a DataFrame with multiple rows (each with a Date)
            if "all_personal_stats" in st.session_state:
                personal_stats_df = st.session_state.all_personal_stats
                personal_stats_df['Date'] = pd.to_datetime(personal_stats_df['Date'])  # Ensure Date column is datetime
                
                # Date range picker (default range is from earliest to latest date in your data)
                min_date = personal_stats_df['Date'].min().date()
                max_date = personal_stats_df['Date'].max().date()
                date_range = st.date_input("Select date range", [min_date, max_date], min_value=min_date, max_value=max_date)
                
                # Defensive: ensure date_range is a tuple or list of two dates
                if len(date_range) == 2:
                    start_date, end_date = date_range
                    # Filter the DataFrame for dates between start_date and end_date inclusive
                    filtered_df = personal_stats_df[
                        (personal_stats_df['Date'] >= pd.Timestamp(start_date)) & 
                        (personal_stats_df['Date'] <= pd.Timestamp(end_date))
                    ]
                    
                    if filtered_df.empty:
                        st.warning("No personal stats in the selected date range.")
                    else:
                        # Show filtered stats - you can customize here, e.g., mean, min, max
                        st.write(f"Showing stats from {start_date} to {end_date}:")
                        st.dataframe(filtered_df.style.highlight_max(subset=filtered_df.columns.difference(['Date']), color='yellow'))
                        
                        # Show summary stats for that range
                        summary = pd.DataFrame({
                            "min": filtered_df.min(numeric_only=True),
                            "max": filtered_df.max(numeric_only=True),
                            "mean": filtered_df.mean(numeric_only=True).round(2)
                        })
                        st.write("Summary stats in this range:")
                        st.dataframe(summary)
                else:
                    st.error("Please select a valid date range.")
            else:
                st.warning("Please fill out your personal stats first (and ensure multiple entries are saved).")
    
    # Rest of your You vs Pro code...
        with col1:
            st.write("Best and Worst Player stats")
            max_min_player = pd.DataFrame({
                "min": st.session_state.pro_player_data.min(),
                "max": st.session_state.pro_player_data.max()
            })
            st.dataframe(max_min_player)

        with col1:        
            st.write("Best and Worst Player stats")
            max_min_player = pd.DataFrame({
                "min": st.session_state.pro_player_data.min(),
                "max": st.session_state.pro_player_data.max()})
            st.dataframe(max_min_player)
        with col2:
            if "personal_stats_data" in st.session_state:
                st.write("Best and Worst Personal stats")
                personal_stats = pd.DataFrame({
                    "min": st.session_state.personal_stats_data.min(),
                    "max": st.session_state.personal_stats_data.min()})
                st.dataframe(personal_stats)
