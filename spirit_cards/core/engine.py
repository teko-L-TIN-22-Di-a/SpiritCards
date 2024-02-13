from .scene import Scene
from .context import Context

class Engine:
    
    _current_scene: Scene = None
    context: Context

    def __init__(self, services: dict[str,any]):
        self.context = Context(services)

    def load_scene(self, scene: Scene) -> None:
        if self._current_scene is not None: 
            self._current_scene.cleanup()
        
        self._current_scene = scene
        self._current_scene.init()

    def process(self, delta: int) -> None:

        if self._current_scene is None:
           print("No current loaded scene please call load_scene!")
           return

        self._current_scene.process(delta)