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
                
