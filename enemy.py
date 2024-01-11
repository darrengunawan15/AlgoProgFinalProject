import pygame
import os

class Enemy(pygame.sprite.Sprite):
    def __init__(self, map_instance, x, y, enemies_group):
        """
        Initializes an Enemy object.

        Parameters:
        - map_instance (Map): The map instance associated with the enemy.
        - x (int): The initial x-coordinate of the enemy on the map.
        - y (int): The initial y-coordinate of the enemy on the map.
        - enemies_group (pygame.sprite.Group): The group containing all enemy sprites.
        """

        super().__init__()
        self.map = map_instance
        self.enemies_group = enemies_group

        # Load enemy animation frames
        self.parent_path = "assets/enemies/"
        self.monster_sheet = pygame.image.load(os.path.join(self.parent_path, "ghost.png")).convert_alpha()

        # Scaling enemy
        self.scale_factor = 3
        self.monster_frames = [pygame.transform.scale(self.monster_sheet.subsurface(pygame.Rect(i * 32, 0, 32, 32)), (int(16 * self.scale_factor), int(16 * self.scale_factor))) for i in range(4)]
       
        self.frame_index = 0
        self.image = self.monster_frames[self.frame_index]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Animation settings
        self.animation_speed = 0.2
        self.animation_timer = pygame.time.get_ticks()

        self.health = 100

        self.hit_cooldown = 1000  # in milliseconds
        self.last_hit_time = pygame.time.get_ticks()

    def update(self, player):
        """
        Updates the enemy's animation and checks for collisions with the player.

        Parameters:
        - player (Player): The player object.
        """

        # Animation
        current_time = pygame.time.get_ticks()
        if current_time - self.animation_timer > self.animation_speed * 1000:
            self.animation_timer = current_time
            self.frame_index = (self.frame_index + 1) % len(self.monster_frames)
            self.image = self.monster_frames[self.frame_index]

        # Cooldown between hit
        current_time = pygame.time.get_ticks()
        if current_time - self.last_hit_time > self.hit_cooldown:
            if pygame.sprite.collide_rect(self, player):
                player.hit()
                self.last_hit_time = current_time

    def draw(self, screen, camera):
        """
        Draws the enemy on the specified screen using the camera transformation.

        Parameters:
        - screen (pygame.Surface): The surface where the enemy will be drawn.
        - camera (Camera): The camera object for transforming the enemy's position.
        """

        screen.blit(self.image, camera.apply(self))
