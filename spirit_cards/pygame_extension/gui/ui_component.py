import pygame
from spirit_cards.core.entity import Entity

class UIComponent:

    relative_to: any = None # should be another UIComponent or expose get_rect

    margin: pygame.Vector2 = pygame.Vector2(0,0)

    _rect: pygame.Rect

    def __init__(self, rect, margin: pygame.Vector2 = None, relative_to = None):
        self.rect = rect
        self.relative_to = relative_to
        
        if(margin is not None):
            self.margin = margin

    def get_pos(self) -> pygame.Vector2:
        pos = pygame.Vector2(self.rect.topright)

        if(self.relative_to is not None):
            return self.relative_to.get_pos() + pos
        
        return pos
    
    def get_inner_pos(self) -> pygame.Vector2:
        return self.get_pos() + self.margin

    def get_rect(self) -> pygame.Rect:
        if(self.relative_to is not None):
            relative_pos = self.relative_to.get_pos()
            return self.rect.copy().move(relative_pos.x, relative_pos.y)
        
        return self.rect.copy()

