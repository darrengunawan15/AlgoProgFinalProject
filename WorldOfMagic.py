import pygame
import sys
from player import Player
from enemy import Enemy
from map import Map
from camera import Camera
from item import Item
from scoreboard import Scoreboard, ReplayButton, VictoryScreen

# Variables
WIDTH = 1024
HEIGHT = 576

class WorldOfMagic():
    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('World Of Magic')

        self.map = Map(self.screen, "assets\levels\level-1.tmx")

        self.camera = Camera(self.map.tmx_map.width * self.map.block_size,
                             self.map.tmx_map.height * self.map.block_size)
                             
        self.player = Player(self.screen, self.camera)

        self.scoreboard = Scoreboard(self.player)
        self.replay_button = ReplayButton(WIDTH, HEIGHT)
        self.victory_screen = VictoryScreen(self.screen, self)

    def run(self):
        items = pygame.sprite.Group()
        enemies = pygame.sprite.Group()

        # Items
        self.item1 = Item(self.screen, self.map, self.camera, 1960, 190, "sneakers.png", 2345, items, self) # Boost
        self.item2 = Item(self.screen, self.map, self.camera, 1960, 1590, "stars.png", 521, items, self)
        self.item3 = Item(self.screen, self.map, self.camera, 1100, 920, "shovel.png", 394, items, self)
        self.item4 = Item(self.screen, self.map, self.camera, 1100, 1140, "jetpack.png", 1234, items, self) # Jetpack
        self.item5 = Item(self.screen, self.map, self.camera, 30, 490, "clownhorn.png", 241, items, self)
        self.item6 = Item(self.screen, self.map, self.camera, 890, 830, "portal.png", 3456, items, self) # Portal
        items.add(self.item1, self.item2, self.item3, self.item4, self.item5, self.item6)

        # Enemies
        self.enemy1 = Enemy(self.map, 1200, 200, enemies)
        self.enemy2 = Enemy(self.map, 1700, 200, enemies)
        self.enemy3 = Enemy(self.map, 100, 520, enemies)
        self.enemy4 = Enemy(self.map, 400, 520, enemies)
        self.enemy5 = Enemy(self.map, 700, 520, enemies)
        self.enemy6 = Enemy(self.map, 1700, 200, enemies)
        enemies.add(self.enemy1, self.enemy2, self.enemy3, self.enemy4, self.enemy5)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif self.replay_button.check_click(event):
                    self.reset()
                    self.replay_button.visible = False

            # Game background
            self.screen.fill((3, 0, 46))

            # Set camera to always follow player
            self.camera.update(self.player, self.screen.get_width(), self.screen.get_height())

            # Rendering the player and all map tiles on the game screen and camera's position for proper positioning and scrolling.            
            for sprite in [self.player] + self.map.tiles_group.sprites():
                self.screen.blit(sprite.image, self.camera.apply(sprite))

            self.player.move()
            self.player.update(self.map)

            for enemy in enemies.sprites():
                enemy.draw(self.screen, self.camera)
                enemy.update(self.player)

            for item in items.sprites():
                item.draw()
                item.update(self.player)

            self.scoreboard.draw(self.screen)
            self.scoreboard.update()

            # Check for game over
            if self.player.health <= 0:
                self.screen.fill((0, 0, 0))
                self.replay_button.visible = True
            else:
                self.replay_button.visible = False

            # Update and draw the replay button
            self.replay_button.update()
            self.replay_button.draw(self.screen)

            pygame.display.update()
            pygame.time.Clock().tick(60)

    def show_victory_screen(self):
        if self.player.score >= 624:
            self.victory_screen.show("VICTORY! You meet the profit quota!")
        else:
            self.victory_screen.show("YOU ARE FIRED! You did not meet the profit quota!")

    def reset(self):
        pygame.quit()
        WorldOfMagic().run()

WorldOfMagic().run()