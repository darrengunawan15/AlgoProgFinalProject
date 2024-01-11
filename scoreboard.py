import pygame
import os
import sys

class Scoreboard(pygame.sprite.Sprite):
    def __init__(self, player):
        """
        Initializes a Scoreboard object for displaying player-related information on the screen.

        Parameters:
        - player (Player): The player object associated with the scoreboard.
        """
        
        super().__init__()
        self.player = player
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 24)

    def draw(self, screen):
        """
        Draws the scoreboard on the specified screen.

        Parameters:
        - screen (pygame.Surface): The surface where the scoreboard will be drawn.
        """

        scoreboard_text = self.font.render(f"Profit Quota: {self.player.score} / 624", True, (255, 255, 255))
        screen.blit(scoreboard_text, (10, 10))

        health_text = self.font.render(f"Health: {self.player.health}", True, (255, 255, 255))
        screen.blit(health_text, (10, 40))

class ReplayButton(pygame.sprite.Sprite):
    def __init__(self, width, height):
        """
        Initializes a ReplayButton object for handling replay button functionality.

        Parameters:
        - width (int): The width of the game window.
        - height (int): The height of the game window.
        """
        super().__init__()

        self.parent_path = "assets/buttons/"
        self.image = pygame.image.load(os.path.join(self.parent_path, "replay_button.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height // 2)
        self.visible = True

    def draw(self, screen):
        """
        Draws the replay button on the specified screen.

        Parameters:
        - screen (pygame.Surface): The surface where the replay button will be drawn.
        """
        if self.visible:
            screen.blit(self.image, self.rect)

    def check_click(self, event):
        """
        Checks if the replay button is clicked.

        Parameters:
        - event (pygame.event.Event): The pygame event object to check for mouse clicks.

        Returns:
        - bool: True if the replay button is clicked, False otherwise.
        """

        if self.visible and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                return True
        return False

class VictoryScreen:
    def __init__(self, screen, game_instance):
        """
        Initializes a VictoryScreen object for displaying victory-related content.

        Parameters:
        - screen (pygame.Surface): The surface where the victory screen will be displayed.
        - game_instance: An instance of the game class associated with the victory screen.
        """

        self.screen = screen
        self.game_instance = game_instance

    def show(self, text):
        """
        Displays the victory screen with the specified text and waits for user input.

        Parameters:
        - text (str): The text to be displayed on the victory screen.
        """

        # Display victory-related content
        font = pygame.font.Font(None, 36)
        text = font.render(text, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))

        # Display the victory screen
        self.screen.fill((0, 0, 0))
        self.screen.blit(text, text_rect)
        pygame.display.flip()

        # Wait for user input to continue or exit
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self.game_instance.reset()
