import time
from ..bot_state import BotState
from ..state_type import StateType

class PlayingMinigameState(BotState):
    def __init__(self, bot):
        super().__init__(bot)
        self._current_direction = None
        self._last_action_time = 0
        self.action_cooldown = 0.2 

    def _handle_arrow(self, direction, screen):
        arrow_template = f"{direction}_arrow"
        key_to_press = 'a' if direction == 'left' else 'd'
        key_to_release = 'd' if direction == 'left' else 'a'
        opposite_direction = 'right' if direction == 'left' else 'left'

        if time.time() - self._last_action_time < self.action_cooldown:
            return

        if self.detector.find(screen, arrow_template):
            if self._current_direction is None:
                self.bot.log(f"[MINIGAME] ▶️ {direction}")
                self.controller.key_down(key_to_press)
                self._current_direction = direction
                self._last_action_time = time.time()
            elif self._current_direction == opposite_direction:
                self.bot.log(f"[MINIGAME] ◀️ {direction}に切り替え")
                self.controller.key_up(key_to_release)
                self._current_direction = None
                self._last_action_time = time.time()

    def handle(self, screen):
        # --- 個別タイムアウト判定 (35秒) ---
        # ミニゲームが長引いた場合、強制的にリザルト確認へ移行
        if self.get_elapsed_time() > 35:
            self.bot.log("[TIMEOUT] ⚠️ ミニゲームが35秒を超過しました。強制終了します。")
            self._exit_minigame()
            return StateType.FINISHING
        # -------------------------------

        # 成功時：リザルト画面クリック処理へ
        if self.detector.find(screen, "success"):
            self.bot.log("[MINIGAME] 🐟 Success! リザルト処理(FINISHING)へ。")
            self._exit_minigame()
            return StateType.FINISHING
        
        # 失敗時：竿の状態を確認してから投げ直しへ
        if self.detector.find(screen, "failed"):
            self.bot.log("[MINIGAME] ❌ 失敗。竿をチェックして投げ直します。")
            self._exit_minigame()
            return StateType.CHECKING_ROD

        self._handle_arrow('left', screen)
        self._handle_arrow('right', screen)
        return StateType.PLAYING_MINIGAME

    def _exit_minigame(self):
        """ミニゲーム終了時のクリーンアップ処理"""
        self.controller.release_all_controls()
        self._current_direction = None
        # 操作終了後の短いディレイ
        time.sleep(0.5)