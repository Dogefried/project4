import pygame.font
 
class Button:
 
    def __init__(self, ai_game, msg):
        """初始化按钮参数"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        
        # 设置按钮以及字体参数.
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        
        # 创建按钮rect并且将位置设置为中心.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        
        # 按钮消息只需要准备一次.
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """将消息渲染为图片，然后设置位置"""
        self.msg_image = self.font.render(msg, True, self.text_color,
                self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # 在屏幕显示按钮和文字.
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)