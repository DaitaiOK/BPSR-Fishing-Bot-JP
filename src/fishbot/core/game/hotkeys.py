import keyboard
import multiprocessing
import sys
from src.fishbot.utils.logger import log
from src.fishbot.utils.roi_visualizer import main as show_roi_visualizer

class Hotkeys:
    def __init__(self, bot):
        self.bot = bot
        self.paused = True
        self.visualizer_process = None
        self._register_hotkeys()

    def _register_hotkeys(self):
        # 7: 開始 / 再開
        keyboard.add_hotkey('7', self._resume)
        # 8: 一時停止 (プログラムは終了せず待機状態へ)
        keyboard.add_hotkey('8', self._pause)
        # 9: ROI Visualizer
        keyboard.add_hotkey('9', self._toggle_visualizer)
        # 0: 完全終了 (bot.stopを呼びmainループを抜けさせる)
        keyboard.add_hotkey('0', self._stop)
        
        log("[INFO] ✅ Hotkeys: '7'(Start/Resume), '8'(Pause/Menu), '0'(Exit), '9'(Visualizer)")

    def _resume(self):
        if self.paused:
            self.paused = False
            log("[HOTKEY] Bot RUNNING.")

    def _pause(self):
        if not self.paused:
            self.paused = True
            log("[HOTKEY] Bot PAUSED. Returning to Standby Mode...")

    def _stop(self):
        log("[HOTKEY] Shutting down the application...")
        # ROI Visualizerの停止
        if self.visualizer_process and self.visualizer_process.is_alive():
            self.visualizer_process.terminate()
        
        # Botのループフラグを停止にセット
        self.bot.stop()

    def _toggle_visualizer(self):
        if self.visualizer_process and self.visualizer_process.is_alive():
            log("[HOTKEY] Closing the ROI visualizer.")
            self.visualizer_process.terminate()
            self.visualizer_process = None
        else:
            log("[HOTKEY] Opening the ROI visualizer.")
            self.visualizer_process = multiprocessing.Process(target=show_roi_visualizer, daemon=True)
            self.visualizer_process.start()

    def wait_for_exit(self):
        """0キーが押されるまでブロックする"""
        keyboard.wait('0')