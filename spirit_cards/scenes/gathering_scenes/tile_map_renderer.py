
import pygame
from spirit_cards.asset_map import AssetMap
from spirit_cards.core.context import Context
from spirit_cards.core.entity import Entity
from spirit_cards.core.entity_manager import EntityManager
from spirit_cards.pygame_extension.pygame_services import PygameServices
from spirit_cards.scenes.gathering_scenes.follow_camera import FollowCamera
from spirit_cards.scenes.gathering_scenes.gathering_services import GatheringServices
from spirit_cards.scenes.gathering_scenes.isometric_entity import IsometricEntity
from spirit_cards.scenes.gathering_scenes.isometric_tile_map import IsometricTileMap
from spirit_cards.services.asset_manager import AssetManager
from spirit_cards.services.global_services import GlobalServices
from spirit_cards.scenes.gathering_scenes.map_description import desc


class TileMapRenderer(Entity):

    _surface: pygame.Surface
    _entity_manager: EntityManager

    _tile_texture: pygame.surface.Surface
    _tile_map: IsometricTileMap

    def __init__(self, context: Context):
        self._surface = context.get_service(PygameServices.SCREEN_SURFACE)
        self._entity_manager = context.get_service(GatheringServices.ENTITY_MANAGER)
        asset_manager: AssetManager = context.get_service(GlobalServices.ASSET_MANAGER)
        
        self._tile_texture = asset_manager.get_image(AssetMap.TILE1)
        tile_size = pygame.Vector2(self._tile_texture.get_size())
        # TODO dynamic tilemap
        self.tile_array = [[]]
        for x, row in enumerate(desc):
            for y, tile in enumerate(row):
                tile_name = "TILE"+str(tile)
                asset = AssetMap.__getattribute__(AssetMap, tile_name)
                texture = asset_manager.get_image(asset)
                if len(self.tile_array) < x + 1:
                    self.tile_array.append([])
                if len(self.tile_array[x]) < y + 1:
                    self.tile_array[x].append(0)
                self.tile_array[x][y] = texture
        map_height = len(desc)
        map_width = len(desc[0])
        self._tile_map = IsometricTileMap((map_height,map_width), (tile_size.x, 100, tile_size.y))

        print("Prerendering Map")
        self._pre_draw_map(self.tile_array)
        print("Finished Prerendering")

    def update(self, delta: float) -> None:
        pass

    def render(self, delta: float) -> None:
        camera: FollowCamera = self._entity_manager.get_filtered(FollowCamera.TAG)[0]

        map_texture = self._tile_map.get_map_texture()
        map_offset = pygame.Vector2(map_texture.get_size()) / -2 + pygame.Vector2(camera.bounds.center)
        self._surface.blit(self._tile_map.get_map_texture(), map_offset)

        isometric_entities: list[IsometricEntity] = self._entity_manager.get_filtered(IsometricEntity.TAG)

        for entity in isometric_entities:
            draw_pos = self._tile_map.to_screen_space(entity.position) + map_offset
            self._surface.blit(entity.surface, draw_pos)

    def cleanup(self) -> None:
        pass

    def _pre_draw_map(self, tile_array: list[list[int]]) -> None:
        surface = self._tile_map.get_map_texture()

        tile_offset = self._tile_map.tile_size.xy / -2 # From center coordinate of tile to top left of tile for rendering.

        for x, row in enumerate(self._tile_map.tile_map):
            for z, item in enumerate(row):
                screen_pos = self._tile_map.to_screen_space(pygame.Vector3(x, item.position.y, z))
                surface.blit(self._tile_texture, screen_pos + tile_offset)