import random
import pygame
from spirit_cards.asset_map import MONTSERRAT_24, TEST_TILE
from spirit_cards.core.scene import Scene

from spirit_cards.pygame_extension.event_buffer import EventBuffer
from spirit_cards.pygame_extension.pygame_services import PygameServices
from spirit_cards.scenes.gathering_scenes.isometric_tile_map import IsometricTileMap
from spirit_cards.services.asset_manager import AssetManager
from spirit_cards.services.global_services import GlobalServices

class SecondaryScene(Scene):

    _event_buffer: EventBuffer
    _surface: pygame.Surface
    _font: pygame.font.Font
    _texture: pygame.surface.Surface

    _tile_map: IsometricTileMap

    _offset: pygame.Vector2 = pygame.Vector2(0, 0)
    _thingy: pygame.Vector3 = pygame.Vector3(0, 1, 0)

    def init(self, parameters: any = None) -> None:
        asset_manager: AssetManager = self.context.get_service(GlobalServices.ASSET_MANAGER)
        self._event_buffer = self.context.get_service(PygameServices.EVENT_BUFFER)
        self._surface = self.context.get_service(PygameServices.SCREEN_SURFACE)
        self._texture = asset_manager.get_image(TEST_TILE)

        self._font = asset_manager.get_font(MONTSERRAT_24)

        tile_size = pygame.Vector2(self._texture.get_size())
        self._tile_map = IsometricTileMap((5,2), (tile_size.x, 190, tile_size.y))

        print("Prerendering Map")
        self._pre_draw_map()
        print("Finished Prerendering")

    def process(self, delta: int) -> None:

        speed = 10

        # Map + debug camera
        pressed_keys = pygame.key.get_pressed()
        if(pressed_keys[pygame.K_w]):
            self._offset.y += speed
        if(pressed_keys[pygame.K_s]):
            self._offset.y -= speed
        if(pressed_keys[pygame.K_a]):
            self._offset.x += speed
        if(pressed_keys[pygame.K_d]):
            self._offset.x -= speed

        center = pygame.Vector2(self._surface.get_size()) / 2
        
        map_texture = self._tile_map.get_map_texture()
        map_offset = pygame.Vector2(map_texture.get_size()) / -2 + center + self._offset
        self._surface.blit(self._tile_map.get_map_texture(), map_offset)

        text = self._font.render("Heyo", True, "White")
        self._surface.blit(text, (4, 4))
        pygame.draw.circle(self._surface, "Red", center, 10, 4)

        temp_movement = pygame.Vector3(0,0,0)

        # Pseudo player
        if(pressed_keys[pygame.K_UP]):
            temp_movement.z -= 1
        if(pressed_keys[pygame.K_DOWN]):
            temp_movement.z += 1
        if(pressed_keys[pygame.K_LEFT]):
            temp_movement.x -= 1
        if(pressed_keys[pygame.K_RIGHT]):
            temp_movement.x += 1

        if(temp_movement.length() != 0):
            self._thingy += temp_movement.rotate_y(45).normalize() * 0.1

        thingy_pos = self._tile_map.to_screen_space(self._thingy) + map_offset
        pygame.draw.circle(self._surface, "Cyan", thingy_pos, 24, 8)

    def _pre_draw_map(self) -> None:
        surface = self._tile_map.get_map_texture()

        tile_offset = self._tile_map.tile_size.xy / -2

        for x, row in enumerate(self._tile_map.tile_map):
            for z, item in enumerate(row):
                screen_pos = self._tile_map.to_screen_space(pygame.Vector3(x, item.position.y, z))
                surface.blit(self._texture, screen_pos + tile_offset)

    def cleanup(self) -> None:
        pass