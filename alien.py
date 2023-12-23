import pygame
from pygame.sprite import Sprite
 
class Alien(Sprite):
    """外星人类"""

    def __init__(self, ai_game):
        """初始化外星人"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # 加载外星人图片，设置rect参数.
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # 每个外星人初始放在屏幕左上角.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 浮点存放水平位置.
        self.x = float(self.rect.x)

    def check_edges(self):
        """检查是否到达边界"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """移动外星人"""
        self.x += (self.settings.alien_speed *
                        self.settings.fleet_direction)
        self.rect.x = self.x
