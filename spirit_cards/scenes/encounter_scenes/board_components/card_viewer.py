import pygame
from spirit_cards.pygame_extension.gui.ui_component import UIComponent


class CardViewer(UIComponent):

    card_texture: pygame.Surface

    def __init__(self, card_texture: pygame.Surface):
        self.card_texture = pygame.transform.smoothscale_by(card_texture, 0.5)
        size = pygame.Vector2(self.card_texture.get_size())
        super().__init__(pygame.Rect(
            0, 0,
            size.x, size.y
        ))

    def get_surface(self) -> pygame.Surface:
        return self.card_texture