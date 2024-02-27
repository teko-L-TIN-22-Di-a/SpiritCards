import pygame

from spirit_cards.core.engine_services import *
from spirit_cards.core.scene import Scene
from spirit_cards.core.scene_switcher import SceneSwitcher

from spirit_cards.pygame_extension.pygame_services import *
from spirit_cards.pygame_extension.event_buffer import EventBuffer

from spirit_cards.example_code.secondary_scene import SecondaryScene

class ExampleScene(Scene):

    _surface: pygame.Surface
    _event_buffer: EventBuffer
    _scene_switcher: SceneSwitcher

    _font: pygame.font.Font

    def init(self, parameters: any = None) -> None:

        self._scene_switcher = self.context.get_service(EngineServices.SCENE_SWITCHER)

        self._surface = self.context.get_service(PygameServices.SCREEN_SURFACE)
        self._event_buffer = self.context.get_service(PygameServices.EVENT_BUFFER)

        self._font = pygame.font.SysFont('timesnewroman',  24)

    def process(self, delta: int) -> None:

        for e in self._event_buffer.get_events():
            if(e.type == pygame.KEYDOWN and e.key == pygame.K_2):
                print("switching scene")
                self._scene_switcher.load_scene(SecondaryScene(self.context))

        self._surface.fill("White")
        text = self._font.render(str(delta), True, "Black")
        self._surface.blit(text, (4, 4))

    def cleanup(self) -> None:
        pass
