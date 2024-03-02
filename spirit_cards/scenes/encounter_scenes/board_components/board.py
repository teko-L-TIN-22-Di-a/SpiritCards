import pygame
from dataclasses import dataclass
from spirit_cards.card_engine.board_context import BoardContext

from spirit_cards.card_engine.slot import Slot
from spirit_cards.core.context import Context
from spirit_cards.core.entity import Entity
from spirit_cards.pygame_extension.gui.ui_component import UIComponent
from spirit_cards.pygame_extension.pygame_services import PygameServices


@dataclass
class BoardConfiguration:
    battle_slot_count = BoardContext.BATTLE_SLOT_COUNT
    support_slot_count = BoardContext.SUPPORT_SLOT_COUNT
    hand_size = BoardContext.HAND_SIZE

class BoardSide:

    board_component: UIComponent
    battle_zone: UIComponent
    support_zone: UIComponent
    hand_zone: UIComponent

    battle_slots: list[Slot]
    support_slots: list[Slot]
    hand_slots: list[Slot]

    def __init__(self, config: BoardConfiguration):
        self.battle_slots = [Slot() for x in range(0, config.battle_slot_count)]
        self.support_slots = [Slot() for x in range(0, config.support_slot_count)]
        self.hand_slots = []

    def init_sizes(self, screen_size: pygame.Vector2):
        margin = 24
        card_size = pygame.Vector2((185, 256))
        board_space_between = 64

        #TODO add Grave add Deck

        self.board_component = UIComponent(pygame.Rect(
            0,0,
            screen_size.x,
            screen_size.y / 2 - board_space_between / 2
        ))

        self.battle_zone = UIComponent(pygame.Rect(
            0,0,
            pygame.Vector2(self.board_component.get_rect().size).x * 0.64,
            pygame.Vector2(self.board_component.get_rect().size).y * 0.55
        ))

        self.support_zone = UIComponent(pygame.Rect(
            0, self.battle_zone.get_rect().bottom,
            pygame.Vector2(self.board_component.get_rect().size).x * 0.28,
            pygame.Vector2(self.board_component.get_rect().size).y * 0.45,
        ))
        self.hand_zone = UIComponent(pygame.Rect(
            self.support_zone.get_rect().right, self.battle_zone.get_rect().bottom,
            pygame.Vector2(self.board_component.get_rect().size).x * 0.72,
            pygame.Vector2(self.board_component.get_rect().size).y * 0.45
        ))

    def get_test(self) -> pygame.Surface:
        board_surface = pygame.Surface(self.board_component.get_rect().size)
        
        pygame.draw.rect(board_surface, "Blue", self.board_component.get_rect())
        pygame.draw.rect(board_surface, "Green", self.battle_zone.get_rect())
        pygame.draw.rect(board_surface, "Red", self.support_zone.get_rect())
        pygame.draw.rect(board_surface, "Cyan", self.hand_zone.get_rect())

        return board_surface

class Board(Entity):

    _surface: pygame.surface.Surface

    player1_side: BoardSide
    player2_side: BoardSide

    def __init__(self, context: Context, config: BoardConfiguration = None):

        if(config is None):
            config = BoardConfiguration()

        self._surface = context.get_service(PygameServices.SCREEN_SURFACE)

        self.player1_side = BoardSide(config)
        self.player1_side.init_sizes(pygame.Vector2(self._surface.get_size()))
        self.player2_side = BoardSide(config)
        self.player2_side.init_sizes(pygame.Vector2(self._surface.get_size()))

    def update(self, delta: float) -> None:
        pass

    def render(self, delta: float) -> None:

        board_space_between = 64

        self._surface.blit(pygame.transform.rotate(self.player2_side.get_test(), 180), (0,0))
        self._surface.blit(self.player1_side.get_test(), (0,self.player2_side.board_component.get_rect().size[1] + board_space_between))

        pygame.draw.rect(self._surface, "pink", pygame.Rect(0,0, 64, 64))

        
