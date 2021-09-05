import sys
import pygame


def check_keydown_events(event, ai_settings, screen, player):
    # for event in pygame.event.get():
    if event.key == pygame.K_RIGHT:
        player.moving_right = True
    elif event.key == pygame.K_LEFT:
        player.moving_left = True
    elif event.key == pygame.K_UP:
        player.moving_up = True
    elif event.key == pygame.K_DOWN:
        player.moving_down = True


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
