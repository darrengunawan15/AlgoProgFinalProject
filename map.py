import pygame
from pytmx import load_pygame

class Map(pygame.sprite.Sprite):
    def __init__(self, screen, tmx_map_path):
        """
        Initializes a Map object, loading a Tiled map from the specified file path.

        Parameters:
        - screen (pygame.Surface): The surface where the map tiles will be drawn.
        - tmx_map_path (str): The file path to the Tiled map file.
        """

        super().__init__()
        self.screen = screen
        self.tmx_map = load_pygame(tmx_map_path)
        self.block_size = self.tmx_map.tilewidth

        # Create a sprite group for map tiles
        self.tiles_group = pygame.sprite.Group()
        self.load_tiles()

    def load_tiles(self):
        """
        Loads map tiles from the Tiled map and creates sprite objects for each tile.

        This method should be called during the initialization to populate the tiles_group.
        """

        for layer in self.tmx_map.layers:
            for x, y, gid, in layer:
                tile = self.tmx_map.get_tile_image_by_gid(gid)
                if tile:
                    tile_sprite = pygame.sprite.Sprite()
                    tile_sprite.image = tile
                    tile_sprite.rect = tile.get_rect()
                    tile_sprite.rect.x = x * self.block_size
                    tile_sprite.rect.y = y * self.block_size

                    # Add the tile sprite to the tiles_group
                    self.tiles_group.add(tile_sprite)

    def draw(self):
        """
        Draws the map tiles on the specified screen.
        """
        
        # Draw the tiles from the tiles_group
        self.tiles_group.draw(self.screen)

    def get_colliding_tiles(self, player_rect):
        """
        Retrieves a list of tile sprites that collide with the provided player_rect.

        Parameters:
        - player_rect (pygame.Rect): The rectangle representing the player's position and dimensions.
        """

        # Return a list of tile sprites that collide with the player_rect
        return [tile for tile in self.tiles_group if tile.rect.colliderect(player_rect)]