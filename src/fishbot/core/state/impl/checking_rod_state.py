import time
from ..bot_state import BotState
from ..state_type import StateType

class CheckingRodState(BotState):
    """
    竿の状態を確認し、壊れていればメニューを開いて交換するステート。
    交換に成功（broken_rodが消失）するまでこのステートを維持し、
    正常が確認された場合のみ CASTING_BAIT へ移行する。
    """

    def handle(self, screen):
        self.bot.log("[CHECKING_ROD] 🛠️ 竿の状態を確認中...")
        # 画面が安定するまで少し待機（爆速仕様 0.3s）
        time.sleep(0.3)

        # 1. 壊れた竿のアイコン(broken_rod)を検知
        if self.detector.find(screen, "broken_rod"):
            self.bot.log("[CHECKING_ROD] ⚠️ 竿が壊れています！交換を実行します...")
            self.bot.stats.increment('rod_breaks')
            time.sleep(0.5)

            # 2. メニューを開く ('m'キー)
            self.controller.press_key('m')
            time.sleep(1.5) # メニューが開くアニメーション待ち

            # 3. 指定座標 (1650, 580) をクリックして竿を交換
            self.bot.log("[CHECKING_ROD] 🖱️ 交換ボタンをクリック...")
            self.controller.click_at(1650, 580)
            
            # 交換反映・アニメーション待ち
            time.sleep(1.5)
            self.bot.log("[CHECKING_ROD] 🔄 交換処理を試行しました。再確認のためステートを維持します。")
            
            # 【重要】再度自分自身を返し、正常になるまでループさせる
            return StateType.CHECKING_ROD
        
        else:
            # 2. 壊れていない、もしくは交換が成功してアイコンが消えた場合
            self.bot.log("[CHECKING_ROD] ✅ 竿の状態は正常です。キャストへ移行します。")
            # 待機なしで即座に移行
            return StateType.CASTING_BAIT