import pyautogui
import time

# Fail-Safe機能を有効にする
pyautogui.FAILSAFE = True

try:
    print("5秒後にマウスを動かします。プログラムを停止させるには、マウスを画面の左上隅に移動させてください。")
    time.sleep(5)  # 5秒間待機

    # マウスを画面中央に移動（Fail-Safeテストのため）
    pyautogui.moveTo(pyautogui.size().width / 2, pyautogui.size().height / 2, duration=1)

except pyautogui.FailSafeException:
    print("Fail-Safeによりプログラムが停止されました。")

print("プログラム終了")
