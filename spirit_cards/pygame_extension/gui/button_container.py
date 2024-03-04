import pygame
from spirit_cards.pygame_extension.gui.button import Button
from spirit_cards.pygame_extension.gui.ui_component import UIComponent


class ButtonContainer(UIComponent):
    
    _buttons: list[Button]

    def __init__(self, buttons: list[Button]):

        max_width = max(map(lambda x: x.get_rect().width, buttons))
        height = sum(map(lambda x: x.get_rect().height, buttons))

        super().__init__(pygame.Rect(
            0,0,
            max_width, height
        ))

        self._buttons = buttons
        self._init_component()

    def get_surface(self) -> pygame.Surface:
        
        surface = pygame.Surface(self.get_rect().size)
        surface.fill("black")

        for button in self._buttons:
            surface.blit(button.get_surface(), button.get_local_rect())

        return surface

    def update(self) -> pygame.Surface:
        for button in self._buttons: button.update()

    def _init_component(self):
        curr_pos = 0
        for button in self._buttons:
            button.rect = button.rect.move(0, curr_pos)
            button.relative_to = self
            curr_pos += button.get_rect().height