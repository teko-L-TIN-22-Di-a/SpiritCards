
import pygame

from dataclasses import dataclass

from spirit_cards.core.engine_services import SCENE_SWITCHER

from spirit_cards.core.scene import Scene
from spirit_cards.core.scene_switcher import SceneSwitcher
from spirit_cards.pygame_extension.load_scene.asset_loader import LoadThread
from spirit_cards.pygame_extension.pygame_services import EVENT_BUFFER, SCREEN_SURFACE
from spirit_cards.services.asset_manager import AssetManager, AssetType
from spirit_cards.services.global_services import ASSET_MANAGER

@dataclass
class LoadSceneParameters:
    # Format: { path: type }
    load_files: dict[str, AssetType]
    scene: type[Scene]
    scene_parameters: any = None

class LoadScene(Scene):

    _parameters: LoadSceneParameters

    _scene_switcher: SceneSwitcher
    _surface: pygame.Surface
    _asset_manager: AssetManager

    _font: pygame.font.Font
    _thread: LoadThread  

    def init(self, parameters: LoadSceneParameters) -> None:
        self._parameters = parameters

        self._scene_switcher = self.context.get_service(SCENE_SWITCHER)
        self._surface = self.context.get_service(SCREEN_SURFACE)
        self._asset_manager = self.context.get_service(ASSET_MANAGER)

        self._font = pygame.font.SysFont('timesnewroman',  24)

        self._thread = LoadThread(parameters.load_files)
        self._thread.start()

    def process(self, delta: float) -> None:

        if(not self._thread.is_alive()):
            self._asset_manager.register_asset_map(self._thread._load_results)
            self._thread.join()
            self._scene_switcher.load_scene(self._parameters.scene(self.context), self._parameters.scene_parameters)


        text = self._font.render("...", True, "White")
        self._surface.blit(text, (4, 4))

    def cleanup(self) -> None:
        pass