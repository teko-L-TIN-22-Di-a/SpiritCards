
from dataclasses import dataclass
import pygame
from spirit_cards.core.context import Context
from spirit_cards.core.entity import Entity
from spirit_cards.pygame_extension.event_buffer import EventBuffer
from spirit_cards.pygame_extension.gui.ui_component import UIComponent
from spirit_cards.pygame_extension.pygame_services import PygameServices


@dataclass
class MsgBoxConfiguration:
    component: UIComponent
    position: pygame.Vector2 = None # Can be None and the center of the screen will be used.
    close_on_click: bool = True

class MsgBox(Entity):

    _surface: pygame.Surface
    _event_buffer: EventBuffer

    current_configuration: MsgBoxConfiguration = None
    visible: bool = False

    def __init__(self, context: Context):
        self._surface = context.get_service(PygameServices.SCREEN_SURFACE)
        self._event_buffer = context.get_service(PygameServices.EVENT_BUFFER)

    def show(self, config: MsgBoxConfiguration) -> None:
        self.current_configuration = config
        self.visible = True

    def close(self) -> None:
        self.visible = False

    def update(self, delta: float) -> None:
        if(self.current_configuration is None or not self.visible):
            return
        
        if(not self.current_configuration.close_on_click):
            return
        
        for event in self._event_buffer.get_events():
            if(event.type != pygame.MOUSEBUTTONDOWN):
                continue

            mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
            component = self.current_configuration.component
            component_rect = component.get_rect().move(self.get_position()).move(-pygame.Vector2(component.get_rect().center))

            if(not component_rect.collidepoint(mouse_pos.x, mouse_pos.y)):
                self.close()
        

    def render(self, delta: float) -> None:
        if(self.current_configuration is None or not self.visible):
            return
        
        component = self.current_configuration.component
        component_rect = component.get_rect().move(self.get_position()).move(-pygame.Vector2(component.get_rect().center))
        pygame.draw.rect(self._surface, "red", component_rect)

    def get_position(self) -> pygame.Vector2:
        if(self.current_configuration.position is not None):
            return self.current_configuration.position
        else:
            return pygame.Vector2(self._surface.get_rect().center)