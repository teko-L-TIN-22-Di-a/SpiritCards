import pygame
from spirit_cards.asset_map import AssetMap
from spirit_cards.card_engine.card_engine import CardEngine
from spirit_cards.card_engine.card_player import CardPlayer
from spirit_cards.core.context import ScopedContext

from spirit_cards.core.engine_services import *
from spirit_cards.core.entity_manager import EntityManager
from spirit_cards.core.scene import Scene
from spirit_cards.core.scene_switcher import SceneSwitcher
from spirit_cards.pygame_extension.gui.msg_box import MsgBox

from spirit_cards.pygame_extension.pygame_services import *
from spirit_cards.pygame_extension.event_buffer import EventBuffer

from spirit_cards.scenes.encounter_scenes.board_components.board import Board
from spirit_cards.scenes.encounter_scenes.encounter_services import EncounterServices
from spirit_cards.services.asset_manager import AssetManager
from spirit_cards.services.global_services import GlobalServices
from spirit_cards.pygame_extension.pygame_services import PygameServices
from spirit_cards.core.engine_services import EngineServices

class EncounterScene(Scene):

    _scoped_context: ScopedContext
    _surface: pygame.Surface
    _event_buffer: EventBuffer
    _scene_switcher: SceneSwitcher

    _entity_manager: EntityManager
    _card_engine: CardEngine
    _board: Board

    _font: pygame.font.Font

    def init(self, parameters: any = None) -> None:

        self._scene_switcher = self.context.get_service(EngineServices.SCENE_SWITCHER)
        self._surface = self.context.get_service(PygameServices.SCREEN_SURFACE)
        self._event_buffer = self.context.get_service(PygameServices.EVENT_BUFFER)
        asset_manager: AssetManager = self.context.get_service(GlobalServices.ASSET_MANAGER)

        self._font = asset_manager.get_font(AssetMap.MONTSERRAT_24)

        self._entity_manager = EntityManager()
        msgBox = MsgBox(self.context)
        self._scoped_context = ScopedContext(self.context, {
            EncounterServices.ENTITY_MANAGER: self._entity_manager,
            EncounterServices.MESSAGE_BOX: msgBox
        })

        player1 = CardPlayer()
        player2 = CardPlayer()
        
        self._card_engine = CardEngine(player1, player2)

        self._entity_manager.register(Board(self._scoped_context))
        self._entity_manager.register(CardEngine(player1, player2), [CardEngine.TAG])
        self._entity_manager.register(msgBox)

    def process(self, delta: float) -> None:

        self._surface.fill("#BABABF")

        self._entity_manager.update(delta)
        self._entity_manager.render(delta)

        # FPS viewer
        text = self._font.render(str(int((1/delta)*60)), True, "Black")
        pygame.draw.rect(self._surface, "White", pygame.Rect(0,0,text.get_size()[0] + 8, text.get_size()[1] + 8))
        self._surface.blit(text, (4, 4))

    def cleanup(self) -> None:
        self._scoped_context.cleanup()
        self._entity_manager.cleanup()
