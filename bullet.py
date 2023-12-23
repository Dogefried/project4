import pygame
from pygame.sprite import Sprite
 
class Bullet(Sprite):
    """子弹类"""

    def __init__(self, ai_game):
        """从飞船头创建子弹"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # 创建rect，并移到合适位置.
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
            self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop
        
        # 浮点数存放子弹水平位置.
        self.y = float(self.rect.y)

    def update(self):
        """子弹上移"""
        # 跟新子弹坐标.
        self.y -= self.settings.bullet_speed
        # 跟新rect位置.
        self.rect.y = self.y

    def draw_bullet(self):
        """在屏幕上显示子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)
