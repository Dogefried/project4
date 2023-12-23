import pygame
 
from pygame.sprite import Sprite
 
class Ship(Sprite):
    """飞船类"""
 
    def __init__(self, ai_game):
        """初始化飞船参数"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # 加载飞船图片并且获得飞船rect.
        self.image = pygame.image.load('./images/ship.bmp')
        self.rect = self.image.get_rect()

        # 初始化飞船位置为中间底部.
        self.rect.midbottom = self.screen_rect.midbottom

        # 飞船水平值.
        self.x = float(self.rect.x)

        # 移动标识
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """跟新飞船位置"""
        # 跟新飞船水平参数.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # 跟新飞船rect参数.
        self.rect.x = self.x

    def blitme(self):
        """在屏幕打印飞船"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """将飞船放到中间底部"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
