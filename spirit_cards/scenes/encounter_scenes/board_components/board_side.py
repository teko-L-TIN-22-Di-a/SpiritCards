
from dataclasses import dataclass
import pygame
from spirit_cards.card_engine.board_context import BoardContext
from spirit_cards.card_engine.slot import Slot
from spirit_cards.pygame_extension.gui.ui_component import UIComponent
    
class BoardSide(UIComponent):

    board_component: UIComponent
    battle_zone: UIComponent
    support_zone: UIComponent
    hand_zone: UIComponent

    battle_slots: list[Slot]
    support_slots: list[Slot]
    hand_slots: list[Slot]

    def __init__(self, rect: pygame.Rect):
        super().__init__(rect)

        self.battle_slots = [Slot() for x in range(0, BoardContext.BATTLE_SLOT_COUNT)]
        self.support_slots = [Slot() for x in range(0, BoardContext.SUPPORT_SLOT_COUNT)]
        self.hand_slots = []

        self._initialize_component()

    def _initialize_component(self):
        margin = pygame.Vector2(6, 6)
        card_size = pygame.Vector2((185, 256))
        board_space_between = 32

        #TODO add Grave add Deck

        self.battle_zone = UIComponent(pygame.Rect(
            0,0,
            pygame.Vector2(self.get_rect().size).x * 0.64,
            pygame.Vector2(self.get_rect().size).y * 0.55
        ), margin)

        self.support_zone = UIComponent(pygame.Rect(
            0, self.battle_zone.get_rect().bottom,
            pygame.Vector2(self.get_rect().size).x * 0.28,
            pygame.Vector2(self.get_rect().size).y * 0.45,
        ), margin)
        self.hand_zone = UIComponent(pygame.Rect(
            self.support_zone.get_rect().right, self.battle_zone.get_rect().bottom,
            pygame.Vector2(self.get_rect().size).x * 0.72,
            pygame.Vector2(self.get_rect().size).y * 0.45
        ), margin)

    def draw_to_surface(self) -> pygame.Surface:
        size = pygame.Vector2(self.get_rect().size)
        board_surface = pygame.Surface(size)
        
        pygame.draw.rect(board_surface, "#092B40", pygame.Rect(0,0,size.x, size.y))
        pygame.draw.rect(board_surface, "#405F73", self.battle_zone.get_inner_rect(), 2, 4)
        pygame.draw.rect(board_surface, "#405F73", self.support_zone.get_inner_rect(), 2, 4)
        pygame.draw.rect(board_surface, "#405F73", self.hand_zone.get_inner_rect(), 2, 4)

        return board_surface