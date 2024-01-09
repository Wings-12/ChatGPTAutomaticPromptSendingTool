import sys
import tkinter
import pyautogui
import time
import traceback
from pynput.mouse import Listener, Button
import threading


# Fail-Safe機能を有効にする
pyautogui.FAILSAFE = True

def exit_program():
    print("プログラムを終了します。")
    root.destroy()

root = tkinter.Tk()
root.title("ChatGPT 自動送信ツール")
root.geometry("400x300")  # Set the window size to 400 pixels wide and 300 pixels tall

# ラベルの初期化
coordinates_label = tkinter.Label(root, text="X: 0, Y: 0")
coordinates_label.pack()

# グローバル変数の初期化
listener_thread = None
listener_running = False
saved_input_box_x = 0
saved_input_box_y = 0
saved_send_button_x = 0
saved_send_button_y = 0

def on_input_box_coordinates_button_click(x, y, button, pressed):
    global listener_running
    if not listener_running:
        return False
    if pressed and button == Button.left:
        # print(f"Mouse clicked at ({x}, {y})")
        # メインスレッドでラベルを更新する　理由:Tkinterがシングルスレッドで動作するGUIフレームワークであるため
        # 詳細：pynput ライブラリのリスナーは別スレッドで動作しているため、
        # 直接GUIを更新することはスレッドの安全性に反します。
        # root.after を使用することで、スレッド間の競合を避けつつ、メインスレッドにGUIの更新をスケジュールすることができます。
        root.after(0, lambda: coordinates_label.config(text=f"X: {x}, Y: {y}"))
        global saved_input_box_x, saved_input_box_y
        saved_input_box_x = x
        saved_input_box_y = y
    if pressed and button == Button.right:
        input_box_coordinates_button.config(text='入力欄座標取得')
        listener_running = False

def start_listener():
    with Listener(on_click=on_input_box_coordinates_button_click) as listener:
        listener.join()

def toggle_input_box_coordinates_button():
    global listener_thread, listener_running
    if not listener_running:
        input_box_coordinates_button.config(text='クリックして入力欄座標取得してください。右クリックで終了します。')
        listener_running = True
        listener_thread = threading.Thread(target=start_listener)
        listener_thread.start()

def start_function():
    try:
        print("回答が書き終わるのを待っています。")
        time.sleep(3)  # 1秒ごとにチェック

        # 保存された座標を使用してテキスト入力欄にクリック
        # 後ほど修正：ざっくりとした座標を使用しているため、正確にクリックできない場合がある
        pyautogui.click(saved_input_box_x, saved_input_box_y)
        print(f"Mouse clicked at ({saved_input_box_x}, {saved_input_box_y})")
        # time.sleep(3)  # 1秒待機
        # ChatGPTの入力欄に「続きを書いてください。」と入力
        pyautogui.write('Continue generating in Japansese.', interval=0.05)
        print("続きを書いてください。を入力しました。")

        return  # ここでテスト終了
        
        # 送信ボタンの座標を使用してクリック
        pyautogui.click(saved_send_button_x, saved_send_button_y)
    except Exception as e:
        traceback.print_exc()  # 例外の詳細を出力

def stop_function():
    # ストップボタンの機能
    pass

def resume_function():
    # 再開ボタンの機能
    pass

input_box_coordinates_button = tkinter.Button(root, text="メッセージボックス座標取得", command=toggle_input_box_coordinates_button)
start_button = tkinter.Button(root, text="Start", command=start_function)
stop_button = tkinter.Button(root, text="Stop", command=stop_function)
resume_button = tkinter.Button(root, text="Resume", command=resume_function)

input_box_coordinates_button.pack()
start_button.pack()
stop_button.pack()
resume_button.pack()
root.mainloop()
