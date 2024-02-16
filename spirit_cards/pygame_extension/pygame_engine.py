from dataclasses import dataclass
import pygame

from spirit_cards.core.engine import Engine
from spirit_cards.core.scene import Scene

from spirit_cards.pygame_extension.pygame_services import *
from spirit_cards.pygame_extension.event_buffer import EventBuffer

@dataclass
class PygameConfiguration:
    start_scene: type[Scene]
    start_scene_parameters: any
    clear_color: str = "black"
    frame_rate: int = 60


class PygameEngine:
    
    _startup_services: dict[str, any]
    _engine: Engine

    running = False

    def __init__(self, services: dict[str, any]):
        pygame.init()
        self._startup_services = services

    def run(self, configuration: PygameConfiguration) -> None:
        self.running = True

        clock = pygame.time.Clock()
        tick_rate = 1000/configuration.frame_rate

        pygame.display.set_caption("SpiritCards")
        surface = pygame.display.set_mode((1280, 720))

        icon = pygame.Surface((32, 32))
        icon.fill(pygame.Color(0,0,0))
        pygame.display.set_icon(icon)

        event_buffer = EventBuffer()

        self.engine = Engine({
            SCREEN_SURFACE: surface,
            EVENT_BUFFER: event_buffer,
            **self._startup_services
        })

        if(configuration.start_scene is not None):
            self.engine.load_scene(
                configuration.start_scene(self.engine.context),
                configuration.start_scene_parameters
                )

        last_ticks: int = 0
        current_ticks: int = 0

        while self.running:

            event_buffer.update(pygame.event.get())

            for event in event_buffer.get_events():
                if event.type == pygame.QUIT:
                    self.running = False

            surface.fill(configuration.clear_color)

            current_ticks = pygame.time.get_ticks()
            delta = (current_ticks - last_ticks) / tick_rate
            last_ticks = current_ticks

            self.engine.process(delta)
            
            pygame.display.update()
            pygame.display.flip()

            clock.tick(configuration.frame_rate)

    def cleanup(self) -> None:
        pygame.quit()