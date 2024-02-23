import pygame
from spirit_cards.asset_map import MONTSERRAT_24

from spirit_cards.core.engine_services import *
from spirit_cards.core.scene import Scene
from spirit_cards.core.scene_switcher import SceneSwitcher

from spirit_cards.pygame_extension.pygame_services import *
from spirit_cards.pygame_extension.event_buffer import EventBuffer

from spirit_cards.example_code.secondary_scene import SecondaryScene
from spirit_cards.services.asset_manager import AssetManager
from spirit_cards.services.global_services import ASSET_MANAGER

class BoardPrototypeScene(Scene):

    _surface: pygame.Surface
    _event_buffer: EventBuffer
    _scene_switcher: SceneSwitcher

    _font: pygame.font.Font

    def init(self, parameters: any = None) -> None:

        self._scene_switcher = self.context.get_service(SCENE_SWITCHER)

        self._surface = self.context.get_service(SCREEN_SURFACE)
        self._event_buffer = self.context.get_service(EVENT_BUFFER)

        asset_manager: AssetManager = self.context.get_service(ASSET_MANAGER)
        self._font = asset_manager.get_font(MONTSERRAT_24)

    def process(self, delta: int) -> None:

        # for e in self._event_buffer.get_events():
        #     if(e.type == pygame.KEYDOWN and e.key == pygame.K_2):
        #         print("switching scene")
        #         self._scene_switcher.load_scene(SecondaryScene(self.context))

        self._surface.fill("White")
        text = self._font.render(str(delta), True, "Black")
        self._surface.blit(text, (4, 4))

    def cleanup(self) -> None:
        pass
