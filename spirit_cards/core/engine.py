from spirit_cards.core.scene import Scene
from spirit_cards.core.context import Context
from spirit_cards.core.scene_switcher import SceneSwitcher
from spirit_cards.core.engine_services import *

class Engine(SceneSwitcher):
    
    current_scene: Scene = None
    context: Context

    def __init__(self, services: dict[str,any]):
        self.context = Context(services)

        self.context.set_service(SCENE_SWITCHER, self)

    def load_scene(self, scene: Scene, parameters: any = None) -> None:
        if self.current_scene is not None: 
            self.current_scene.cleanup()
            print(f"Engine | cleanup {type(self.current_scene).__name__} success")
        
        print(f"Engine | transitioning to scene {type(scene).__name__}")
        print("Engine | with parameters: " + ("None" if parameters is None else str(vars(parameters))))
        self.current_scene = scene
        self.context.set_service(CURRENT_SCENE, scene)
        self.current_scene.init(parameters)
        print(f"Engine | init {type(scene).__name__} success")

    def process(self, delta: float) -> None:

        if self.current_scene is None:
           print("No current loaded scene please call load_scene!")
           return

        self.current_scene.process(delta)