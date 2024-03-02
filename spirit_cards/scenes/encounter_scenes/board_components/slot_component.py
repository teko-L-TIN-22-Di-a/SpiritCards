
import pygame
from spirit_cards.card_engine.slot import Slot
from spirit_cards.pygame_extension.gui.ui_component import UIComponent


class SlotComponent(UIComponent):
    card_size: pygame.Vector2
    slot: Slot