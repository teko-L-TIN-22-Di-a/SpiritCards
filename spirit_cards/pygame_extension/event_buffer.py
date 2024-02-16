import pygame

class EventBuffer:
    _events: list[pygame.event.Event] = []

    def update(self, events: list[pygame.event.Event]) -> None:
        self._events = events

    def get_events(self) -> list[pygame.event.Event]:
        return self._events.copy()
