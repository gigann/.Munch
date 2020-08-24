"""
Issac Gann (gannmann) 2020

menus module handles game states between menus e.g. main menu and game menu
"""
import itertools
import time

import pygame_gui
import pygame

import dungeon
import assets
import entity
import message

pygame.init()

def main_menu(window_width, window_height, framerate, surface):
    """handles all logic concerning the main menu state of the game

    Args:
        window_width ([integer]): [width of the window in pixels]
        window_height ([integer]): [height of the window in pixels]
        framerate ([integer]): [framerate to lock the game at]
        surface ([pygame.Surface]): [A pygame surface that can be blitted to]

    Returns:
        [type]: [description]
    """
    game_state = 'main menu'

    surface.fill((0, 0, 0))

    gui = pygame_gui.UIManager((window_width, window_height), 'fonts/theme.json')

    clock = pygame.time.Clock()

    # gui elements
    button_size = (200, 50)

    load_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(((
            -(button_size[0]//2) + window_width//2), window_height//2),
                                  button_size),
        text='Load Save', manager=gui)
    new_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(((
            -(button_size[0]//2) + window_width//2), button_size[1] + window_height//2),
                                  button_size),
        text='New Game', manager=gui)

    settings_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(((
            -(button_size[0]//2) + window_width//2), 2*button_size[1] + window_height//2),
                                  button_size),
        text='Settings', manager=gui)
    morgue_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(((
            -(button_size[0]//2) + window_width//2), 3*button_size[1] + window_height//2),
                                  button_size),
        text='Morgue', manager=gui)
    quit_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(((
            -(button_size[0]//2) + window_width//2), 4*button_size[1] + window_height//2),
                                  button_size),
        text='Quit', manager=gui)

    running = True
    while running:
        # #print('FPS: ' + str(round(clock.get_fps(), 0)) + ', running: ' + str(running) + ', state: ' + str(game_state))
        dT = clock.tick(framerate)/1000.0 # fps

        # menu events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == new_button:
                        game_state = 'game'
                        return (running, game_state)
                    if event.ui_element == load_button:
                        pass #load_game()
                    if event.ui_element == settings_button:
                        pass #open_settings()
                    if event.ui_element == morgue_button:
                        pass #open_morgue()
                    if event.ui_element == quit_button:
                        running = False
            gui.process_events(event) # gui events
        # menu render
        gui.update(dT)
        gui.draw_ui(surface)
        pygame.display.update()

    return (running, game_state)

def game_menu(window_width, window_height, framerate, surface):
    game_state = 'game'

    player_action = False

    surface.fill((0, 0, 0))

    clock = pygame.time.Clock()

    num_turns = 0

    '''
    # gui elements, console, etc
    gui = pygame_gui.UIManager((window_width, window_height), 'fonts/theme.json')

    console_rect = pygame.Rect(0, 0, window_width//2, window_height//4)
    console_text_rect = console_rect.copy()
    console_text_rect.width = console_text_rect.width - 30
    console_text_rect.height = console_text_rect.height - 60

    console_ui_window = pygame_gui.elements.UIWindow(rect=console_rect,
    manager=gui, window_display_title='Log', object_id='console_window',
    resizable=False, visible=True)
    console_ui_window.blendmode = 1
    console_ui_window.enable_close_button = False
    console_ui_window.rebuild()

    console_text = 'Can you find Big Mike?<br>Type ? for help.'
    console_text_box = pygame_gui.elements.UITextBox(
        html_text=console_text, relative_rect=console_text_rect, manager=gui,
        wrap_to_height=False, layer_starting_height=1, container=console_ui_window,
        parent_element=None, object_id='console_text_box', visible=1)
    console_text_box.blendmode = 1

    '''

    #console.out('Welcome to Hominidae!')
    #console.out('The legendary Big Mike awaits you!')
    #console.out('Press ? for help!')

    # dungeon stuff
    new_dungeon = dungeon.Dungeon()

    #tile_surface = pygame.Surface((window_width, window_height))

    console_surface = pygame.Surface((window_width//2, window_height//5))
    console = message.Message(console_surface, 5, assets.tiny_font)

    player_info_surface = pygame.Surface((window_width//5, window_height//2))
    player_info = new_dungeon.player.get_info()
    player_info_text = message.TextList(player_info_surface, player_info, assets.body_font)

    player_inv_surface = pygame.Surface((window_width//5, window_height//2))
    player_inv_text = message.TextList(player_inv_surface, new_dungeon.player.inv, assets.tiny_font)

    game_surface = pygame.Surface((window_width - window_width//5 , window_height - window_height//5))
    game_surface.fill(assets.game_background)
    
    map_surface = pygame.Surface((window_width//3, window_height//5))
    blip_player = False
    blip_player = new_dungeon.render_minimap(map_surface, blip_player)

    #blits
    player_info_text.out()

    new_dungeon.render_proper(game_surface)
    surface.blit(game_surface, (0, 0))
    surface.blit(map_surface, (window_width//2, window_height - window_height//5))
    surface.blit(player_info_surface, (window_width - window_width//5, 16))
    surface.blit(player_inv_surface, (window_width - window_width//5, window_height//2))
    surface.blit(console_surface, (0, window_height - window_height//5))
    # menu render
    #console_text_box.set_active_effect('typing_appear')
    '''
    gui.update(0.0001)
    gui.draw_ui(surface)
    '''
    pygame.display.update()

    #'''
    # accurate FPS
    frame_time = []
    start_time = time.time()

    running = True
    while running:
        player_action = False

        # #print('FPS: ' + str(round(clock.get_fps(), 0)) + ', running: ' + str(running) + ', state: ' + str(game_state))        
        #dT = clock.tick(framerate)/1000.0 # fps    
        dT = clock.tick()/1000.0 # TESTING MAX FRAMERATE

        # #print('dT : ' + str(dT))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state = 'main menu'
                return(running, game_state)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    new_dungeon.player.current_hp += 100

                if event.key == pygame.K_KP2:
                    player_action = new_dungeon.player.move(new_dungeon, 1, 1, console)
                if event.key == pygame.K_KP4:
                    player_action = new_dungeon.player.move(new_dungeon, -1, 1, console)
                if event.key == pygame.K_KP6:
                    player_action = new_dungeon.player.move(new_dungeon, 1, -1, console)
                if event.key == pygame.K_KP8:
                    player_action = new_dungeon.player.move(new_dungeon, -1, -1, console)
                if event.key == pygame.K_KP1:
                    player_action = new_dungeon.player.move(new_dungeon, 0, 1, console)
                if event.key == pygame.K_KP3:
                    player_action = new_dungeon.player.move(new_dungeon, 1, 0, console)
                if event.key == pygame.K_KP7:
                    player_action = new_dungeon.player.move(new_dungeon, -1, 0, console)
                if event.key == pygame.K_KP9:
                    player_action = new_dungeon.player.move(new_dungeon, 0, -1, console)

                if event.key == pygame.K_PERIOD or event.key == pygame.K_KP5:
                    console.out('waited')
                    player_action = True

                if event.key == pygame.K_c: # toggle door
                    player_action = new_dungeon.toggle_door(console)

                if event.key == pygame.K_COMMA and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    player_action = new_dungeon.use_stairs('up', console)

                if event.key == pygame.K_PERIOD and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    player_action = new_dungeon.use_stairs('down', console)

                if event.key == pygame.K_g or event.key == pygame.K_COMMA: # pick up item
                    player_action = new_dungeon.player.pickup(new_dungeon, console)

                if event.key == pygame.K_d: # drop item
                    player_action = new_dungeon.player.drop(new_dungeon, console)
  
                if event.key == pygame.K_w: # wield item
                    player_action = new_dungeon.player.wield(new_dungeon, console)

                if event.key == pygame.K_s: # sheathe item
                    player_action = new_dungeon.player.sheathe(new_dungeon, console)

                if event.key == pygame.K_f: # fling item
                    target = target_menu(new_dungeon, player_inv_text, player_inv_surface,
                                player_info_surface, player_info_text, game_surface,
                                blip_player, map_surface, window_width, window_height,
                                console, console_surface, surface)
                    if target != None:
                        player_action = new_dungeon.player.fling(new_dungeon, target, console)
                    else:
                        player_action = False
                if event.key == pygame.K_UP: # select an item above the currently selected item
                    new_dungeon.player.select('up', player_inv_text, player_inv_surface, surface, window_width, window_height)

                if event.key == pygame.K_DOWN: # select an item below the currently selected item
                    new_dungeon.player.select('down', player_inv_text, player_inv_surface, surface, window_width, window_height)

            if event.type == pygame.USEREVENT: # gui events
                pass
            
            # menu render
            '''
            gui.process_events(event)
            '''

        if player_action:
            new_dungeon.player.process_conditions(new_dungeon, console)

            num_turns += 1

            '''MONSTER TURN'''
            for creature in new_dungeon.current_level.creature_list:
                creature.run_ai(new_dungeon, new_dungeon.find_fov(), console)
                creature.process_conditions(new_dungeon, console)

            '''
            console_text_box.kill()
            console_text = (new_dungeon.player.name + ' ' + player_action + '<br>' + console_text)
            console_text_box = pygame_gui.elements.UITextBox(
                html_text=console_text, relative_rect=console_text_rect, manager=gui,
                wrap_to_height=False, layer_starting_height=1, container=console_ui_window,
                parent_element=None, object_id='console_text_box', visible=1)
            console_text_box.blendmode = 1

            #'''

            # inv list
            player_info = new_dungeon.player.get_info()
            player_info_text = message.TextList(player_info_surface, player_info, assets.body_font)
            player_info_text.out()

            player_inv_text.out()
            
            game_surface.fill(assets.game_background)
            new_dungeon.render_proper(game_surface)
            blip_player = new_dungeon.render_minimap(map_surface, blip_player)
            surface.blit(game_surface, (0, 0))
            surface.blit(map_surface, (window_width//2, window_height - window_height//5))
            surface.blit(player_info_surface, (window_width - window_width//5, 16))
            surface.blit(player_inv_surface, (window_width - window_width//5, window_height//2))
            surface.blit(console_surface, (0, window_height - window_height//5))
            pygame.display.update()
            #'''
        #'''
        '''
        surface.blit(game_surface, (0, 0))# (16, 16))
        gui.update(dT)
        gui.draw_ui(surface)    
        pygame.display.update()
        #'''
        # new render strategy
        # 1. render tile surface ONCE
        # 2. if player does something
        #   3. move tile surface offset from player
        #   4. update entity renders offset from player
        #   5. update FOV
        # 6. always render GUI or only update during player idk yet

        end_time = time.time()
        time_taken = end_time - start_time
        start_time = end_time
        frame_time.append(time_taken)
        frame_time = frame_time[-20:]
        if sum(frame_time) != 0:
            fps = len(frame_time) / sum(frame_time)
            print(fps)

'''
def item_menu(player, surface, action, window_width, window_height): # shows a menu for selecting items to equip/throw/drop etc...
    menu_open = True

    item_menu_surface = pygame.Surface((window_width//5, window_height//2))
    action_list = []
    item_menu_text = message.TextList(item_menu_surface, action_list, assets.body_font)

    for i in player.inv:
        
        if action in i.action_set:
        
            action_list.append(i)

    while menu_open:
        for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP: # select an item above the currently selected item
                        player.select('up')
                    if event.key == pygame.K_DOWN: # select an item below the currently selected item
                        player.select('down')
                    if event.key == pygame.K_KP_ENTER: # use item
                        return 'action'
                    if event.key == pygame.K_ESCAPE:
                        return 'no action'

        
        item_menu_text.out()
        surface.blit(item_menu_surface, (0, 0))
        pygame.display.update()
        



    return 'no action'
'''

def auto_target_menu(): # cycles through available targets
    pass

# returns a selected tile in x, y tuple
def target_menu(new_dungeon, player_inv_text, player_inv_surface,
                player_info_surface, player_info_text,
                game_surface, blip_player, map_surface, window_width, window_height,
                console, console_surface, surface): # either directional or a specific tile

    clock = pygame.time.Clock()

    console.out('Select a target with movement keys. Enter to confirm or ESC to cancel...')

    player_info = new_dungeon.player.get_info()
    player_info_text = message.TextList(player_info_surface, player_info, assets.body_font)
    player_info_text.out()
    player_inv_text.out()
    game_surface.fill(assets.game_background)
    new_dungeon.render_proper(game_surface)
    blip_player = new_dungeon.render_minimap(map_surface, blip_player)
    surface.blit(game_surface, (0, 0))
    surface.blit(map_surface, (window_width//2, window_height - window_height//5))
    surface.blit(player_info_surface, (window_width - window_width//5, 16))
    surface.blit(player_inv_surface, (window_width - window_width//5, window_height//2))
    surface.blit(console_surface, (0, window_height - window_height//5))
    pygame.display.update()

    #'''
    # accurate FPS
    frame_time = []
    start_time = time.time()

    select_x = new_dungeon.player.x
    select_y = new_dungeon.player.y



    fov = new_dungeon.find_fov()

    running = True
    while running:
        moved_selector = False

        old_x = select_x
        old_y = select_y

        # #print('FPS: ' + str(round(clock.get_fps(), 0)) + ', running: ' + str(running) + ', state: ' + str(game_state))        
        #dT = clock.tick(framerate)/1000.0 # fps    
        dT = clock.tick()/1000.0 # TESTING MAX FRAMERATE

        # #print('dT : ' + str(dT))
        
        # only select if floor and in line of sight
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP2:
                    if fov[select_x + 1][select_y + 1] and not new_dungeon.current_level.cells[select_x + 1][select_y + 1].solid:
                        select_x += 1
                        select_y += 1
                        moved_selector = True
                if event.key == pygame.K_KP4:
                    if fov[select_x - 1][select_y + 1] and not new_dungeon.current_level.cells[select_x - 1][select_y + 1].solid:
                        select_x -= 1
                        select_y += 1
                        moved_selector = True
                if event.key == pygame.K_KP6:
                    if fov[select_x + 1][select_y - 1] and not new_dungeon.current_level.cells[select_x + 1][select_y - 1].solid:
                        select_x += 1
                        select_y -= 1
                        moved_selector = True
                if event.key == pygame.K_KP8:
                    if fov[select_x - 1][select_y - 1] and not new_dungeon.current_level.cells[select_x - 1][select_y - 1].solid:
                        select_x -= 1
                        select_y -= 1
                        moved_selector = True
                if event.key == pygame.K_KP1:
                    if fov[select_x][select_y + 1] and not new_dungeon.current_level.cells[select_x][select_y + 1].solid:
                        select_y += 1
                        moved_selector = True
                if event.key == pygame.K_KP3:
                    if fov[select_x + 1][select_y] and not new_dungeon.current_level.cells[select_x + 1][select_y].solid:
                        select_x += 1
                        moved_selector = True
                if event.key == pygame.K_KP7:
                    if fov[select_x - 1][select_y] and not new_dungeon.current_level.cells[select_x - 1][select_y].solid:
                        select_x -= 1
                        moved_selector = True
                if event.key == pygame.K_KP9:
                    if fov[select_x][select_y - 1] and not new_dungeon.current_level.cells[select_x][select_y - 1].solid:
                        select_y -= 1
                        moved_selector = True

                if event.key == pygame.K_ESCAPE: # cancel targeting
                    new_dungeon.current_level.cells[select_x][select_y].selected = False
                    
                    player_info = new_dungeon.player.get_info()
                    player_info_text = message.TextList(player_info_surface, player_info, assets.body_font)
                    player_info_text.out()
                    player_inv_text.out()
                    game_surface.fill(assets.game_background)
                    new_dungeon.render_proper(game_surface)
                    blip_player = new_dungeon.render_minimap(map_surface, blip_player)
                    surface.blit(game_surface, (0, 0))
                    surface.blit(map_surface, (window_width//2, window_height - window_height//5))
                    surface.blit(player_info_surface, (window_width - window_width//5, 16))
                    surface.blit(player_inv_surface, (window_width - window_width//5, window_height//2))
                    surface.blit(console_surface, (0, window_height - window_height//5))
                    pygame.display.update()

                    return None

                if event.key == pygame.K_KP_ENTER: # continue with action
                    new_dungeon.current_level.cells[select_x][select_y].selected = False
                    
                    player_info = new_dungeon.player.get_info()
                    player_info_text = message.TextList(player_info_surface, player_info, assets.body_font)
                    player_info_text.out()
                    player_inv_text.out()
                    game_surface.fill(assets.game_background)
                    new_dungeon.render_proper(game_surface)
                    blip_player = new_dungeon.render_minimap(map_surface, blip_player)
                    surface.blit(game_surface, (0, 0))
                    surface.blit(map_surface, (window_width//2, window_height - window_height//5))
                    surface.blit(player_info_surface, (window_width - window_width//5, 16))
                    surface.blit(player_inv_surface, (window_width - window_width//5, window_height//2))
                    surface.blit(console_surface, (0, window_height - window_height//5))
                    pygame.display.update()

                    return (select_x, select_y)

            if moved_selector:
                new_dungeon.current_level.cells[old_x][old_y].selected = False

                new_dungeon.current_level.cells[select_x][select_y].selected = True

                # inv list
                player_info = new_dungeon.player.get_info()
                player_info_text = message.TextList(player_info_surface, player_info, assets.body_font)
                player_info_text.out()

                player_inv_text.out()
                
                game_surface.fill(assets.game_background)
                new_dungeon.render_proper(game_surface)
                blip_player = new_dungeon.render_minimap(map_surface, blip_player)
                surface.blit(game_surface, (0, 0))
                surface.blit(map_surface, (window_width//2, window_height - window_height//5))
                surface.blit(player_info_surface, (window_width - window_width//5, 16))
                surface.blit(player_inv_surface, (window_width - window_width//5, window_height//2))
                surface.blit(console_surface, (0, window_height - window_height//5))
                pygame.display.update()


        end_time = time.time()
        time_taken = end_time - start_time
        start_time = end_time
        frame_time.append(time_taken)
        frame_time = frame_time[-20:]
        if sum(frame_time) != 0:
            fps = len(frame_time) / sum(frame_time)
            #print(fps)

def options_menu():
    # add options for the following:
    # tileset vs ascii
    # sound and music
    # framerate
    # fullscreen
    # aspect ratio
    # language
    # light/dark mode

    pass




def character_menu():
    pass