import pygame
from dataclasses import dataclass

from spirit_cards.core.context import Context
from spirit_cards.core.entity import Entity
from spirit_cards.pygame_extension.pygame_services import PygameServices
from spirit_cards.scenes.encounter_scenes.board_components.board_side import BoardSide

class Board(Entity):

    BOARD_SPACE_BETWEEN = 32

    _context: Context
    _surface: pygame.surface.Surface

    player1_side: BoardSide
    player2_side: BoardSide

    def __init__(self, context: Context):
        self._context = context
        self._surface = context.get_service(PygameServices.SCREEN_SURFACE)
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
            screen_size.y / 2 - Board.BOARD_SPACE_BETWEEN / 2
        )

        self.player1_side = BoardSide(pygame.Rect(
            0,board_size.y + Board.BOARD_SPACE_BETWEEN,
            board_size.x, board_size.y   
        ), self._context)
        self.player2_side = BoardSide(pygame.Rect(
            0,0,
            board_size.x, board_size.y   
        ), self._context)
        
