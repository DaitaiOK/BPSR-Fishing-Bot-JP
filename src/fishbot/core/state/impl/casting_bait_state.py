import time
from ..bot_state import BotState
from ..state_type import StateType

class CastingBaitState(BotState):
    def handle(self, screen):
        # --- 個別タイムアウト判定 (15秒) ---
        # 処理がスタックして15秒経過したら、強制的に次のステートへ
        if self.get_elapsed_time() > 15:
            self.bot.log("[TIMEOUT] ⚠️ Casting took too long. Forcing transition to WAITING_FOR_BITE.")
            return StateType.WAITING_FOR_BITE
        # -------------------------------

        # 設定された秒数（実質1秒）待機
        self.bot.log("[CASTING_BAIT] 🎣 1.0秒後にキャストを開始します")
        time.sleep(1)

        # 座標計算
        center_x = self.config.screen.monitor_width // 2 + self.config.screen.monitor_x
        center_y = self.config.screen.monitor_height // 2 + self.config.screen.monitor_y

        # マウス移動とフォーカスクリック
        self.bot.log(f"[CASTING_BAIT] 📍 Moving mouse to center ({center_x}, {center_y})")
        self.controller.move_to(center_x, center_y)
        time.sleep(0.1)
        self.controller.click_at(center_x, center_y)
        time.sleep(0.1)

        # 単押しキャスト
        self.bot.log("[CASTING_BAIT] 🎣 Casting bait...")
        self.controller.mouse_down('left')
        time.sleep(0.1)
        self.controller.mouse_up('left')
        
        # キャスト後の硬直待ち
        time.sleep(1)
        
        # 正常完了した場合はタイマーを意識せず次のステートへ
        return StateType.WAITING_FOR_BITE