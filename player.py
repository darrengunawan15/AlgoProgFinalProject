import pygame
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, screen, camera):
        """
        Initializes a Player object.

        Parameters:
        - screen (pygame.Surface): The surface where the player will be drawn.
        - camera (Camera): The camera object for transforming the player's position.
        """

        super().__init__()
        self.screen = screen
        self.camera = camera

        # Load player animation frames for different states
        self.parent_path = "assets/player/"
        self.idle_frames = [pygame.image.load(os.path.join(self.parent_path, f"player-idle{i}.png")).convert_alpha() for i in range(1, 7)]
        self.jump_frames = [pygame.image.load(os.path.join(self.parent_path, f"player-jump{i}.png")).convert_alpha() for i in range(1, 3)]
        self.run_frames = [pygame.image.load(os.path.join(self.parent_path, f"player-run{i}.png")).convert_alpha() for i in range(1, 7)]

        # Scaling player
        self.scale_factor = 1.5
        self.idle_frames = [pygame.transform.scale(frame, (frame.get_width() * self.scale_factor, frame.get_height() * self.scale_factor)) for frame in self.idle_frames]
        self.jump_frames = [pygame.transform.scale(frame, (frame.get_width() * self.scale_factor, frame.get_height() * self.scale_factor)) for frame in self.jump_frames]
        self.run_frames = [pygame.transform.scale(frame, (frame.get_width() * self.scale_factor, frame.get_height() * self.scale_factor)) for frame in self.run_frames]

        # Facing left
        self.idle_frames_left = [pygame.transform.flip(frame, True, False) for frame in self.idle_frames]
        self.jump_frames_left = [pygame.transform.flip(frame, True, False) for frame in self.jump_frames]
        self.run_frames_left = [pygame.transform.flip(frame, True, False) for frame in self.run_frames]

        self.frame_index = 0
        self.image = self.idle_frames[self.frame_index]

        self.rect = self.image.get_rect()
        self.rect.center = (screen.get_width() // 2, screen.get_height() // 2)
        self.screen_rect = screen.get_rect()

        # Animation settings
        self.animation_speed = 0.2
        self.animation_timer = pygame.time.get_ticks()

        # Player movement speed
        self.speed = 5

        self.jump_speed = -20

        # Player initial state
        self.state = "idle"
        self.player_direction = "right"
        self.y_velocity = 0
        self.jump_count = 1

        # Health
        self.max_health = 100
        self.health = self.max_health

        # Score
        self.score = 0

    def update(self, map_instance):
        """
        Updates the player's position, animation, and checks for collisions.

        Parameters:
        - map_instance (Map): The map instance associated with the player.
        """

        # Gravity
        self.y_velocity += 1
        self.rect.y += self.y_velocity
        self.map = map_instance

        # Check for collisions with map tiles
        colliding_tiles = self.map.get_colliding_tiles(self.rect)

        # Adjust the player's position based on collisions
        for tile in colliding_tiles:
            if self.y_velocity > 0:
                self.rect.bottom = tile.rect.top
                self.y_velocity = 0
                self.jump_count = 1 
            elif self.y_velocity < 0:
                self.rect.top = tile.rect.bottom - 1
                self.y_velocity = 0

        # Prevent player from falling below the screen
        if self.rect.bottom > 1728:
            self.rect.bottom = 1728
            self.y_velocity = 0
            self.jump_count = 1

        # Update animation frame
        current_time = pygame.time.get_ticks()
        if current_time - self.animation_timer > self.animation_speed * 1000:
            self.animation_timer = current_time
            self.frame_index = (self.frame_index + 1) % len(self.get_current_frames())
            self.image = self.get_current_frames()[self.frame_index]

    # Player movements
    def move(self):
        """
        Handles player movements based on keyboard input.

        The player can move left, right, and jump using the arrow keys or spacebar.
        """

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.player_direction = "left"
            self.state = "run-left"

            # Check for collisions with map tiles in the x-direction
            if not self.check_wall_collision(-self.speed):
                self.rect.x -= self.speed
                    
        elif keys[pygame.K_RIGHT] and self.rect.right < 2048:
            self.player_direction = "right"
            self.state = "run-right"

            # Check for collisions with map tiles in the x-direction
            if not self.check_wall_collision(self.speed):
                self.rect.x += self.speed
            
        else:
            if self.player_direction == "right":
                self.state = "idle-right"
            else:
                self.state = "idle-left"

        # Jump
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.rect.y > 0 and self.jump_count > 0:
            if self.player_direction == "right":
                self.state = "jump-right"
            else:
                self.state = "jump-left"

            self.y_velocity = self.jump_speed
            self.jump_count -= 1
            self.frame_index = 0

            if keys[pygame.K_LEFT] and not self.check_wall_collision(-self.speed) and self.rect.left > 0:
                self.rect.x -= self.speed
            elif keys[pygame.K_RIGHT] and not self.check_wall_collision(self.speed) and self.rect.right < 2048:
                self.rect.x += self.speed

    def get_current_frames(self):
        """
        Returns the current set of frames based on the player's state and direction.

        Returns:
        - list: The list of frames for the current player state and direction.
        """

        frame_dict = {
            "idle-right": self.idle_frames,
            "idle-left": self.idle_frames_left,
            "jump-right": self.jump_frames,
            "jump-left": self.jump_frames_left,
            "run-right": self.run_frames,
            "run-left": self.run_frames_left
        }

        return frame_dict.get(self.state, self.idle_frames)  # Default to idle frames if state is not found

        
    def draw(self):
        self.screen.blit(self.image, self.rect)
    
    def check_wall_collision(self, x_offset):
        """
        Checks for collisions with map tiles in the x-direction.

        Parameters:
        - x_offset (int): The amount to offset the player's position in the x-direction.

        Returns:
        - bool: True if a collision is detected, False otherwise.
        """
         
        temp_rect = self.rect.copy()
        temp_rect.x += x_offset
        return any(tile.rect.colliderect(temp_rect) for tile in self.map.get_colliding_tiles(temp_rect))
    
    def hit(self):
        """
        Handles the player being hit, reducing health and printing a message.
        """

        self.health -= 20
        # print("Oh i got Hit") # For debugging purpose
        # print(self.health) # For debugging purpose

    def change_speed_x(self, amount):
        self.speed = amount

    def change_speed_y(self, amount):
        self.jump_speed = amount

    def update_points(self, amount):
        self.score += amount