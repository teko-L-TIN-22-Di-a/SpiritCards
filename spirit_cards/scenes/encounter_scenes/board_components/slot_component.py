
import pygame
from spirit_cards.card_engine.slot import Slot
from spirit_cards.pygame_extension.gui.ui_component import UIComponent


class SlotComponent(UIComponent):
    card_size: pygame.Vector2
    slot: Slot

    def __init__(self, slot: Slot, rect: pygame.Rect, margin: pygame.Vector2 = pygame.Vector2(0,0)):
        super().__init__(rect, margin)
        self.slot = slot