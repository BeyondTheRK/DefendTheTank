class GameStats():
    """Track stats for Alien Invasion."""

    def __init__(self, ai_settings):
        """init stats."""
        self.ai_settings = ai_settings
        self.reset_stats()
        
        #high score never reset
        self.high_score = 0
        
        #start alien invasion in active state
        self.game_active = False

    def reset_stats(self):
        """init stats that change during game"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
