
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


class TileMapRenderer(Entity):

    _surface: pygame.Surface
    _entity_manager: EntityManager

    _tile_texture: pygame.surface.Surface
    _tile_map: IsometricTileMap

    def __init__(self, context: Context):
        self._surface = context.get_service(PygameServices.SCREEN_SURFACE)
        self._entity_manager = context.get_service(GatheringServices.ENTITY_MANAGER)
        asset_manager: AssetManager = context.get_service(GlobalServices.ASSET_MANAGER)
        
        self._tile_texture = asset_manager.get_image(AssetMap.TEST_TILE)
        tile_size = pygame.Vector2(self._tile_texture.get_size())
        self._tile_map = IsometricTileMap((5,2), (tile_size.x, 190, tile_size.y))

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
            draw_pos = self._tile_map.to_screen_space(entity.position) + map_offset
            # TODO tidy up asset
            playersprite = pygame.image.load("assets/test_playersprite2.png")
            playersprite = pygame.transform.scale(playersprite,(82,96))
            self._surface.blit(playersprite, draw_pos)
            # pygame.draw.circle(self._surface, "Cyan", draw_pos, 24, 8)

    def cleanup(self) -> None:
        pass

    def _pre_draw_map(self) -> None:
        surface = self._tile_map.get_map_texture()

        tile_offset = self._tile_map.tile_size.xy / -2 # From center coordinate of tile to top left of tile for rendering.

        for x, row in enumerate(self._tile_map.tile_map):
            for z, item in enumerate(row):
                screen_pos = self._tile_map.to_screen_space(pygame.Vector3(x, item.position.y, z))
                surface.blit(self._tile_texture, screen_pos + tile_offset)