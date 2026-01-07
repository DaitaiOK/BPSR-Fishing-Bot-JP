import time
import sys
from src.fishbot.core.fishing_bot import FishingBot
from src.fishbot.core.game.hotkeys import Hotkeys
from src.fishbot.utils.logger import log

def main():
    bot = FishingBot()
    hotkeys = Hotkeys(bot)
    bot.start()

    log("[INFO] ========================================")
    log("[INFO]   FishBot Standby Mode")
    log("[INFO]   7: Start/Resume | 8: Pause | 0: Exit")
    log("[INFO] ========================================")

    try:
        # 0キーが押されて bot.stop() が呼ばれるまで回り続ける
        while not bot.is_stopped():
            if not hotkeys.paused:
                bot.update()
            else:
                # 一時停止中はスリープを入れて待機負荷を下げる
                time.sleep(0.5)

            # メインループの最小間隔
            time.sleep(0.01)

    except KeyboardInterrupt:
        log("[INFO] KeyboardInterrupt detected.")

    log("[INFO] Cleaning up and exiting...")
    sys.exit(0)

if __name__ == "__main__":
    main()