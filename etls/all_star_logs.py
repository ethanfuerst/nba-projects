from etl_methods import update_game_log

if __name__ == '__main__':
    update_game_log('nba_all_star_log', 'All Star')
    update_game_log('nba_player_all_star_log', 'All Star', 'P')