from etl_methods import update_game_log

if __name__ == '__main__':
    update_game_log('nba_reg_log', 'Regular Season')
    update_game_log('nba_player_reg_log', 'Regular Season', 'P')