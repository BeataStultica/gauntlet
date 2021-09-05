import sys
import pygame


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


def check_keydown_events(event, ai_settings, screen, player):
    # for event in pygame.event.get():

    if event.key == pygame.K_RIGHT:
        player.moving_right = True
        if player.moving_up == True:
            player.image = change_sprite('topright')
            player.side = 'topRight'
        elif player.moving_down == True:
            player.image = change_sprite('bottomright')
            player.side = 'bottomRight'
        else:
            player.image = change_sprite('right')
            player.side = 'Right'
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
            player.side = 'Left'
    elif event.key == pygame.K_UP:
        player.moving_up = True
        if player.moving_right == True:
            player.image = change_sprite('topright')
            player.side = 'topRight'
        elif player.moving_left == True:
            player.image = change_sprite('topleft')
            player.side = 'topleft'
        else:
            player.image = change_sprite('up')
            player.side = 'Top'
    elif event.key == pygame.K_DOWN:
        player.moving_down = True
        if player.moving_right == True:
            player.image = change_sprite('bottomright')
            player.side = 'bottomRight'
        elif player.moving_left == True:
            player.image = change_sprite('bottomleft')
            player.side = 'bottomleft'
        else:
            player.image = change_sprite('down')
            player.side = 'Down'


def keyup(event, player):
    # for event in pygame.event.get():
    if event.key == pygame.K_RIGHT:
        player.moving_right = False
    elif event.key == pygame.K_LEFT:
        player.moving_left = False
    elif event.key == pygame.K_UP:
        player.moving_up = False
    elif event.key == pygame.K_DOWN:
        player.moving_down = False
    elif event.key == pygame.K_q:
        sys.exit()


def check_event(ai_settings, screen, player):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, player)
        elif event.type == pygame.KEYUP:
            keyup(event, player)


def draw_text(surf, text, size, x, y):
    font_name = pygame.font.match_font('arial')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def update_screen(ai_settings, screen, player, all_sprites):
    screen.fill(ai_settings.bg_color)
    all_sprites.update()
    all_sprites.draw(screen)
    draw_text(screen, str(player.side), 18, ai_settings.screen_width*0.8, 10)
    pygame.display.flip()
