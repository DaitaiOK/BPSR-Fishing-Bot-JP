import time
from abc import ABC, abstractmethod
from ..bot_component import BotComponent

class BotState(BotComponent, ABC):
    def __init__(self, bot):
        super().__init__(bot)
        self.level_check_interceptor = bot.level_check_interceptor
        # ステートに進入した時刻を記録する変数
        self.state_entry_time = 0

    def reset_timer(self):
        """タイマーを現在時刻でリセット（アクション成功時などに使用）"""
        self.state_entry_time = time.time()

    def get_elapsed_time(self):
        """ステート開始（またはリセット）からの経過秒数を取得"""
        if self.state_entry_time == 0:
            return 0
        return time.time() - self.state_entry_time

    @abstractmethod
    def handle(self, screen):
        """
        各ステートのメインロジック。
        各クラスで self.get_elapsed_time() をチェックし、
        設定値を超えたら次の StateType を return するように実装する。
        """
        pass