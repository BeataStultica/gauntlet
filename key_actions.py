import sys
import pygame
from arrow import Arrow
from wall import Wall
from enemy_spawn import EnemySpawn
from enemy import Enemy


def change_sprite(side):
    coords = {'left': (450, 25, 48, 48), 'right': (
        450, 75, 48, 48), 'up': (450, 50, 48, 48), 'down': (475, 0, 48, 48), 'topright': (525, 50, 48, 48),
        'topleft': (525, 25, 48, 48), 'bottomright': (525, 75, 48, 48),  'bottomleft': (525, 0, 48, 48)}
    rect = pygame.Rect(coords[side])
    sheet = pygame.image.load('assets/elf.png').convert()
    image = pygame.Surface((24, 24)).convert()
    image.blit(sheet, (0, 0), rect)
    transColor = image.get_at((2, 2))
    image.set_colorkey(transColor)
    image = pygame.transform.scale(image, (48, 48))
    return image


def check_keydown_events(event, ai_settings, screen, player, arrows):
    # for event in pygame.event.get():
    '''
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] and keys[pygame.K_LEFT] and keys[pygame.K_UP]:
        player.image = change_sprite('top')
        player.side = 'up'
        player.moving_up = True
    elif keys[pygame.K_RIGHT] and keys[pygame.K_LEFT] and keys[pygame.K_DOWN]:
        player.image = change_sprite('down')
        player.side = 'down'
        player.moving_down = True
    '''
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


def check_event(ai_settings, screen, player, arrows):
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


def spawn_mob(maps, ai_settings, screen, mobs, x, y):
    new_mob = Enemy(ai_settings, screen, x, y, maps)
    mobs.add(new_mob)


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


def draw_lvl(walls, ai_settings, screen, maps, mobs_spawn, flag):
    '''
    for wall in walls:
        walls.remove(wall)
        wall.kill()
    for spawn in mobs_spawn:
        mobs_spawn.remove(spawn)
        # spawn.kill()
    '''
    for row in range(len(maps.tilemap1)):
        for column in range(len(maps.tilemap1[0])):

            if maps.tilemap1[row][column] == 1:
                if flag:
                    newall = Wall(ai_settings, screen, maps, column, row)
                    walls.add(newall)
            if maps.tilemap1[row][column] == 3:
                if flag:
                    spawn = EnemySpawn(ai_settings, screen, maps, column, row)
                    mobs_spawn.add(spawn)
                screen.blit(maps.textures_floor,
                            (column*40, row*40), (0, 0, 40, 40))
            else:
                screen.blit(maps.textures_floor,
                            (column*40, row*40), (0, 0, 40, 40))


def object_hit(player, walls, mobs_spawn, mobs):
    hits = pygame.sprite.spritecollide(player, walls, False)
    hits_spawn = pygame.sprite.spritecollide(player, mobs_spawn, False)
    mobs_hit = pygame.sprite.spritecollide(player, mobs, False)
    for i in mobs_hit:
        i.kill()
        player.hp -= i.atk
        if player.hp <= 0:
            player.kill()
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


def update_screen(ai_settings, screen, player, all_sprites, arrows, maps, walls, mobs, mobs_spawn, first_draw=1):
    screen.fill([255, 0, 0])
    # pygame.display.update()
    draw_lvl(walls, ai_settings, screen, maps, mobs_spawn, first_draw)
    walls.update()
    walls.draw(screen)
    all_sprites.update()
    all_sprites.draw(screen)
    mobs_spawn.update()
    mobs_spawn.draw(screen)
    for i in mobs_spawn:
        i.timer -= 10
        if i.timer == 0:
            i.timer = 1000

            spawn_mob(maps, ai_settings, screen, mobs, i.x-40, i.y)
    mobs.update()
    mobs.draw(screen)
    object_hit(player, walls, mobs_spawn, mobs)
    update_arrows(arrows, ai_settings)
    arrows.update()
    arrows.draw(screen)
    pygame.sprite.groupcollide(walls, arrows, False, True)
    damaged_mobs = pygame.sprite.groupcollide(mobs, arrows, False, True)
    for i in damaged_mobs:
        i.hp -= player.atk
        if i.hp <= 0:
            i.kill()
            player.score += i.cost
    draw_text(screen, str(player.side), 18, ai_settings.screen_width*0.90, 10)
    draw_text(screen, 'HP: '+str(player.hp), 18,
              ai_settings.screen_width*0.90, 40)
    draw_text(screen, 'SCORE: '+str(player.score),
              18, ai_settings.screen_width*0.90, 70)
    pygame.display.flip()
