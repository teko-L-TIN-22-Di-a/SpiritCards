import pygame
from spirit_cards.core.entity import Entity

class UIComponent:

    relative_to: any = None # should be another UIComponent or expose get_rect

    margin: pygame.Vector2 = pygame.Vector2(0,0)

    rect: pygame.Rect

    def __init__(self, rect, margin: pygame.Vector2 = None, relative_to = None):
        self.rect = rect
        self.relative_to = relative_to
        
        if(margin is not None):
            self.margin = margin

    def get_surface(self) -> pygame.Surface:
        pass

    def update(self) -> pygame.Surface:
        pass

    def get_pos(self) -> pygame.Vector2:
        pos = pygame.Vector2(self.rect.topleft)

        if(self.relative_to is not None):
            return self.relative_to.get_pos() + pos
        
        return pos
    
    def get_local_pos(self) -> pygame.Rect:
        return pygame.Vector2(self.rect.topleft)
    
    def get_inner_pos(self) -> pygame.Vector2:
        return self.get_pos() + self.margin

    def get_local_rect(self) -> pygame.Rect:
        return self.rect.copy()

    def get_rect(self) -> pygame.Rect:
        if(self.relative_to is not None):
            relative_pos = self.relative_to.get_pos()
            return self.rect.copy().move(relative_pos.x, relative_pos.y)
        
        return self.rect.copy()
    
    def get_inner_rect(self) -> pygame.Rect:
        rect = self.get_rect()
        return pygame.Rect(
            rect.left + self.margin.x,
            rect.top + self.margin.y,
            rect.width - self.margin.x*2,
            rect.height - self.margin.y*2)


