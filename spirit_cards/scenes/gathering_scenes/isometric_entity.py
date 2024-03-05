import pygame

from spirit_cards.core.entity import Entity

class IsometricEntity(Entity):

    TAG = "drawable_isometric_entity"

    position: pygame.Vector3
    direction: bool
    bounds: pygame.Rect
    surface: pygame.Surface

    def __init__(self, position: pygame.Vector3, direction: bool = True, bounds: pygame.Rect = None, surface: pygame.Surface = None):
        self.position = position
        self.direction = direction
        self.bounds = bounds
        self.surface = surface

    def flip_surface(self):
        self.surface = pygame.transform.flip(self.surface,True,False)