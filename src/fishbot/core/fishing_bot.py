import time
from src.fishbot.config import Config
from src.fishbot.core.game.controller import GameController
from src.fishbot.core.game.detector import Detector
from src.fishbot.core.state.impl.finishing_state import FinishingState
from src.fishbot.core.state.impl.checking_rod_state import CheckingRodState
from src.fishbot.core.state.impl.casting_bait_state import CastingBaitState
from src.fishbot.core.state.impl.playing_minigame_state import PlayingMinigameState
from src.fishbot.core.state.impl.waiting_for_bite_state import WaitingForBiteState
from src.fishbot.core.state.state_machine import StateMachine
from src.fishbot.core.state.state_type import StateType
from src.fishbot.core.stats import StatsTracker
from src.fishbot.utils.logger import log
from src.fishbot.core.interceptors.level_check_interceptor import LevelCheckInterceptor

class FishingBot:
    def __init__(self):
        self.config = Config()
        self.stats = StatsTracker()
        self.log = log

        self.detector = Detector(self.config)
        self.controller = GameController(self.config)
        self.state_machine = StateMachine(self)

        self.level_check_interceptor = LevelCheckInterceptor(self)

        self._stopped = False
        self.debug_mode = self.config.bot.debug_mode

        self.target_delay = 0
        if self.config.bot.target_fps > 0:
            self.target_delay = 1.0 / self.config.bot.target_fps

        self._register_states()

    def _register_states(self):
        # すべてのステートを登録し、フルオートループを有効化
        self.state_machine.add_state(StateType.WAITING_FOR_BITE, WaitingForBiteState(self))
        self.state_machine.add_state(StateType.PLAYING_MINIGAME, PlayingMinigameState(self))
        self.state_machine.add_state(StateType.FINISHING, FinishingState(self))
        self.state_machine.add_state(StateType.CHECKING_ROD, CheckingRodState(self))
        self.state_machine.add_state(StateType.CASTING_BAIT, CastingBaitState(self))

    def start(self):
        # ログを全自動仕様に変更
        log("[INFO] 🎣 Full-Auto Bot Ready!")
        log("[INFO] 💡 竿の確認とキャストから全自動で開始します。")
        log(f"[INFO] ⚙️ Accuracy: {self.config.bot.detection.precision * 100:.0f}%")
        time.sleep(1)
        
        # 起動後、まず竿の状態を確認し、問題なければキャストするフローへ
        self.state_machine.set_state(StateType.CHECKING_ROD)

    def update(self):
        if self._stopped:
            return
        loop_start = time.time()
        screen = self.detector.capture_screen()
        self.state_machine.handle(screen)

        if self.target_delay > 0:
            loop_time = time.time() - loop_start
            sleep_time = max(0, self.target_delay - loop_time)
            if sleep_time > 0:
                time.sleep(sleep_time)

    def stop(self):
        if not getattr(self, "_stats_shown", False):
            self.stats.show()
            self._stats_shown = True
        if not self._stopped:
            self.log("[BOT] 🛑 Shutting down...")
            self._stopped = True
            self.controller.release_all_controls()

    def is_stopped(self):
        return self._stopped