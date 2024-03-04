from dataclasses import dataclass
from typing import Callable
from pygame import Rect
import pygame
from spirit_cards.asset_map import AssetMap
from spirit_cards.core.context import Context
from spirit_cards.pygame_extension.event_buffer import EventBuffer
from spirit_cards.pygame_extension.gui.ui_component import UIComponent
from spirit_cards.pygame_extension.pygame_services import PygameServices
from spirit_cards.services.asset_manager import AssetManager
from spirit_cards.services.global_services import GlobalServices

@dataclass
class ButtonConfig:
    tag: str
    text: str
    size: pygame.Vector2
    on_click: Callable[[str], None]

class Button(UIComponent):

    _event_buffer: EventBuffer
    _font: pygame.font.Font

    mouse_over: bool = False

    button_config: ButtonConfig

    def __init__(self, context: Context, config: ButtonConfig):
        self.button_config = config
        super().__init__(pygame.Rect(
            0,0,
            config.size.x, config.size.y
        ))

        self._event_buffer = context.get_service(PygameServices.EVENT_BUFFER)
        asset_manager: AssetManager = context.get_service(GlobalServices.ASSET_MANAGER)
        self._font = asset_manager.get_font(AssetMap.MONTSERRAT_24)
        
    def get_surface(self) -> pygame.Surface:
        surface = pygame.Surface(self.button_config.size)
        center = pygame.Vector2(surface.get_rect().center)
        text_surface = self._font.render(self.button_config.text, True, "White")
        
        if(self.mouse_over):
            surface.fill("darkgray")

        surface.blit(text_surface, center - pygame.Vector2(text_surface.get_rect().center))

        return surface

    def update(self) -> pygame.Surface:
        self.mouse_over = False
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())

        if(self.get_rect().collidepoint(mouse_pos)):
            self.mouse_over = True

            for event in self._event_buffer.get_events():
                if(event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                    self.button_config.on_click(self.button_config.tag)

        

            