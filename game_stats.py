class GameStats:
    """统计数据"""
    
    def __init__(self, ai_game):
        """初始化"""
        self.settings = ai_game.settings
        self.reset_stats()

        # 默认为非活动.
        self.game_active = False

        # 设置一个历史最高分.
        self.high_score = 0
        
    def reset_stats(self):
        """初始化用于统计的属性"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1