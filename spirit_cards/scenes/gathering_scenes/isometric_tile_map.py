
import random
import pygame

from dataclasses import dataclass

@dataclass
class Tile:
    position: pygame.Vector3
    accessible: bool = True

class IsometricTileMap:

    _surface_dirty: bool = False
    _surface: pygame.surface.Surface = None

    tile_size: pygame.Vector3
    tile_map: list[list[Tile]]
    map_size: pygame.Vector3

    # tile_size x, y and z is reserved for the full height
    def __init__(self, map_size_tuple: tuple[int, int] | pygame.Vector2, tile_size_tuple: tuple[int, int, int] | pygame.Vector3):
        self.map_size = pygame.Vector3(map_size_tuple[0], 1, map_size_tuple[1])
        self.tile_size = pygame.Vector3(tile_size_tuple)

        self.tile_map = [
            [
                Tile(pygame.Vector3(x, 1, z)) for z in range(0,int(self.map_size.z))
            ]
            for x in range(0,int(self.map_size.x))
        ]

    def get_map_texture(self) -> pygame.surface.Surface:
        if (self._surface is None or self._surface_dirty):
            self.regenerate_surface()

        return self._surface

    def regenerate_surface(self) -> None:
        
        x_width = self.map_size.x * (self.tile_size.x/2)
        z_width = self.map_size.z * (self.tile_size.x/2)

        map_surface_size = pygame.Vector2(
            x_width + z_width,
            max(self.map_size.x, self.map_size.z) * (self.tile_size.y / 2) + self.tile_size.z
        )

        # self._surface = pygame.surface.Surface((map_surface_size.x, map_surface_size.y), pygame.SRCALPHA)
        self._surface = pygame.surface.Surface((map_surface_size.x, map_surface_size.y))
        self._surface.fill("green")

    def to_screen_space(self, position: pygame.Vector3) -> pygame.Vector2:

        x_part = pygame.Vector2((self.tile_size.x / 2) * position.x, (self.tile_size.y / 2) * position.x)
        z_part = pygame.Vector2((-self.tile_size.x / 2) * position.z, (self.tile_size.y / 2) * position.z)
        y_part = pygame.Vector2(0, (self.tile_size.y / 2) * position.y)

        surface_offset = pygame.Vector2(self._surface.get_width() / 2, 0)
        leaning_offset = pygame.Vector2((self.map_size.z - self.map_size.x) * self.tile_size.x / 4, 0)

        return x_part + z_part + y_part + surface_offset + leaning_offset
    