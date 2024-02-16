
from spirit_cards.core.scene import Scene

# Acts as an interface for the Service SceneSwitcher, logic is implemented under engine.
class SceneSwitcher:
    def load_scene(self, scene: Scene, parameters: any = None) -> None:
        pass