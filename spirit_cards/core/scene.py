from spirit_cards.core.entity_manager import EntityManager
from spirit_cards.core.context import Context

class Scene:

    entity_manager: EntityManager = EntityManager()
    context: Context

    def __init__(self, context: Context):
        self.context = context

    def process(self, delta: float) -> None:
        pass

    def init(self, parameters: any) -> None:
        pass

    def cleanup(self) -> None:
        pass