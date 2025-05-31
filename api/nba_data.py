#functions to pull player stats with the nba_api
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players 


def get_player_id(player_name):
    find_player = players.find_players_by_full_name(player_name)
    if not find_player: 
        return None
    player_id = find_player[0]['id']
    return player_id
    
def get_player_stats(player_name):
    player_id = get_player_id(player_name)
    if not player_id:
        return None 
    career = playercareerstats.PlayerCareerStats(player_id=player_id)
    df = career.get_data_frames()[0]
    if 'PLAYER_ID' in df.columns or 'TEAM_ID' in df.columns or 'LEAGUE_ID':
        df = df.drop(columns=['PLAYER_ID', 'TEAM_ID', 'LEAGUE_ID'])
    df.rename(columns={
            'SEASON_ID': 'Season',
            'TEAM_ABBREVIATION': 'Team',
            'PLAYER_AGE': 'Age',
            'FG_PCT': 'FG%',
            'FG3_PCT':'FG3%',
            'FT_PCT':'FT%',
            'PF':'Fouls'
        }, inplace=True)
    df = df.iloc[:,1:]
    return df

