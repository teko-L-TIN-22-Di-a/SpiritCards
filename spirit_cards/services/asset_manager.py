import pygame

from enum import Enum

class AssetType(Enum):
    Image = "Image"
    Font = "Font"

class AssetManager:
    
    _asset_map: dict[str, any] = {}

    def register_asset_map(self, asset_map: dict[str, any]) -> None:
        for entry in asset_map: self._asset_map[entry] = asset_map[entry]

    def register_assets(self, key: str, asset: any) -> None:
        self._asset_map[key] = asset

    def get_asset(self, key: str) -> any:
        return self._asset_map[key]
    
    def get_image(self, key: str) -> pygame.surface.Surface:
        return self.get_asset_type_safe(key, pygame.surface.Surface)
    
    def get_font(self, key: str) -> pygame.font.Font:
        return self.get_asset_type_safe(key, pygame.font.Font)
    
    def get_asset_type_safe(self, key: str, asset_type: type) -> any:
        asset = self._asset_map[key]

        if type(asset) is asset_type: return asset
        
        raise Exception(f"AssetManager | Tried to Load '{key}' as '{asset_type.__qualname__}' but was '{type(asset).__qualname__}'")