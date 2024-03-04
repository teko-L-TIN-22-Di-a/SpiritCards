import pygame
from dataclasses import dataclass
from spirit_cards.card_engine.card_engine import CardEngine
from spirit_cards.card_engine.card_player import CardPlayer

from spirit_cards.core.context import Context
from spirit_cards.core.entity import Entity
from spirit_cards.pygame_extension.pygame_services import PygameServices
from spirit_cards.scenes.encounter_scenes.board_components.board_side import BoardSide
from spirit_cards.scenes.encounter_scenes.encounter_services import EncounterServices

class BoardRenderer(Entity):

    BOARD_SPACE_BETWEEN = 32

    _context: Context
    _surface: pygame.surface.Surface
    _card_engine: CardEngine

    following_player: CardPlayer

    player1_side: BoardSide # Always also the following_player
    player2_side: BoardSide

    def __init__(self, following_player: CardPlayer, context: Context):
        self._context = context
        self._surface = context.get_service(PygameServices.SCREEN_SURFACE)
        self._card_engine = context.get_service(EncounterServices.CARD_ENGINE)
        self.following_player = following_player
        self._initialize_components()

    def update(self, delta: float) -> None:
        pass

    def render(self, delta: float) -> None:

        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        
        player2_mouse_pos = mouse_pos - pygame.Vector2(self.player2_side.rect.topleft)
        player1_mouse_pos = mouse_pos - pygame.Vector2(self.player1_side.rect.topleft)

        self._surface.blit(self.player2_side.draw_to_surface(player2_mouse_pos, True), self.player2_side.get_rect())
        self._surface.blit(self.player1_side.draw_to_surface(player1_mouse_pos), self.player1_side.get_rect())

    def _initialize_components(self):
        screen_size = pygame.Vector2(self._surface.get_size())
        board_size = pygame.Vector2(
            screen_size.x,
            screen_size.y / 2 - BoardRenderer.BOARD_SPACE_BETWEEN / 2
        )

        board_context = self._card_engine.board_context
        player1 = board_context.player1 if board_context.player1 == self.following_player else board_context.player2
        player2 = board_context.player2 if board_context.player2 != self.following_player else board_context.player1

        self.player1_side = BoardSide(pygame.Rect(
            0,board_size.y + BoardRenderer.BOARD_SPACE_BETWEEN,
            board_size.x, board_size.y   
        ), player1, self._context)
        self.player2_side = BoardSide(pygame.Rect(
            0,0,
            board_size.x, board_size.y   
        ), player2, self._context)
        
