import random
import pygame
from spirit_cards.asset_map import MONTSERRAT_24, TEST_SPRITE_SHEET, TEST_TILE
from spirit_cards.pygame_extension.event_buffer import EventBuffer

from spirit_cards.pygame_extension.pygame_services import *
from spirit_cards.core.scene import Scene
from spirit_cards.services.asset_manager import AssetManager
from spirit_cards.services.global_services import ASSET_MANAGER

class Tile:
    y: int = 1

    def __init__(self, y):
        self.y = y

class SecondaryScene(Scene):

    _event_buffer: EventBuffer
    _surface: pygame.Surface
    _font: pygame.font.Font
    _texture: pygame.surface.Surface

    _tile_map: list[list[Tile]]
    _map_surface: pygame.Surface

    _offset = (0, 0)

    def init(self, parameters: any = None) -> None:
        asset_manager: AssetManager = self.context.get_service(ASSET_MANAGER)
        self._event_buffer = self.context.get_service(EVENT_BUFFER)
        self._surface = self.context.get_service(SCREEN_SURFACE)
        self._texture = asset_manager.get_image(TEST_TILE)

        self._font = asset_manager.get_font(MONTSERRAT_24)

        # self._tile_map = [[Tile(random.randrange(10, 15)/10) for z in range(0,5)] for x in range(0,5)]
        map_size = (5,5)
        self._tile_map = [[Tile(1) for z in range(0,map_size[1])] for x in range(0,map_size[0])]

        # Prerender map

        tile_size = self._texture.get_size()
        half_size = (
            tile_size[0]/2, 
            48 #tile_size[1]/4
        )

        map_surface_size = (
            map_size[0]*half_size[0] + map_size[1]*half_size[0], 
            max(map_size[0], map_size[1]) * half_size[1]*2 + tile_size[1] - half_size[1]
        )

        self._map_surface = pygame.surface.Surface((map_surface_size[0], map_surface_size[1]), pygame.SRCALPHA)
        start_offset = (map_surface_size[0]- map_size[1]*half_size[0]-half_size[0], 0)

        for x, row in enumerate(self._tile_map):
            for z, item in enumerate(row):

                x_part = (half_size[0]*x, half_size[1]*x)
                z_part = (half_size[0]*-z, half_size[1]*z)
                y_part = (0, half_size[1]*item.y)
                xyz_pos = (x_part[0] + z_part[0] + y_part[0], x_part[1] + z_part[1] + y_part[1])

                pos = (xyz_pos[0] + start_offset[0], xyz_pos[1] + start_offset[1])
                self._map_surface.blit(self._texture, pos)

    def process(self, delta: int) -> None:

        speed = 10

        pressed_keys = pygame.key.get_pressed()
        if(pressed_keys[pygame.K_w]):
            self._offset = (self._offset[0], self._offset[1]+speed)
        if(pressed_keys[pygame.K_s]):
            self._offset = (self._offset[0], self._offset[1]-speed)
        if(pressed_keys[pygame.K_a]):
            self._offset = (self._offset[0]+speed, self._offset[1])
        if(pressed_keys[pygame.K_d]):
            self._offset = (self._offset[0]-speed, self._offset[1])

        tile_size = self._texture.get_size()
        half_size = (tile_size[0]/2, tile_size[1]/4)

        self._surface.fill(pygame.Color(50,50,50))
        text = self._font.render("Heyo", True, "White")
        self._surface.blit(text, (4, 4))

        self._surface.blit(self._map_surface, self._offset)
        

    def cleanup(self) -> None:
        pass