import pygame

class Camera:
    def __init__(self, width, height):
        """
        Initializes a camera object with a specified width and height.

        Parameters:
        - width (int): The width of the camera view.
        - height (int): The height of the camera view.
        """

        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, target):
        """
        Applies the camera transformation to a target object.

        Parameters:
        - target (pygame.sprite.Sprite): The target object to be transformed.

        Returns:
        - pygame.Rect: The transformed rectangle of the target within the camera view.
        """

        return target.rect.move(self.camera.topleft)

    def update(self, target, width, height):
        """
        Updates the camera position based on the position of the target and limits scrolling to the size of the map.

        Parameters:
        - target (pygame.sprite.Sprite): The target object that the camera should follow.
        - width (int): The width of the game window or map.
        - height (int): The height of the game window or map.
        """

        x = -target.rect.x + width // 2
        y = -target.rect.y + height // 2

        # Limit scrolling to the size of the map
        x = min(0, x)  # Left
        y = min(0, y)  # Top
        x = max(-(self.width - width), x)  # Right
        y = max(-(self.height - height), y)  # Bottom

        self.camera = pygame.Rect(x, y, self.width, self.height)