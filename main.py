import sys
import tkinter
import pyautogui
import time
import traceback
from pynput.mouse import Listener, Button
import threading
import json


# Fail-Safe機能を有効にする
pyautogui.FAILSAFE = True

root = tkinter.Tk()
root.title("ChatGPT 自動送信ツール")
root.geometry("400x300")  # Set the window size to 400 pixels wide and 300 pixels tall

# グローバル変数の初期化
listener_thread = None
listener_running = False
saved_input_box_x = 0
saved_input_box_y = 0
saved_send_button_x = 0
saved_send_button_y = 0
running = False
process_thread = None

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
        root.after(0, lambda: input_box_coordinates_label.config(text=f"X: {x}, Y: {y}"))
        global saved_input_box_x, saved_input_box_y
        saved_input_box_x = x
        saved_input_box_y = y
    if pressed and button == Button.right:
        input_box_coordinates_button.config(text='入力欄座標取得')
        listener_running = False

def start_listener_for_input_bot():
    with Listener(on_click=on_input_box_coordinates_button_click) as listener:
        listener.join()

def input_box_coordinates_start_button():
    global listener_thread, listener_running
    if not listener_running:
        input_box_coordinates_button.config(text='クリックして入力欄座標取得してください。右クリックで終了します。')
        listener_running = True
        listener_thread = threading.Thread(target=start_listener_for_input_bot)
        listener_thread.start()

def on_send_button_coordinates_button_click(x, y, button, pressed):
    global listener_running
    if not listener_running:
        return False
    if pressed and button == Button.left:
        # print(f"Mouse clicked at ({x}, {y})")
        # メインスレッドでラベルを更新する　理由:Tkinterがシングルスレッドで動作するGUIフレームワークであるため
        # 詳細：pynput ライブラリのリスナーは別スレッドで動作しているため、
        # 直接GUIを更新することはスレッドの安全性に反します。
        # root.after を使用することで、スレッド間の競合を避けつつ、メインスレッドにGUIの更新をスケジュールすることができます。
        root.after(0, lambda: send_button_coordinates_label.config(text=f"X: {x}, Y: {y}"))
        global saved_send_button_x, saved_send_button_y
        saved_send_button_x = x
        saved_send_button_y = y
    if pressed and button == Button.right:
        send_button_coordinates_button.config(text='送信ボタン座標取得')
        listener_running = False

def start_listener_for_send_button():
    with Listener(on_click=on_send_button_coordinates_button_click) as listener:
        listener.join()

def send_button_coordinates_start_button():
    global listener_thread, listener_running
    if not listener_running:
        send_button_coordinates_button.config(text='クリックして入力欄座標取得してください。右クリックで終了します。')
        listener_running = True
        listener_thread = threading.Thread(target=start_listener_for_send_button)
        listener_thread.start()

def start_function():
    try:
        global running
        running = True
        while running:
            # 入力された待ち時間を取得
            wait_time = int(wait_time_entry.get())
            print(f"回答が書き終わるのを{wait_time}秒待っています。")
            
            # wait_time秒待つ代わりに、0.1秒ごとにrunningを確認
            for _ in range(int(wait_time * 10)):
                if not running:
                    return
                time.sleep(0.1)

            # 以下の処理はrunningがTrueの場合にのみ実行
            if running:
                # 保存された座標を使用してテキスト入力欄にクリック
                pyautogui.click(saved_input_box_x, saved_input_box_y)
                print(f"Mouse clicked at ({saved_input_box_x}, {saved_input_box_y})")
                # ChatGPTの入力欄に「続きを書いてください。」と入力
                pyautogui.write('Continue generating in Japanese.', interval=0.05)
                print("続きを書いてください。を入力しました。")

            # 'Continue generating in Japanese.'を書き終えた後もスタートボタン処理がrunningかどうかを確認
            if not running:
                return

            if running:
                # 送信ボタンの座標を使用してクリック
                pyautogui.click(saved_send_button_x, saved_send_button_y)
    except ValueError:
        print("無効な待ち時間が入力されました。数値を入力してください。")
    except Exception as e:
        traceback.print_exc()  # 例外の詳細を出力

def start_thread():
    """スタートボタンのスレッドを開始する関数。"""
    global process_thread
    process_thread = threading.Thread(target=start_function)
    process_thread.start()

def stop_function():
    # ストップボタンの機能
    global running
    running = False
    if process_thread is not None:
        process_thread.join()
    print("処理を停止しました。")

# 設定の保存に使用するファイル名
CONFIG_FILENAME = 'config.json'

# 設定をJSONファイルに保存する関数
def save_configuration():
    config_data = {
        'input_box': {
            'x': saved_input_box_x,
            'y': saved_input_box_y
        },
        'send_button': {
            'x': saved_send_button_x,
            'y': saved_send_button_y
        },
        'wait_time': wait_time_entry.get()  # ユーザー入力の待ち時間
    }
    with open(CONFIG_FILENAME, 'w') as config_file:
        json.dump(config_data, config_file, indent=4)
    print("設定を保存しました。")

# 設定を読み込む関数
def load_configuration():
    try:
        with open(CONFIG_FILENAME, 'r') as config_file:
            config_data = json.load(config_file)
            global saved_input_box_x, saved_input_box_y, saved_send_button_x, saved_send_button_y
            saved_input_box_x = config_data['input_box']['x']
            saved_input_box_y = config_data['input_box']['y']
            saved_send_button_x = config_data['send_button']['x']
            saved_send_button_y = config_data['send_button']['y']
            # ラベルを更新する
            input_box_coordinates_label.config(text=f"入力欄：X: {saved_input_box_x}, Y: {saved_input_box_y}")
            send_button_coordinates_label.config(text=f"送信ボタン：X: {saved_send_button_x}, Y: {saved_send_button_y}")
            wait_time_entry.delete(0, tkinter.END)
            wait_time_entry.insert(0, config_data['wait_time'])
            print("設定を読み込みました。")
    except FileNotFoundError:
        print("設定ファイルが見つかりません。デフォルト値を使用します。")
    except json.JSONDecodeError:
        print("設定ファイルが破損しています。デフォルト値を使用します。")



input_box_coordinates_label = tkinter.Label(root, text="入力欄：X: 0, Y: 0")
input_box_coordinates_label.pack()

input_box_coordinates_button = tkinter.Button(root, text="メッセージボックス座標取得", command=input_box_coordinates_start_button)
input_box_coordinates_button.pack()

send_button_coordinates_label = tkinter.Label(root, text="送信ボタン：X: 0, Y: 0")
send_button_coordinates_label.pack()

send_button_coordinates_button = tkinter.Button(root, text="送信ボタン座標取得", command=send_button_coordinates_start_button)
send_button_coordinates_button.pack()

# 応答待ち時間入力フィールドとラベルを追加
wait_time_label = tkinter.Label(root, text="応答待ち時間（秒）:")
wait_time_label.pack()
wait_time_entry = tkinter.Entry(root)
wait_time_entry.pack()

# 設定保存ボタンの追加
save_button = tkinter.Button(root, text="設定保存", command=save_configuration)
save_button.pack()

start_button = tkinter.Button(root, text="Start", command=start_thread)
start_button.pack()

stop_button = tkinter.Button(root, text="Stop", command=stop_function)
stop_button.pack()

# プログラム起動時に設定を読み込む
load_configuration()

root.mainloop()
