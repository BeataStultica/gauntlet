def evaluation_function(game):
    player_turn = game.get_player_turn()
    #opposite_player_turn = 1 if player_turn == 0 else 0
    #utility = 0
    utility = check_player_utility(player_turn, game)

    #utility += check_player_utility(opposite_player_turn,  game)

    return utility


def check_player_utility(player_turn, game):
    utility = 0
    treas_coord = []
    food_coord = []
    key_coord = False
    exit_coord = False
    for k in range(len(game.state)):
        for n in range(len(game.state[0])):
            if game.state[k][n] == 9:
                exit_coord = [k, n]
            if game.state[k][n] == 8:
                key_coord = [k, n]
            if game.state[k][n] == 4:
                treas_coord.append([k, n])
            if game.state[k][n] == 5:
                food_coord.append([k, n])
    # if player_turn == 0:
    for i in game.mobs_coord:
        utility -= 1/(((game.player_x - i[1]) **
                       2 + (game.player_y - i[0])**2)**(1/2)+0.0001)
    # if player_turn == 1:
    if key_coord:
        utility += 100*1/(((game.player_x - key_coord[1]) **
                           2 + (game.player_y - key_coord[0])**2)**(1/2)+0.0001)
    else:
        utility += 100*1/(((game.player_x - exit_coord[1]) **
                           2 + (game.player_y - exit_coord[0])**2)**(1/2)+0.0001)
    for i in treas_coord:
        value = 1/(((game.player_x - i[1]) **
                    2 + (game.player_y - i[0])**2)**(1/2)+0.0001)
        if value >= 1/2:
            utility += value
        else:
            utility += 0.3*value
    if game.player.hp < 500:
        for i in food_coord:
            value = 1/(((game.player_x - i[1]) **
                        2 + (game.player_y - i[0])**2)**(1/2)+0.0001)
            if value >= 1/2:
                utility += value
            else:
                utility += 0.4*value
    return utility


def result_function(node, a):
    children = node.get_children()
    return children[a]
