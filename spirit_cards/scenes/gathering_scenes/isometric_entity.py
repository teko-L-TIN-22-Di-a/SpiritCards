import pygame

from spirit_cards.core.entity import Entity

class IsometricEntity(Entity):

    TAG = "drawable_isometric_entity"

    position: pygame.Vector3
    direction: bool
    bounds: pygame.Rect
    surface: pygame.Surface
    colliders: list[pygame.Rect]

    def __init__(self, position: pygame.Vector3, surface: pygame.Surface, direction: bool = True, bounds: pygame.Rect = None):
        self.position = position
        self.direction = direction
        self.bounds = bounds
        self.surface = surface
        self.offset = pygame.Vector2(surface.get_size())
        self.colliders = []

    def flip_surface(self):
        self.surface = pygame.transform.flip(self.surface, True, False)

    def set_bounds(self, bounds: pygame.Rect):
        self.bounds = bounds

    def set_colliders(self, colliders: list[pygame.Rect]):
        self.colliders = colliders