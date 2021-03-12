from etl_methods import update_game_log

if __name__ == '__main__':
    update_game_log('nba_playoff_log', 'Playoffs')
    update_game_log('nba_player_playoff_log', 'Playoffs', 'P')