from .entity_manager import EntityManager
from .context import Context

class Scene:

    entity_manager: EntityManager = EntityManager
    context: Context

    def __init__(self, context: Context):
        self.context = context

    def process(self, delta: int) -> None:
        pass

    def init(self) -> None:
        pass

    def cleanup(self) -> None:
        pass