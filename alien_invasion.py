import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """整体类管理游戏资产和行为"""

    def __init__(self):
        """初始化游戏，创建游戏资源"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # 创建一个实例来存储游戏统计数据,并创建一个记分牌。
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # 点击开始按钮.
        self.play_button = Button(self, "Play")

    def run_game(self):
        """启动游戏的主循环."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        """响应按键和鼠标事件."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """当玩家点击Play时开始一个新游戏"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # 重置游戏设置.
            self.settings.initialize_dynamic_settings()

            # 重置游戏统计数据.
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            #清除所有残留的外星人和子弹.
            self.aliens.empty()
            self.bullets.empty()
            
            # 创建一个新的舰队和中心的船。
            self._create_fleet()
            self.ship.center_ship()

            #隐藏鼠标光标r.
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """响应按键"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """响应按键释放。"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """创建一个新的子弹并将其添加到子弹组。"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """更新子弹位置，清除旧子弹。"""
        # 更新子弹位置.
        self.bullets.update()

        # 处理掉已经消失的子弹.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                 self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """应对子弹与外星人的碰撞。"""
        # 移除所有碰撞的子弹和外星人.
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # 摧毁现有的子弹，创造新的舰队
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # 提升等级
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """
        检查舰队是否在边缘，
然后更新舰队中所有外星人的位置。
        """
        self._check_fleet_edges()
        self.aliens.update()

        # 寻找外星飞船碰撞。
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # 寻找撞击屏幕底部的外星人.
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # 飞船撞击
                self._ship_hit()
                break

    def _ship_hit(self):
        """对飞船被外星人袭击做出反应."""
        if self.stats.ships_left > 0:
            #减小飞船数量，跟新记分板.
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            
            # 清空存在的外星人和子弹.
            self.aliens.empty()
            self.bullets.empty()
            
            # 创建一组新外星人舰队.
            self._create_fleet()
            self.ship.center_ship()
            
            # 暂停.
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _create_fleet(self):
        """创建外星人舰队"""
        # 创建一行外星人舰队，并记录一行数量.
        # 两个外星人之间的距离为一个外星人.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        
        # 计算应该有多少行.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                                (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        
        # 创建完整外星人舰队.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """创建外星人并定义它的位置"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """检查外星人是否到达便捷"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
            
    def _change_fleet_direction(self):
        """将外星人向下移动同时改变左右方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """更新屏幕"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # 显示得分信息.
        self.sb.show_score()

        # 游戏未开始时显示开始按钮.
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    # 创建游戏实例，开始游戏.
    ai = AlienInvasion()
    ai.run_game()
