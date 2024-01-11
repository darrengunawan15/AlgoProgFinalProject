import pygame
import os

class Item(pygame.sprite.Sprite):
    def __init__(self, screen, map_instance, camera, x, y, pathname, points, items_group, game_instance):
        """
        Initializes an Item object.

        Parameters:
        - screen (pygame.Surface): The surface where the item will be drawn.
        - map_instance (Map): The map instance associated with the item.
        - camera (Camera): The camera object for transforming the item's position.
        - x (int): The initial x-coordinate of the item on the map.
        - y (int): The initial y-coordinate of the item on the map.
        - pathname (str): The file path to the item's image file.
        - points (int): The points associated with collecting the item.
        - items_group (pygame.sprite.Group): The group containing all item sprites.
        - game_instance: An instance of the game class associated with the item. # Main game file
        """

        super().__init__()
        self.screen = screen
        self.map = map_instance
        self.camera = camera
        self.points = points
        self.game_instance = game_instance

        self.items_group = items_group

        # Load item image
        self.parent_path = "assets/items/"
        self.item_image = pygame.image.load(os.path.join(self.parent_path, pathname)).convert_alpha()

        # Scale item
        self.scale_factor = 2
        self.image = pygame.transform.scale(self.item_image, (int(32 * self.scale_factor), int(32 * self.scale_factor)))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, player):
        """
        Updates the item, checking for collisions with the player.

        Parameters:
        - player (Player): The player object.
        """

        if pygame.sprite.collide_rect(self, player):
            self.collect_item(player)

    def draw(self):
        """
        Draws the item on the specified screen using the camera transformation.
        """

        self.screen.blit(self.image, self.camera.apply(self))

    def collect_item(self, player):
        """
        Handles the collection of the item by the player, updating points and applying special effects.

        Parameters:
        - player (Player): The player object.
        """

        # print(f"Item collected! Points: {self.points}") # For debugging purpose

        if self.points < 1000:
            player.update_points(self.points)
        else:
            if self.points == 1234:
                player.change_speed_y(-30)
            elif self.points == 2345:
                player.change_speed_x(8)
            elif self.points == 3456:
                self.game_instance.show_victory_screen()

        self.items_group.remove(self)