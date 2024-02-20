
import pygame

from dataclasses import dataclass
from threading import Thread

from spirit_cards.services.asset_manager import AssetType

DEFAULT_FONT_SIZE = 16
FONT_SIZE = "font_size"

@dataclass
class AssetLoadConfiguration:
    type: AssetType
    parse_parameters: any = None

class AssetLoader():
    def load(load_entries: dict[str, AssetLoadConfiguration]) -> dict[str, any]:
        load_results: dict[str, any] = {}

        for entry in load_entries:
            
            if(load_entries[entry].type == AssetType.Image):
                print(f"LoadThread | Loading image '{entry}'")
                load_results[entry] = pygame.image.load(entry)
                continue

            if(load_entries[entry].type == AssetType.Font):
                print(f"LoadThread | Loading font '{entry}'")
                parse_parameters = load_entries[entry].parse_parameters
                font_size = parse_parameters[FONT_SIZE] if parse_parameters[FONT_SIZE] is not None else DEFAULT_FONT_SIZE
                load_results[entry] = pygame.font.Font(entry, font_size)
                continue

            print(f"LoadThread | Couldn't load {entry} unkown type {load_entries[entry].type}")

        return load_results

class LoadThread(Thread):

    _load_entries: dict[str, AssetType]
    _load_results: dict[str, any] = {}

    def __init__(self, load_entries: dict[str, AssetType]):
        super().__init__()
        self._load_entries = load_entries


    def run(self):
        self._load_results = AssetLoader.load(self._load_entries)        

            
        
