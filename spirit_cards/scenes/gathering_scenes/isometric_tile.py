import pygame

class IsometricTile:

    map_position: pygame.Vector3
    texture: pygame.surface.Surface
    accessible: bool = True
    screen_position: pygame.Vector2
    non_accessible: list = [3,8,9,11,12]

    def __init__(self, map_position: pygame.Vector3, texture: pygame.surface.Surface, accessible: bool = True) -> None:
        self.map_position = map_position
        self.texture = texture
        self.accessible = accessible
        self.screen_position = None

    def set_screen_position(self, position: pygame.Vector2):
        self.screen_position = position