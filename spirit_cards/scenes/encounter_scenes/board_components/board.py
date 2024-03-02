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

    battle_slots: list[Slot]
    support_slots: list[Slot]
    hand_slots: list[Slot]

    def __init__(self, config: BoardConfiguration):
        self.battle_slots = [Slot() for x in range(0, config.battle_slot_count)]
        self.support_slots = [Slot() for x in range(0, config.support_slot_count)]
        self.hand_slots = []

class Board(Entity):

    _surface: pygame.surface.Surface

    player1_side: BoardSide
    player2_side: BoardSide

    def __init__(self, context: Context, config: BoardConfiguration = None):

        if(config is None):
            config = BoardConfiguration()

        self.player1_side = BoardSide(config)
        self.player2_side = BoardSide(config)

        self._surface = self.context.get_service(PygameServices.SCREEN_SURFACE)

        self._init_sizes(context)

    def update(self, delta: float) -> None:
        pass

    def render(self, delta: float) -> None:
        pass

    def _init_sizes(self, context: Context) -> None:
        
        margin = 24
        card_size = pygame.Vector2((185, 256))
        board_space_between = 124
        
        size = pygame.Vector2(self._surface.get_size())

        board_size = pygame.Vector2(
            
        )

        hand_zone_size = pygame.Vector2(
            board_size.x * 0.36,
            board_size.y * 0.8
        )
        #TODO add Grave add Deck

        board_component = UIComponent(pygame.Rect(
            0,0,
            size.x,
            size.y / 2 - board_space_between
        ))

        battle_zone = UIComponent(pygame.Rect(
            0,0,
            board_size.x * 0.64,
            board_size.y * 1.2
        ))

        support_zone = UIComponent(pygame.Rect(
            0,
            battle_zone.get_rect().bottom,
            board_size.x * 0.28,
            board_size.y * 0.8,
        ))

        

        
