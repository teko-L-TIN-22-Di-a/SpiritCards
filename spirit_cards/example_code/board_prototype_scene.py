import pygame
from spirit_cards.asset_map import AssetMap
from spirit_cards.card_engine.card_engine import CardEngine
from spirit_cards.card_engine.card_player import CardPlayer
from spirit_cards.core.context import ScopedContext

from spirit_cards.core.engine_services import *
from spirit_cards.core.scene import Scene
from spirit_cards.core.scene_switcher import SceneSwitcher

from spirit_cards.pygame_extension.pygame_services import *
from spirit_cards.pygame_extension.event_buffer import EventBuffer

from spirit_cards.scenes.encounter_scenes.board_components.board import Board
from spirit_cards.services.asset_manager import AssetManager
from spirit_cards.services.global_services import GlobalServices
from spirit_cards.pygame_extension.pygame_services import PygameServices
from spirit_cards.core.engine_services import EngineServices

class BoardPrototypeScene(Scene):

    _scoped_context: ScopedContext
    _surface: pygame.Surface
    _event_buffer: EventBuffer
    _scene_switcher: SceneSwitcher

    _card_engine: CardEngine
    _board: Board

    _font: pygame.font.Font
    _card_texture: pygame.surface.Surface

    def init(self, parameters: any = None) -> None:

        self._scene_switcher = self.context.get_service(EngineServices.SCENE_SWITCHER)
        self._surface = self.context.get_service(PygameServices.SCREEN_SURFACE)
        self._event_buffer = self.context.get_service(PygameServices.EVENT_BUFFER)
        asset_manager: AssetManager = self.context.get_service(GlobalServices.ASSET_MANAGER)

        self._font = asset_manager.get_font(AssetMap.MONTSERRAT_24)

        self._card_texture = pygame.transform.smoothscale(asset_manager.get_image(AssetMap.TEST_CARD), (185, 256))

        self._scoped_context = ScopedContext(self.context, {
              
        })

        player1 = CardPlayer()
        player2 = CardPlayer()
        
        self._card_engine = CardEngine(player1, player2)

        self._board = Board(self._scoped_context)

    def process(self, delta: int) -> None:

        self._surface.fill("White")

        self._board.render(delta)

        text = self._font.render(str(delta), True, "Black")
        self._surface.blit(text, (4, 4))

        card_rect = pygame.Rect(24, 24, 185, 256)
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())

        if(card_rect.collidepoint(mouse_pos.x, mouse_pos.y)):
            pygame.draw.rect(self._surface, "green", card_rect)
            beeg_card = pygame.transform.scale_by(self._card_texture, 2)
            screen_center = pygame.Vector2(self._surface.get_rect().center)
            card_center = pygame.Vector2(beeg_card.get_rect().center)
            self._surface.blit(beeg_card,screen_center - card_center)

        self._surface.blit(self._card_texture, (24,24))

        # self._surface.blit(pygame.transform.rotate(self._card_texture, 180), (24,24))
        # self._surface.blit(self._card_texture, (24,24))

        return

        self._card_engine.update()

    def cleanup(self) -> None:
        self._scoped_context.cleanup()
