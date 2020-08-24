"""
Issac Gann (gannmann) 2020

message module handles outputting strings to the screen.
"""

import pygame

import assets

class Message(object):
    def __init__(self, surface, lines, font):
        self.surface = surface
        self.lines = lines
        self.font = font
        self.num_lines = 0
        self.log = []

    def out(self, text, fgcolor=(255, 255, 255), bgcolor = None):
        self.surface.fill((0, 0, 0))
        
        if len(self.log) < self.lines:
            self.log.append(text) # add to end
        
        else:
            self.log.pop(0) # remove from top
            self.log.append(text)
        
        self.num_lines = 0.5
        for t in self.log:
            text_surface = self.font.render(t, True, fgcolor, bgcolor)
            self.surface.blit(text_surface, (self.font.get_height(), self.font.get_height()*self.num_lines))
            self.num_lines += 1

class TextList(object):
    def __init__(self, surface, item_list, font):
        self.surface = surface
        self.list = item_list
        self.font = font

    def out(self, fgcolor=(255, 255, 255), bgcolor = None):
        self.surface.fill((0, 0, 0))
        
        for t in self.list:
            if type(t) == tuple:
                text_surface = self.font.render(t[0], True, t[1], bgcolor)
                self.surface.blit(text_surface, (self.font.get_height(), self.font.get_height()*self.list.index(t)+1))
            else:
                if t.selected:
                    text_surface = self.font.render(t.name, True, (0, 0, 0), (255, 255, 0))
                    self.surface.blit(text_surface, (self.font.get_height(), self.font.get_height()*self.list.index(t)+1))
                else:
                    text_surface = self.font.render(t.name, True, fgcolor, bgcolor)
                    self.surface.blit(text_surface, (self.font.get_height(), self.font.get_height()*self.list.index(t)+1))
                
class Bar(object): # for displaying x out of max x information e.g. health bars, hunger bars, exp bars
    def __init__(self, name, current_value, max_value, width=128, height=16, fg_color=(255, 0, 0), bg_color=(16, 16, 16), font_color=(255, 255, 255), font=assets.tiny_font):
        self.name = name
        self.current_value = current_value
        self.max_value = max_value
        self.width = width
        self.height = height
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.font_color = font_color
        self.font = font

        self.render_text = self.name + ': ' + str(self.current_value) + '/' + str(self.max_value)

        self.surface = pygame.Surface((self.width, self.height))
        self.current_rect = pygame.Rect(0, 0, ((self.width * self.current_value)//self.max_value), self.height)
        self.max_rect = pygame.Rect(0, 0, self.width, self.height)

       
    def update(self, current_value, x, y, surface):
        self.current_value = current_value
        self.render_text = self.name + ': ' + str(self.current_value) + '/' + str(self.max_value)

        self.surface.fill(self.bg_color)

        self.current_rect = pygame.Rect(0, 0, ((self.width * self.current_value)//self.max_value), self.height)

        pygame.draw.rect(self.surface, self.bg_color, self.max_rect)
        pygame.draw.rect(self.surface, self.fg_color, self.current_rect)

        label_surface = self.font.render(self.render_text, True, self.font_color)
        self.surface.blit(label_surface, (0,0))

        surface.blit(self.surface, (x, y))
        # current width (x)     current_value
        # ----------------- =  ---------------
        # max width (64)        max_value

        # current_width * max_value = max_width * current_value
        # current_with = (max_width * current_value) / max_value