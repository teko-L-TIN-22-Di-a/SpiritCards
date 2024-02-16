from spirit_cards.core.entity import Entity

class EntityManager:
    
    _entities: list[Entity] = []

    def register(self, entity: Entity) -> None:
        self._entities.append(entity)

    def update(self, delta: int) -> None:
        for entity in self._entities: entity.update(delta)

    def render(self, delta: int) -> None:
        for entity in self._entities: entity.render(delta)

    def cleanup(self) -> None:
        
        for entity in self._entities: entity.cleanup()

        self._entities.clear()
