import pygame
from spirit_cards.card_engine.board_context import BoardContext
from spirit_cards.pygame_extension.gui.ui_component import UIComponent
from spirit_cards.scenes.encounter_scenes.board_components.slot_component import SlotComponent


class BattleZone(UIComponent):

    slots_components: list[SlotComponent] = []

    def __init__(self, rect: pygame.Rect, margin: pygame.Vector2):
        super().__init__(rect, margin)

        self._initialize_component()

    def _initialize_component(self):
        margin = pygame.Vector2(24, 4)
        inner_rect = self.get_inner_rect()
        slot_size = pygame.Vector2(inner_rect.width / BoardContext.BATTLE_SLOT_COUNT, inner_rect.height)

        for i in range(0, BoardContext.BATTLE_SLOT_COUNT):
            self.slots_components.append(SlotComponent(pygame.Rect(
                inner_rect.x + slot_size.x * i, inner_rect.y + 0,
                slot_size.x, slot_size.y
            ), margin))