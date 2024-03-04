import pygame
from spirit_cards.asset_map import AssetMap
from spirit_cards.card_engine.card_engine import CardEngine
from spirit_cards.card_engine.card_player import PlayerState
from spirit_cards.core.context import Context
from spirit_cards.core.entity import Entity
from spirit_cards.pygame_extension.pygame_services import PygameServices
from spirit_cards.scenes.encounter_scenes.board_components.board_renderer import BoardRenderer
from spirit_cards.scenes.encounter_scenes.encounter_services import EncounterServices
from spirit_cards.services.asset_manager import AssetManager
from spirit_cards.services.global_services import GlobalServices


class DebugBoardRenderer(Entity):

    _card_engine: CardEngine
    _surface: pygame.Surface

    _player1_board: BoardRenderer
    _player2_board: BoardRenderer

    _font: pygame.font.Font

    def __init__(self, context: Context):
        self._card_engine: CardEngine = context.get_service(EncounterServices.CARD_ENGINE)
        self._surface = context.get_service(PygameServices.SCREEN_SURFACE)
        asset_manager: AssetManager = context.get_service(GlobalServices.ASSET_MANAGER)

        self._player1_board = BoardRenderer(self._card_engine.board_context.player1, context)
        self._player2_board = BoardRenderer(self._card_engine.board_context.player2, context)

        self._font = asset_manager.get_font(AssetMap.MONTSERRAT_24)

    def update(self, delta: float) -> None:
        
        self._player1_board.update(delta)
        self._player2_board.update(delta)

    def render(self, delta: float) -> None:
        
        text = None

        if(self._player2_board.following_player.state == PlayerState.WAIT_FOR_INPUT):
            self._player2_board.render(delta)
            text = self._font.render("Viewing Player 2", True, "Black")
        else:
            self._player1_board.render(delta)
            text = self._font.render("Viewing Player 1", True, "Black")

        pygame.draw.rect(self._surface, "White", pygame.Rect(0,32,text.get_size()[0] + 16, text.get_size()[1] + 8))
        self._surface.blit(text, (8, 36))


        