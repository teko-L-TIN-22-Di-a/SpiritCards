
from dataclasses import dataclass
from typing import Literal

import pygame

from spirit_cards.core.engine_services import SCENE_SWITCHER

from spirit_cards.core.scene import Scene
from spirit_cards.core.scene_switcher import SceneSwitcher
from spirit_cards.main_scenes.load_scene.load_thread import LoadThread
from spirit_cards.pygame_extension.pygame_services import EVENT_BUFFER, SCREEN_SURFACE

@dataclass
class LoadSceneParameters:
    # Format: { path: type }
    load_files: dict[str, Literal["image"]]
    scene: type[Scene]
    scene_parameters: any = None

class LoadScene(Scene):

    _parameters: LoadSceneParameters

    _scene_switcher: SceneSwitcher
    _surface: pygame.Surface
    
    _font: pygame.font.Font
    _thread: LoadThread  

    def init(self, parameters: LoadSceneParameters) -> None:
        self._parameters = parameters

        self._scene_switcher = self.context.get_service(SCENE_SWITCHER)

        self._surface = self.context.get_service(SCREEN_SURFACE)

        self._font = pygame.font.SysFont('timesnewroman',  24)

        self._thread = LoadThread()
        self._thread.start()

    def process(self, delta: float) -> None:

        if(not self._thread.is_alive()):
            self._thread.join()
            self._scene_switcher.load_scene(self._parameters.scene(self.context), self._parameters.scene_parameters)

        text = self._font.render("Loading...", True, "White")
        self._surface.blit(text, (4, 4))

    def cleanup(self) -> None:
        pass