import pygame

class IsometricTile:

    map_position: pygame.Vector3
    texture: pygame.surface.Surface
    accessible: bool = True
    screen_position: pygame.Vector2

    def __init__(self, map_position: pygame.Vector3, texture: pygame.surface.Surface, accessible: bool = True) -> None:
        self.map_position = map_position
        self.texture = texture
        self.accessible = accessible
        self.screen_position = None

    def set_screen_position(self, position: pygame.Vector2):
        self.screen_position = position
    
    def circel_collider(self, point: pygame.Vector2):
        if point.distance_to(self.screen_position) < 50:
            return True
        else: return False