import sys
import pygame
from arrow import Arrow
from wall import Wall
from enemy_spawn import EnemySpawn
from enemy import Enemy
from next_lvl import Exit
from treasure import Treasure
from foods import Food


def change_sprite(side):
    coords = {'left': (900, 50, 50, 50), 'right': (
        900, 150, 50, 50), 'up': (900, 100, 50, 50), 'down': (950, 0, 50, 50), 'topright': (1050, 100, 50, 50),
        'topleft': (1050, 50, 50, 50), 'bottomright': (1050, 150, 50, 50),  'bottomleft': (1050, 0, 50, 50)}
    rect = pygame.Rect((0, 0, 38, 38))
    sheet = pygame.image.load('assets/elf.png').convert()
    sheet = pygame.transform.scale(
        sheet, (1198, 832))
    image = pygame.Surface((49, 49)).convert()
    image.blit(sheet, (0, 0), coords[side])
    transColor = image.get_at((2, 2))
    image.set_colorkey(transColor)
    image = pygame.transform.scale(
        image, (40, 40))
    return image


def check_keydown_events(event, ai_settings, screen, player, arrows):
    if event.key == pygame.K_z:
        fire_arrow(ai_settings, arrows, screen, player)
    elif event.key == pygame.K_RIGHT:
        player.moving_right = True
        if player.moving_up == True:
            player.image = change_sprite('topright')
            player.side = 'topright'
        elif player.moving_down == True:
            player.image = change_sprite('bottomright')
            player.side = 'bottomright'
        else:
            player.image = change_sprite('right')
            player.side = 'right'
    elif event.key == pygame.K_LEFT:
        player.moving_left = True
        if player.moving_up == True:
            player.image = change_sprite('topleft')
            player.side = 'topleft'
        elif player.moving_down == True:
            player.image = change_sprite('bottomleft')
            player.side = 'bottomleft'
        else:
            player.image = change_sprite('left')
            player.side = 'left'
    elif event.key == pygame.K_UP:
        player.moving_up = True
        if player.moving_right == True:
            player.image = change_sprite('topright')
            player.side = 'topright'
        elif player.moving_left == True:
            player.image = change_sprite('topleft')
            player.side = 'topleft'
        else:
            player.image = change_sprite('up')
            player.side = 'up'
    elif event.key == pygame.K_DOWN:
        player.moving_down = True
        if player.moving_right == True:
            player.image = change_sprite('bottomright')
            player.side = 'bottomright'
        elif player.moving_left == True:
            player.image = change_sprite('bottomleft')
            player.side = 'bottomleft'
        else:
            player.image = change_sprite('down')
            player.side = 'down'
    elif event.key == pygame.K_ESCAPE:
        ai_settings.game_status = 0
        ai_settings.current_lvl = 1
    elif event.key == pygame.K_x:
        if ai_settings.game_status != 1:
            ai_settings.score = 0
            ai_settings.current_lvl = 1
        ai_settings.game_status = 1


def keyup(event, player):
    keys = pygame.key.get_pressed()
    if event.key == pygame.K_RIGHT:
        player.moving_right = False
        if (player.side == 'bottomright' and keys[pygame.K_DOWN] == 0) or (player.side == 'topright' and keys[pygame.K_UP] == 0):
            pass
        elif player.moving_up == True:
            player.image = change_sprite('up')
            player.side = 'up'
        elif player.moving_down == True:
            player.image = change_sprite('down')
            player.side = 'down'
        elif player.moving_left == True:
            player.image = change_sprite('left')
            player.side = 'left'
    elif event.key == pygame.K_LEFT:
        player.moving_left = False
        if (player.side == 'bottomleft' and keys[pygame.K_DOWN] == 0) or (player.side == 'topleft' and keys[pygame.K_UP] == 0):
            pass
        elif player.moving_up == True:
            player.image = change_sprite('up')
            player.side = 'up'
        elif player.moving_down == True:
            player.image = change_sprite('down')
            player.side = 'down'
        elif player.moving_right == True:
            player.image = change_sprite('right')
            player.side = 'right'
    elif event.key == pygame.K_UP:
        player.moving_up = False
        if (player.side == 'topright' and keys[pygame.K_RIGHT] == 0) or (player.side == 'topleft' and keys[pygame.K_LEFT] == 0):
            pass
        elif player.moving_left == True:
            player.image = change_sprite('left')
            player.side = 'left'
        elif player.moving_right == True:
            player.image = change_sprite('right')
            player.side = 'right'
        elif player.moving_down == True:
            player.image = change_sprite('down')
            player.side = 'down'
    elif event.key == pygame.K_DOWN:
        player.moving_down = False
        if (player.side == 'bottomright' and keys[pygame.K_RIGHT] == 0) or (player.side == 'bottomleft' and keys[pygame.K_LEFT] == 0):
            pass
        elif player.moving_left == True:
            player.image = change_sprite('left')
            player.side = 'left'
        elif player.moving_right == True:
            player.image = change_sprite('right')
            player.side = 'right'
        elif player.moving_up == True:
            player.image = change_sprite('up')
            player.side = 'up'
    elif event.key == pygame.K_q:
        sys.exit()


def check_game_event(ai_settings, screen, player, arrows):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, player, arrows)
        elif event.type == pygame.KEYUP:
            keyup(event, player)


def fire_arrow(ai_settings, arrows, screen, player):
    if len(arrows) < ai_settings.arrow_allowed:
        new_arrow = Arrow(ai_settings, screen, player)
        arrows.add(new_arrow)


def spawn_mob(maps, ai_settings, screen, mobs, player, mobs_spawn):
    for i in mobs_spawn:
        i.timer -= 10
        flag = True
        for j in mobs:
            if i.x - j.x < 60 and ((i.y - j.y)**2)**(1/2) < 28:
                flag = False
                break
        if i.timer <= 0 and player.mobs_limit >= 0 and flag:
            i.timer = 1000
            new_mob = Enemy(ai_settings, screen, i.x-30, i.y, maps, mobs)
            mobs.add(new_mob)
            player.mobs_limit -= 1


def update_arrows(arrows, ai_settings):
    for arrow in arrows:
        if arrow.rect.bottom < 0 or arrow.rect.bottom > ai_settings.screen_height or arrow.rect.left < 0 or arrow.rect.left > ai_settings.screen_width:
            arrows.remove(arrow)
            arrow.kill()


def draw_text(surf, text, size, x, y):
    font_name = pygame.font.match_font('arial')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_lvl(walls, ai_settings, screen, maps, mobs_spawn, exits, treasure, foods, flag):
    lvl = maps.levels[ai_settings.current_lvl]
    for row in range(len(lvl)):
        for column in range(len(lvl[0])):

            if lvl[row][column] == 1:
                if flag:
                    newall = Wall(ai_settings, screen, maps, column, row)
                    walls.add(newall)
            if lvl[row][column] == 3:
                if flag:
                    spawn = EnemySpawn(ai_settings, screen, maps, column, row)
                    mobs_spawn.add(spawn)
                screen.blit(maps.textures_floor,
                            (column*40, row*40), (0, 0, 40, 40))
            if lvl[row][column] == 9:
                if flag:
                    newexit = Exit(ai_settings, screen, maps, column, row)
                    exits.add(newexit)
            if lvl[row][column] == 4:
                if flag:
                    newt = Treasure(ai_settings, screen, maps, column, row)
                    treasure.add(newt)
                screen.blit(maps.textures_floor,
                            (column*40, row*40), (0, 0, 40, 40))
            if lvl[row][column] == 5:
                if flag:
                    newf = Food(ai_settings, screen, maps, column, row)
                    foods.add(newf)
                screen.blit(maps.textures_floor,
                            (column*40, row*40), (0, 0, 40, 40))
            else:
                screen.blit(maps.textures_floor,
                            (column*40, row*40), (0, 0, 40, 40))


def arrow_damage(mobs, arrows, mobs_spawn, player, ai_settings, walls, treasure, foods):
    pygame.sprite.groupcollide(walls, arrows, False, True)
    pygame.sprite.groupcollide(treasure, arrows, False, True)
    pygame.sprite.groupcollide(foods, arrows, False, True)
    damaged_mobs = pygame.sprite.groupcollide(mobs, arrows, False, True)
    damaged_spawn = pygame.sprite.groupcollide(mobs_spawn, arrows, False, True)
    for i in damaged_spawn:
        i.hp -= player.atk
        if i.hp <= 0:
            i.kill()
            ai_settings.score += i.cost
    for i in damaged_mobs:
        i.hp -= player.atk
        if i.hp <= 0:
            i.kill()
            ai_settings.score += i.cost
            player.mobs_limit += 1


def object_hit(player, walls, mobs_spawn, mobs, ai_settings, exits, treasure, food, maps):
    hits = pygame.sprite.spritecollide(player, walls, False)
    hits_spawn = pygame.sprite.spritecollide(player, mobs_spawn, False)
    next_lvl = pygame.sprite.spritecollide(player, exits, False)
    if next_lvl:
        next_lvl[0].kill()
        ai_settings.current_lvl += 1
    treasure_find = pygame.sprite.spritecollide(player, treasure, False)
    for i in treasure_find:
        ai_settings.score += i.value
        maps.levels[ai_settings.current_lvl][int(i.rect.y /
                                             ai_settings.block_size)][int(i.rect.x/ai_settings.block_size)] = 0
        i.kill()
    food_find = pygame.sprite.spritecollide(player, food, False)
    for i in food_find:
        if player.hp+i.value <= player.max_hp:
            player.hp += i.value
        else:
            player.hp = player.max_hp
        maps.levels[ai_settings.current_lvl][int(i.rect.y /
                                             ai_settings.block_size)][int(i.rect.x/ai_settings.block_size)] = 0
        i.kill()
    mobs_hit = pygame.sprite.spritecollide(player, mobs, False)
    for i in mobs_hit:
        i.kill()
        player.mobs_limit += 1
        player.hp -= i.atk
        if player.hp <= 0:
            ai_settings.game_status = 2

    l_coin = 0
    r_coin = 0
    t_coin = 0
    b_coin = 0
    for i in hits+hits_spawn:
        if i.rect.top <= player.rect.bottom and player.rect.centery < i.rect.centery:
            b_coin += 1
            player.speed_factor_collise[3] = 0
            player.y -= 1
            player.rect.centery -= 1
        elif i.rect.bottom >= player.rect.top and player.rect.centery > i.rect.centery:
            t_coin += 1
            player.speed_factor_collise[2] = 0
            player.y += 1
            player.rect.centery += 1
        if i.rect.left <= player.rect.right and player.rect.centerx < i.rect.centerx:
            r_coin += 1
            player.speed_factor_collise[1] = 0
            player.x -= 1
            player.rect.centerx -= 1
        elif i.rect.right >= player.rect.left and player.rect.centerx > i.rect.centerx:
            l_coin += 1
            player.speed_factor_collise[0] = 0
            player.x += 1
            player.rect.centerx += 1
    if l_coin == 0:
        player.speed_factor_collise[0] = 1
    if r_coin == 0:
        player.speed_factor_collise[1] = 1
    if t_coin == 0:
        player.speed_factor_collise[2] = 1
    if b_coin == 0:
        player.speed_factor_collise[3] = 1


def update_screen(ai_settings, screen, player, all_sprites, arrows, maps, walls, mobs, mobs_spawn, exits, treasure, foods, first_draw=1):
    screen.fill([255, 0, 0])
    draw_lvl(walls, ai_settings, screen, maps,
             mobs_spawn, exits, treasure, foods, first_draw)
    walls.update()
    walls.draw(screen)
    all_sprites.update()
    all_sprites.draw(screen)
    mobs_spawn.update()
    mobs_spawn.draw(screen)
    exits.update()
    exits.draw(screen)
    treasure.update()
    treasure.draw(screen)
    foods.update()
    foods.draw(screen)
    player.hp -= 0.02
    spawn_mob(maps, ai_settings, screen, mobs, player, mobs_spawn)
    mobs.update()
    mobs.draw(screen)
    object_hit(player, walls, mobs_spawn, mobs,
               ai_settings, exits, treasure, foods, maps)
    update_arrows(arrows, ai_settings)
    arrows.update()
    arrows.draw(screen)
    arrow_damage(mobs, arrows, mobs_spawn, player,
                 ai_settings, walls, treasure, foods)
    draw_text(screen, 'HP: '+str(int(player.hp)), 18,
              ai_settings.screen_width*0.90, 40)
    draw_text(screen, 'SCORE: '+str(ai_settings.score),
              18, ai_settings.screen_width*0.90, 70)
    draw_text(screen, 'LVL '+str(ai_settings.current_lvl),
              18, ai_settings.screen_width*0.90, 100)
    pygame.display.flip()


def draw_end_screen(screen, ai_settings):
    screen.fill([0, 0, 0])
    draw_text(screen, 'YOU DEAD',
              25, ai_settings.screen_width/2, ai_settings.screen_height/2)
    draw_text(screen, 'SCORE: '+str(ai_settings.score),
              38, ai_settings.screen_width/2, ai_settings.screen_height/2 + 60)
    draw_text(screen, 'Press Esc to go menu or X to restart',
              38, ai_settings.screen_width/2, ai_settings.screen_height/2 + 100)
    pygame.display.flip()


def draw_menu_screen(screen, ai_settings):
    screen.fill([0, 0, 0])
    draw_text(screen, 'PRESS X to start the game',
              38, ai_settings.screen_width/2, ai_settings.screen_height/2)
    pygame.display.flip()


def draw_win_screen(screen, ai_settings):
    screen.fill([100, 100, 100])
    draw_text(screen, 'YOU WIN!!!',
              25, ai_settings.screen_width/2, ai_settings.screen_height/2)
    draw_text(screen, 'SCORE: '+str(ai_settings.score),
              38, ai_settings.screen_width/2, ai_settings.screen_height/2 + 60)
    draw_text(screen, 'Press Esc to go menu or X to restart',
              38, ai_settings.screen_width/2, ai_settings.screen_height/2 + 100)
    pygame.display.flip()
