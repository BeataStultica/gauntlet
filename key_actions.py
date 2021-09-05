import sys
import pygame


def change_sprite(side):
    coords = {'left': (450, 25, 48, 48), 'right': (
        450, 75, 48, 48), 'up': (450, 50, 48, 48), 'down': (475, 0, 48, 48)}
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
    sheet = pygame.image.load('assets/elf.png').convert()

    if event.key == pygame.K_RIGHT:
        player.moving_right = True
        player.image = change_sprite('right')
    elif event.key == pygame.K_LEFT:
        player.moving_left = True
        player.image = change_sprite('left')
    elif event.key == pygame.K_UP:
        player.moving_up = True
        player.image = change_sprite('up')
    elif event.key == pygame.K_DOWN:
        player.moving_down = True
        player.image = change_sprite('down')


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


def update_screen(ai_settings, screen, player, all_sprites):
    screen.fill(ai_settings.bg_color)
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip()
