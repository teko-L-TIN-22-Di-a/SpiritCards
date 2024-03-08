import pygame
from spirit_cards.services.asset_manager import AssetManager
from spirit_cards.asset_map import AssetMap
from spirit_cards.services.global_services import GlobalServices
from spirit_cards.core.context import Context
from spirit_cards.scenes.gathering_scenes.isometric_tile import IsometricTile

class IsometricTileMap:

    _surface_dirty: bool = False
    _surface: pygame.surface.Surface = None

    asset_manager: AssetManager
    tile_map: list[list[IsometricTile]]
    map_size: pygame.Vector3
    tile_size: pygame.Vector3
    bounds: pygame.rect.Rect
    colliders: list[pygame.rect.Rect]

    # tile_size x, y and z is reserved for the full height
    def __init__(self, context: Context, map_description: list[list[int]]):
        self.asset_manager = context.get_service(GlobalServices.ASSET_MANAGER)
        self.colliders = []
        self.tile_map = self.create_tile_map(map_description)
        self.map_size = pygame.Vector3(len(map_description), 1, len(map_description[0]))
        _tile_size = pygame.Vector2(self.tile_map[0][0].texture.get_size())
        self.tile_size = pygame.Vector3(_tile_size.x, 100, _tile_size.y)
        self.bounds = pygame.Rect(0, 0, self.map_size.x, self.map_size.z)
        

    def create_tile_map(self, map_description):
        
        tile_map = [[]]
        for x, row in enumerate(map_description):
            for z, column in enumerate(row):
                tile = self.create_tile(column, x, z)

                # check tile_map array size and expand it, when necessary
                if len(tile_map) < x + 1:
                    tile_map.append([])
                if len(tile_map[x]) < z + 1:
                    tile_map[x].append(0)
                if not tile.accessible:
                    self.colliders.append(pygame.rect.Rect(x,z,1,1))
                tile_map[x][z] = tile

        return tile_map

    def create_tile(self, tile_id: int, tile_row: int, tile_column: int) -> IsometricTile:

        tile_name = "TILE"+str(tile_id)
        asset = AssetMap.__getattribute__(AssetMap, tile_name)
        texture = self.asset_manager.get_image(asset)
        access = True
        if tile_id in IsometricTile.non_accessible:
            access = False
        
        return IsometricTile(pygame.Vector3(tile_row,1,tile_column), texture, access)

    def get_map_texture(self) -> pygame.surface.Surface:

        if (self._surface is None or self._surface_dirty):
            self.regenerate_surface()

        return self._surface

    def regenerate_surface(self) -> None:
        
        x_width = self.map_size.x * (self.tile_size.x/2)
        z_width = self.map_size.z * (self.tile_size.x/2)
        y_component_x = self.map_size.x*self.tile_size.y/2
        y_component_z = self.map_size.z*self.tile_size.y/2
        y_padding = 50

        map_surface_size = pygame.Vector2(
            x_width + z_width,
            y_component_x + y_component_z + y_padding
        )

        self._surface = pygame.surface.Surface((map_surface_size.x, map_surface_size.y))
        self._surface.fill("green")

    def to_screen_space(self, position: pygame.Vector3) -> pygame.Vector2:

        x_part = pygame.Vector2((self.tile_size.x / 2) * position.x, (self.tile_size.y / 2) * position.x)
        z_part = pygame.Vector2((-self.tile_size.x / 2) * position.z, (self.tile_size.y / 2) * position.z)
        y_part = pygame.Vector2(0, (self.tile_size.y / 2) * position.y)

        surface_offset = pygame.Vector2(self._surface.get_width() / 2, 0)
        leaning_offset = pygame.Vector2((self.map_size.z - self.map_size.x) * self.tile_size.x / 4, 0)

        return x_part + z_part + y_part + surface_offset + leaning_offset
    