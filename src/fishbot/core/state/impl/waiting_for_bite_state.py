import time
from ..bot_state import BotState
from ..state_type import StateType

class WaitingForBiteState(BotState):
    def __init__(self, bot):
        super().__init__(bot)

    def handle(self, screen):
        # --- 個別タイムアウト判定 (1分 = 60秒) ---
        # 60秒経過してもアタリがない場合は、一度仕切り直すために最初（竿チェック）へ戻る
        if self.get_elapsed_time() > 60:
            self.bot.log("[TIMEOUT] ⚠️ アタリを検知できないまま1分経過しました。")
            self.bot.log("[TIMEOUT] 🔄 仕切り直すため CHECKING_ROD へ戻ります。")
            
            # 念のためマウスボタンを離しておく
            self.controller.mouse_up('left')
            
            return StateType.CHECKING_ROD
        # -------------------------------------

        # ❗(アタリ)を検知
        if self.detector.find(screen, "exclamation"):
            self.bot.log("[WAITING_FOR_BITE] ❗ Fish hooked! 自動釣り上げを開始します。")
            
            # 魚を掛けるために左クリックを長押し
            self.controller.mouse_down('left')
            
            return StateType.PLAYING_MINIGAME

        # ❗がない間は、キャストされた浮きを見守る（ループ継続）
        return StateType.WAITING_FOR_BITE