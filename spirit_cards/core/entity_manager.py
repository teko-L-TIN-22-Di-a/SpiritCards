from spirit_cards.core.entity import Entity

class EntityManager:
    
    _entities: list[Entity] = []
    _map: dict[str, list[Entity]] = {}

    def get_all(self) -> list[Entity]:
        return self._entities.copy()
    
    def get_filtered(self, tag: str) -> list[Entity]:
        if(tag not in self._map):
            return []

        return self._map[tag].copy()

    def register(self, entity: Entity, tags: list[str] = []) -> None:
        self._entities.append(entity)

        for tag in tags:
            if(tag not in self._map):
                self._map[tag] = []

            self._map[tag].append(entity)

    def update(self, delta: int) -> None:
        for entity in self._entities: entity.update(delta)

    def render(self, delta: int) -> None:
        for entity in self._entities: entity.render(delta)

    def cleanup(self) -> None:
        
        for entity in self._entities: entity.cleanup()

        self._entities.clear()
        self._map.clear()
