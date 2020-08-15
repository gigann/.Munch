import gc
import pygame

#import tcod
#import pygame_gui

import menus

def main():
    gc.enable()

    # CONFIG
    window_width = 800
    window_height = 600
    #fullscreen = False
    framerate = 60

    # INTIALIZE
    pygame.init()
    pygame.display.set_caption('Hominidae') #pygame.display.set_caption('APESHIT')
    master_window = pygame.display.set_mode((window_width, window_height),
    flags=pygame.HWSURFACE | pygame.ASYNCBLIT)

    pygame.key.set_repeat(250, 50) # set repeating keys
    #clock = pygame.time.Clock()

    game_state = 'main menu'

    # MAIN LOOP
    running = True # master loop
    while running:
        #dT = clock.tick(framerate)/100550.0 # fps

        # GAME STATE
        if game_state == 'main menu':
             #print('main menu state')
            running, game_state = menus.main_menu(
                window_width, window_height, framerate, master_window)

        elif game_state == 'game':
             #print('game state')
            running, game_state = menus.game_menu(
                window_width, window_height, framerate, master_window)

        else:  #print('error state')
            pass



if __name__ == '__main__':
    main()
