import sys
import tkinter
import pyautogui
import time
from pynput import keyboard
import threading

def on_press(key):
    if key == keyboard.Key.esc:
        # ESCキーが押されたらプログラムを終了
        print("ESCキーが押されたため、プログラムを終了します。")
        root.destroy()
        return False  # キーボードリスナーを停止

def start_listener():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

# 別スレッドでtkinterと処理が衝突しないようにキーボードリスナーを開始
listener_thread = threading.Thread(target=start_listener)
listener_thread.start()

root = tkinter.Tk()
root.title("ChatGPT 自動送信ツール")
root.geometry("400x300")  # Set the window size to 400 pixels wide and 300 pixels tall

# マウスを画面の左上隅に移動させることで緊急停止できるようにする
# pyautogui.FAILSAFE = True

# # マウスカーソルを画面中央に移動
# pyautogui.moveTo(pyautogui.size().width / 2, pyautogui.size().height / 2)

# # 少し待つ
# time.sleep(2)

# # マウスカーソルを右に100ピクセル、下に100ピクセル移動
# pyautogui.moveRel(100, 100, duration=1)

# # # テキストを入力（実際のテキストエディタなどにフォーカスが合っている必要があります）
# # pyautogui.write('Hello, PyAutoGUI!', interval=0.25)

# # メッセージボックスを表示
# pyautogui.alert('PyAutoGUI test complete!')

# マウスを画面の左上隅に移動させることで緊急停止できるようにする
pyautogui.FAILSAFE = True

def start_function():
    # スタートボタンの機能
    # マウスカーソルを画面中央に移動
    pyautogui.moveTo(pyautogui.size().width / 2, pyautogui.size().height / 2)

    # 少し待つ
    time.sleep(2)

    # マウスカーソルを右に100ピクセル、下に100ピクセル移動
    pyautogui.moveRel(100, 100, duration=1)

    # # テキストを入力（実際のテキストエディタなどにフォーカスが合っている必要があります）
    # pyautogui.write('Hello, PyAutoGUI!', interval=0.25)

    # メッセージボックスを表示
    pyautogui.alert('PyAutoGUI test complete!')
    pass

def stop_function():
    # ストップボタンの機能
    pass

def resume_function():
    # 再開ボタンの機能
    pass


start_button = tkinter.Button(root, text="Start", command=start_function)
stop_button = tkinter.Button(root, text="Stop", command=stop_function)
resume_button = tkinter.Button(root, text="Resume", command=resume_function)

start_button.pack()
stop_button.pack()
resume_button.pack()
root.mainloop()

listener.join()
