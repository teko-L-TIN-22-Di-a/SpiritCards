
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
from spirit_cards.scenes.gathering_scenes.map_description import desc


class TileMapRenderer(Entity):

    _surface: pygame.Surface
    _entity_manager: EntityManager

    _tile_texture: pygame.surface.Surface
    _tile_map: IsometricTileMap

    def __init__(self, context: Context):
        self._surface = context.get_service(PygameServices.SCREEN_SURFACE)
        self._entity_manager = context.get_service(GatheringServices.ENTITY_MANAGER)
        
        self._tile_map = IsometricTileMap(context, desc)

        print("Prerendering Map")
        self._pre_draw_map()
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
            entity.set_bounds(self._tile_map.bounds)
            entity.set_colliders(self._tile_map.colliders)
            draw_pos = self._tile_map.to_screen_space(entity.position) + map_offset + entity.offset
            pygame.draw.circle(self._surface, "red", draw_pos, 10)
            self._surface.blit(entity.surface, draw_pos)

    def cleanup(self) -> None:
        pass

    def _pre_draw_map(self) -> None:
        surface = self._tile_map.get_map_texture()
        tile_offset = self._tile_map.tile_size.xy / -2 # From center coordinate of tile to top left of tile for rendering.

        for x, row in enumerate(self._tile_map.tile_map):
            #row.reverse() # fit tile drawing order to map descripton
            for z, item in enumerate(row):
                screen_pos = self._tile_map.to_screen_space(pygame.Vector3(x, item.map_position.y, z))
                self._tile_map.tile_map[x][z].set_screen_position(screen_pos)
                surface.blit(self._tile_map.tile_map[x][z].texture, screen_pos + tile_offset)