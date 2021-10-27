from path_find_algo import a_star_search, bfs


def evaluation_function(game, settings):

    utility = check_player_utility(game, settings)

    return utility


def check_player_utility(game, settings):
    utility = 0
    treas_coord = []
    food_coord = []
    key_coord = False
    exit_coord = False
    mobs_coord = []
    player_coord = ()
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
            if game.state[k][n] == 13:
                mobs_coord.append([k, n])
            if game.state[k][n] == 14:
                player_coord = (k, n)
    # if player_turn == 0:
    # for i in mobs_coord:
    #    utility -= 4*1/(((player_coord[1] - i[1]) **
    #                     2 + (player_coord[0] - i[0])**2)**(1/2)+0.0001)
    # if player_turn == 1:
    if key_coord:
        a = bfs(settings.key_dict,
                player_coord, settings.key_coord)
        # for i in game.state:
        #    print(i)
        # print(settings.maps_dict)
        # print(player_coord)
        # print(settings.key_coord)
        # print(a)
        # if len(a) + settings.last_v == 1:
        utility += -(len(a))
        # else:
        #    utility += 99
    else:
        utility += -(len(bfs(settings.exit_dict,
                             (game.player_y, game.player_x), tuple(settings.exit_coord))))
    # for i in treas_coord:
    #    value = 1/(((player_coord[1] - i[1]) **
    #                2 + (player_coord[0] - i[0])**2)**(1/2)+0.0001)
    #    if value >= 1/2:
    #        utility += 2*value
        # else:
        #    utility += 0.5*value
    if game.player.hp < 500:
        for i in food_coord:
            value = 1/(((player_coord[1] - i[1]) **
                        2 + (player_coord[0] - i[0])**2)**(1/2)+0.0001)
            if value >= 1/2:
                utility += 2*value
            # else:
            #    utility += value
    return utility


def result_function(node, a):
    children = node.get_children()
    return children[a]
