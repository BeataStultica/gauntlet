import sys
import pygame
from arrow import Arrow
from wall import Wall


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
    # for event in pygame.event.get():
    '''
    if (event.key == pygame.K_RIGHT and event.key == pygame.K_DOWN):
        player.moving_right = False
        player.moving_down = False

    elif (event.key == pygame.K_RIGHT and event.key == pygame.K_UP):
        player.moving_right = False
        player.moving_up = False
    elif (event.key == pygame.K_LEFT and event.key == pygame.K_DOWN):
        player.moving_left = False
        player.moving_down = False
    elif (event.key == pygame.K_LEFT and event.key == pygame.K_UP):
        player.moving_left = False
        player.moving_up = False
    '''
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


def update_screen(ai_settings, screen, player, all_sprites, arrows, maps, walls):
    for wall in walls:
        walls.remove(wall)
        wall.kill()
    for row in range(len(maps.tilemap1)):
        for column in range(len(maps.tilemap1[0])):

            if maps.tilemap1[row][column] == 1:
                newall = Wall(ai_settings, screen, maps, column, row)
                walls.add(newall)
            else:
                screen.blit(maps.textures_floor,
                            (column*20, row*20), (0, 0, 20, 20))
    # screen.fill(ai_settings.bg_color)
    walls.update()
    walls.draw(screen)
    all_sprites.update()
    all_sprites.draw(screen)
    update_arrows(arrows, ai_settings)
    arrows.update()
    arrows.draw(screen)
    draw_text(screen, str(player.side), 18, ai_settings.screen_width*0.8, 10)
    pygame.display.flip()
