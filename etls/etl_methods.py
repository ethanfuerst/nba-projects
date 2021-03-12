#%%
import os
import pandas as pd
import numpy as np
import datetime
import json
import requests
from nba_api.stats.endpoints import leaguegamelog
from to_sql import pg_connect


def update_game_log(table, game_type, p_t='T'):
    logs = pd.DataFrame(columns=['table_updated', 'time_updated', 'rows_updated', 'start_date', 'end_date'])
    df = pg_connect().query(f'SELECT MAX(season_id) as season_id, MAX(game_date) as date FROM {table}')

    season = 1976 if df.iloc[0]['season_id'] == None else int(df.iloc[0]['season_id'][1:])
    max_date = df.iloc[0]['date']

    if max_date:
        pg_connect().query(f"DELETE FROM {table} WHERE game_date = '{max_date.strftime('%Y-%m-%d')}'")

    # drop values = max date to get rid of potentially still in progress games
    # reload values starting at season where game_date = or after max_date

    end_date = None
    rowcount = 0
    errors = {}
    for i in range(season, 2021):
        try:
            log = leaguegamelog.LeagueGameLog(
                counter=0, 
                direction='ASC', 
                league_id='00', 
                player_or_team_abbreviation=p_t, 
                season=f'{i}-{str(i + 1)[2:]}', 
                season_type_all_star=game_type
            )

            df = log.get_data_frames()[0]
            
            if len(df) == 0:
                continue
            
            df = df[df['WL'].isin(['W', 'L'])].copy()
            df = df.drop(['VIDEO_AVAILABLE', 'FANTASY_PTS'], axis=1, errors='ignore').copy()
            df['OPPONENT'] = df['MATCHUP'].astype(str).str[-3:]

            new_columns = [
                'season_id', 'team_id', 'team_abbrev', 'team_name',
                'game_id', 'game_date', 'matchup', 'wl', 'min',
                'fgm', 'fga', 'fg_pct', 'fg3m', 'fg3a', 'fg3_pct',
                'ftm', 'fta', 'ft_pct',
                'oreb', 'dreb', 'reb',
                'ast', 'stl', 'blk', 'tov',
                'pf', 'pts', 'plus_minus', 'opponent']
            
            if p_t == 'P':
                new_columns = new_columns[:1] + ['player_id', 'player_name'] + new_columns[1:]

            df.columns = new_columns

            df['game_date'] = pd.to_datetime(df['game_date'])
            if max_date:
                df = df[df['game_date'].dt.date >= max_date].copy()
            
            df[['fg_pct', 'fg3_pct', 'ft_pct']] = round(df[['fg_pct', 'fg3_pct', 'ft_pct']], 3).copy()

            end_date = df['game_date'].max()
            rowcount += len(df)

            pg_connect().insert(table=table, df=df)
        
        except requests.exceptions.ReadTimeout:
            errors[i] = 'ReadTimeoutError'
            break
        except Exception as e:
            print(i, e)
            errors[i] = str(e)
    
    logs = logs.append({
        'table_updated':table,
        'time_updated':datetime.datetime.now(), #.strftime('%Y-%m-%d %H:%M:%S')
        'rows_updated':rowcount,
        'start_date':max_date,
        'end_date':end_date,
        'errors':json.dumps(errors)
    }, ignore_index=True).replace({np.nan:None})

    pg_connect().insert(table='logs_nba', df=logs)

#%%
if __name__ == '__main__':
    update_game_log('nba_reg_log', 'Regular Season')
    update_game_log('nba_playoff_log', 'Playoffs')
    update_game_log('nba_all_star_log', 'All Star')
    update_game_log('nba_player_reg_log', 'Regular Season', 'P')
    update_game_log('nba_player_playoff_log', 'Playoffs', 'P')
    update_game_log('nba_player_all_star_log', 'All Star', 'P')

# %%
