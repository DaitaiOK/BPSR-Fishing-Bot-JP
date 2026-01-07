import time
from ..bot_state import BotState
from ..state_type import StateType

class FinishingState(BotState):
    def handle(self, screen):
        # --- 個別タイムアウト判定 (7秒) ---
        # 続行ボタンが見つからないまま7秒経過したら、強制的に竿チェックへ戻る
        if self.get_elapsed_time() > 7:
            self.bot.log("[TIMEOUT] ⚠️ 続行ボタンを検知できません。強制的に CHECKING_ROD へ移行します。")
            return StateType.CHECKING_ROD
        # -------------------------------

        # 画像検知
        btn_pos = self.detector.find(screen, "continue")
        
        if btn_pos:
            # ログで今からどこを押すか正確に表示させる
            self.bot.log(f"[FINISHING] ✨ 続行ボタン検知！ターゲット: ({btn_pos[0]}, {btn_pos[1]})")
            
            # キャストができるなら移動(move_to)は動くはず。まず移動させる。
            self.controller.move_to(btn_pos[0], btn_pos[1])
            time.sleep(0.5) 
            
            # click_at(x, y) で確実に座標を指定してクリック
            self.controller.click_at(btn_pos[0], btn_pos[1])
            
            self.bot.log("[FINISHING] 🖱️ クリック実行完了")
            
            # クリック後の画面遷移待ち
            time.sleep(2.0)
            return StateType.CHECKING_ROD

        # ボタンがない間はステートを維持（ループ継続）
        return StateType.FINISHING