import pygame
from spirit_cards.asset_map import AssetMap
from spirit_cards.core.context import ScopedContext
from spirit_cards.core.entity_manager import EntityManager
from spirit_cards.core.scene import Scene

from spirit_cards.pygame_extension.event_buffer import EventBuffer
from spirit_cards.pygame_extension.pygame_services import PygameServices
from spirit_cards.scenes.gathering_scenes.follow_camera import FollowCamera
from spirit_cards.scenes.gathering_scenes.gathering_player import GatheringPlayer
from spirit_cards.scenes.gathering_scenes.gathering_services import GatheringServices
from spirit_cards.scenes.gathering_scenes.isometric_entity import IsometricEntity
from spirit_cards.scenes.gathering_scenes.isometric_tile_map import IsometricTileMap
from spirit_cards.scenes.gathering_scenes.tile_map_renderer import TileMapRenderer
from spirit_cards.services.asset_manager import AssetManager
from spirit_cards.services.global_services import GlobalServices

class GatheringScene(Scene):

    _scoped_context: ScopedContext
    _event_buffer: EventBuffer
    _surface: pygame.Surface

    _entity_manager: EntityManager

    _font: pygame.font.Font

    def init(self, parameters: any = None) -> None:
        asset_manager: AssetManager = self.context.get_service(GlobalServices.ASSET_MANAGER)
        
        self._event_buffer = self.context.get_service(PygameServices.EVENT_BUFFER)
        self._surface = self.context.get_service(PygameServices.SCREEN_SURFACE)
        self._font = asset_manager.get_font(AssetMap.MONTSERRAT_24)

        self._entity_manager = EntityManager()
        self._scoped_context = ScopedContext(self.context, {
            GatheringServices.ENTITY_MANAGER: self._entity_manager
        })

        self._entity_manager.register(FollowCamera(self._scoped_context), [FollowCamera.TAG])
        self._entity_manager.register(TileMapRenderer(self._scoped_context))
        self._entity_manager.register(GatheringPlayer(self._scoped_context), [IsometricEntity.TAG])

    def process(self, delta: int) -> None:
    
        self._entity_manager.update(delta)
        self._entity_manager.render(delta)

        # FPS viewer
        text = self._font.render(str(int((1/delta)*60)), True, "Black")
        pygame.draw.rect(self._surface, "White", pygame.Rect(0,0,text.get_size()[0] + 8, text.get_size()[1] + 8))
        self._surface.blit(text, (4, 4))

    def cleanup(self) -> None:
        self._scoped_context.cleanup()
        self._entity_manager.cleanup()