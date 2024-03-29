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
inputBoxListenerThread = None
inputBoxListenerRunning = False
sendButtonListenerThread = None
sendButtonListenerRunning = False
inputBoxXCoordinate = 0
inputBoxYCoordinate = 0
sendButtonXCoordinate = 0
sendButtonYCoordinate = 0
isProcessRunning = False
automationThread = None
windowXPosition = 0
windowYPosition = 0

# TODO: ラベルの共通化
# input_box_coordinates_button_text = ''
# send_button_coordinates_button_text = ''
# wait_time_label_text = ''
# save_button_text = ''
# start_button_text = ''
# stop_button_text = ''
# topmost_switch_text = ''

# デフォルト設定値
DEFAULT_CONFIG = {
    "input_box": {
        "x": 0,  # デフォルトの入力欄のX座標
        "y": 0   # デフォルトの入力欄のY座標
    },
    "send_button": {
        "x": 0,  # デフォルトの送信ボタンのX座標
        "y": 0   # デフォルトの送信ボタンのY座標
    },
    "wait_time": 80,  # デフォルトの応答待ち時間（秒）
    "window_position": {
    "x": 230,  # デフォルトのウィンドウX座標
    "y": 125   # デフォルトのウィンドウY座標
    },
    "always_on_top": False,  # デフォルトの常に最前面に表示の設定
    "language": "Japanese",  # デフォルトの言語
}

# 言語設定用の変数と辞書
language_var = tkinter.StringVar(value="English")
language_settings = {
    "English": {
        "app_title": "ChatGPT Automation Tool",
        "input_box_coordinates_button_text": "Get Input Box Coordinates",
        "send_button_coordinates_button_text": "Get Send Button Coordinates",
        "wait_time_label_text": "Wait Time (seconds):",
        "save_button_text": "Save Settings",
        "start_button_text": "Start",
        "stop_button_text": "Stop",
        "topmost_switch_text": "Always on top",
    },
    "Japanese": {
        "app_title": "ChatGPT 自動送信ツール",
        "input_box_coordinates_button_text": "入力欄座標取得",
        "send_button_coordinates_button_text": "送信ボタン座標取得",
        "wait_time_label_text": "応答待ち時間（秒）:",
        "save_button_text": "設定保存",
        "start_button_text": "開始",
        "stop_button_text": "停止",
        "topmost_switch_text": "常に最前面に表示",
    }
}

def on_input_box_coordinates_button_click(x, y, button, pressed):
    global inputBoxListenerRunning
    if not inputBoxListenerRunning:
        return False
    if pressed and button == Button.left:
        # print(f"Mouse clicked at ({x}, {y})")
        # メインスレッドでラベルを更新する　理由:Tkinterがシングルスレッドで動作するGUIフレームワークであるため
        # 詳細：pynput ライブラリのリスナーは別スレッドで動作しているため、
        # 直接GUIを更新することはスレッドの安全性に反します。
        # root.after を使用することで、スレッド間の競合を避けつつ、メインスレッドにGUIの更新をスケジュールすることができます。

        # x,y座標の少数を切り捨てる
        x = int(x)
        y = int(y)

        root.after(0, lambda: input_box_coordinates_label.config(text=f"X: {x}, Y: {y}"))
        global inputBoxXCoordinate, inputBoxYCoordinate
        inputBoxXCoordinate = x
        inputBoxYCoordinate = y
    if pressed and button == Button.right:
        if language_var == "Japanese":
            input_box_coordinates_button.config(text="入力座標取得")
        else:
            input_box_coordinates_button.config(text="Get Input Box Coordinates")
        inputBoxListenerRunning = False

def start_listener_for_input_button():
    with Listener(on_click=on_input_box_coordinates_button_click) as listener:
        listener.join()

def input_box_coordinates_start_button():
    global inputBoxListenerThread, inputBoxListenerRunning
    if not inputBoxListenerRunning:
        if language_var.get() == "Japanese":  
            input_box_coordinates_button.config(text="クリックして入力欄座標取得してください。右クリックで保存します。")
        else:
            input_box_coordinates_button.config(text="Click to get the input box coordinates. Right click to save.")
        inputBoxListenerRunning = True
        inputBoxListenerThread = threading.Thread(target=start_listener_for_input_button)
        inputBoxListenerThread.start()

def on_send_button_coordinates_button_click(x, y, button, pressed):
    global sendButtonListenerRunning
    if not sendButtonListenerRunning:
        return False
    
    if pressed and button == Button.left:
        # print(f"Mouse clicked at ({x}, {y})")
        # メインスレッドでラベルを更新する　理由:Tkinterがシングルスレッドで動作するGUIフレームワークであるため
        # 詳細：pynput ライブラリのリスナーは別スレッドで動作しているため、
        # 直接GUIを更新することはスレッドの安全性に反します。
        # root.after を使用することで、スレッド間の競合を避けつつ、メインスレッドにGUIの更新をスケジュールすることができます。

        # x,y座標の少数を切り捨てる
        x = int(x)
        y = int(y)

        root.after(0, lambda: send_button_coordinates_label.config(text=f"X: {x}, Y: {y}"))
        global sendButtonXCoordinate, sendButtonYCoordinate
        sendButtonXCoordinate = x
        sendButtonYCoordinate = y
    if pressed and button == Button.right:
        if language_var.get() == "Japanese":  
            send_button_coordinates_button.config(text="送信ボタン座標取得")
        else:
            send_button_coordinates_button.config(text="Get Send Button Coordinates")
        sendButtonListenerRunning = False

def start_listener_for_send_button():
    with Listener(on_click=on_send_button_coordinates_button_click) as listener:
        listener.join()

def send_button_coordinates_start_button():
    global sendButtonListenerThread, sendButtonListenerRunning
    if not sendButtonListenerRunning:
        if language_var.get() == "Japanese":
            send_button_coordinates_button.config(text='クリックして入力欄座標取得してください。右クリックで保存します。')
        else:
            send_button_coordinates_button.config(text='Click to get the send button coordinates. Right click to save.')
        sendButtonListenerRunning = True
        sendButtonListenerThread = threading.Thread(target=start_listener_for_send_button)
        sendButtonListenerThread.start()

def start_function():
    try:
        global isProcessRunning
        isProcessRunning = True
        while isProcessRunning:

            # 以下の処理はisProcessRunningがTrueの場合にのみ実行
            if isProcessRunning:
                # 保存された座標を使用してテキスト入力欄にクリック
                pyautogui.click(inputBoxXCoordinate, inputBoxYCoordinate)
                # ChatGPTのウィンドウがアクティブになってない場合のためにもう一度クリック
                pyautogui.click(inputBoxXCoordinate, inputBoxYCoordinate)
                print(f"Mouse clicked at ({inputBoxXCoordinate}, {inputBoxYCoordinate})")
                # ChatGPTの入力欄に「続きを書いてください。」と入力
                pyautogui.write('Continue generating in Japanese. Please write in a format that can be pasted with copy code.', interval=0.05)
                print("続きを書いてください。を入力しました。")

            # 'Continue generating in Japanese.'を書き終えた後もスタートボタン処理がisProcessRunningかどうかを確認
            if not isProcessRunning:
                return

            if isProcessRunning:
                # 送信ボタンの座標を使用してクリック
                pyautogui.click(sendButtonXCoordinate, sendButtonYCoordinate)
            
            # 入力された待ち時間を取得
            wait_time = int(wait_time_entry.get())
            print(f"回答が書き終わるのを{wait_time}秒待っています。")
            
            # wait_time秒待つ代わりに、0.1秒ごとにisProcessRunningを確認
            for _ in range(int(wait_time * 10)):
                if not isProcessRunning:
                    return
                time.sleep(0.1)
    except ValueError:
        print("無効な待ち時間が入力されました。数値を入力してください。")
        sys.exit(1)  # プログラムを終了
    except Exception as e:
        traceback.print_exc()  # 例外の詳細を出力
        sys.exit(1)  # プログラムを終了

def start_thread():
    """スタートボタンのスレッドを開始する関数。"""
    global automationThread
    automationThread = threading.Thread(target=start_function)
    automationThread.start()

def stop_function():
    # ストップボタンの機能
    global isProcessRunning
    isProcessRunning = False
    if automationThread is not None:
        automationThread.join()
    print("処理を停止しました。")

# 設定の保存に使用するファイル名
CONFIG_FILENAME = 'config.json'

# 設定をJSONファイルに保存する関数
def save_configuration():
    config_data = {
        'input_box': {
            'x': inputBoxXCoordinate,
            'y': inputBoxYCoordinate
        },
        'send_button': {
            'x': sendButtonXCoordinate,
            'y': sendButtonYCoordinate
        },
        'wait_time': wait_time_entry.get(),
        'window_position': {
            'x': windowXPosition,
            'y': windowYPosition
        },
        'always_on_top': topmost_var.get(),
        'language': language_var.get(),
    }
    with open(CONFIG_FILENAME, 'w') as config_file:
        json.dump(config_data, config_file, indent=4)
    print("設定を保存しました。")

def create_default_config_file():
    """デフォルトの設定値で設定ファイルを新規作成する"""
    print("デフォルト値を使用して新しい設定ファイルを作成します。")
    with open(CONFIG_FILENAME, 'w') as config_file:
        json.dump(DEFAULT_CONFIG, config_file, indent=4)
    return DEFAULT_CONFIG

# ウィンドウの設定値を更新する関数
def update_window_data(config_data):
    # グローバル変数の更新
    global inputBoxXCoordinate, inputBoxYCoordinate, sendButtonXCoordinate, sendButtonYCoordinate

    try:
        inputBoxXCoordinate = config_data['input_box']['x']
        inputBoxYCoordinate = config_data['input_box']['y']
    except KeyError:
        print("設定ファイルに input_box キーが存在しません。")
        sys.exit(1)  # プログラムを終了
    try:
        sendButtonXCoordinate = config_data['send_button']['x']
        sendButtonYCoordinate = config_data['send_button']['y']
    except KeyError:
        print("設定ファイルに send_button キーが存在しません。")
        sys.exit(1)  # プログラムを終了
    try:
        wait_time = config_data['wait_time']
        update_labels(inputBoxXCoordinate, inputBoxYCoordinate, sendButtonXCoordinate, sendButtonYCoordinate, wait_time)
    except KeyError:
        print("設定ファイルに wait_time キーが存在しません。")
        sys.exit(1)  # プログラムを終了
    try:
        # ウィンドウ位置を更新
        windowXPosition = config_data['window_position']['x']
        windowYPosition = config_data['window_position']['y']
        root.geometry(f"+{windowXPosition}+{windowYPosition}")
    except KeyError:
        print("設定ファイルに window_position キーが存在しません。")
        sys.exit(1)
    try:
        # 常に最前面に表示を更新
        topmost_var.set(config_data['always_on_top'])
        toggle_topmost()
    except KeyError:
        print("設定ファイルに always_on_top キーが存在しません。")
        sys.exit(1)
    try:
        # 言語を更新
        selected_language = config_data['language']
        language_var.set(selected_language)
        update_ui_language()
    except KeyError:
        print("設定ファイルに language キーが存在しません。")
        sys.exit(1)
        

# GUIのラベルを更新する関数
def update_labels(input_box_x, input_box_y, send_button_x, send_button_y, wait_time):
    input_box_coordinates_label.config(text=f"X: {input_box_x}, Y: {input_box_y}")
    send_button_coordinates_label.config(text=f"X: {send_button_x}, Y: {send_button_y}")
    wait_time_entry.delete(0, tkinter.END)
    wait_time_entry.insert(0, wait_time)

# 設定を読み込む関数
def read_configuration():
    try:
        with open(CONFIG_FILENAME, 'r') as config_file:
            config_data = json.load(config_file)
            return config_data

    except FileNotFoundError:
        print("設定ファイルが見つかりません。デフォルト値を使用して設定ファイルを作成します。")
        config_data = create_default_config_file()
        return config_data

    except json.JSONDecodeError:
        print("設定ファイルが破損しています。デフォルト値を使用して設定ファイルを作成します。")
        config_data = create_default_config_file()
        return config_data

def save_only_window_position(config_window_position_data):
    """ウィンドウ位置のみを設定ファイルに保存する関数"""
    with open(CONFIG_FILENAME, 'w') as config_file:
        # 設定ファイルの window_position キーの値を更新
        config_window_position_data['window_position']['x'] = windowXPosition
        config_window_position_data['window_position']['y'] = windowYPosition
        json.dump(config_window_position_data, config_file, indent=4)
        print("ウィンドウ位置を保存しました。")

# ウィンドウ位置を更新する関数
def update_window_position(x, y):
    global windowXPosition, windowYPosition
    windowXPosition = x
    windowYPosition = y

    # ウィンドウ位置を設定ファイルに保存
    config_data = read_configuration()
    config_data["window_position"] = {"x": x, "y": y}
    save_only_window_position(config_data)

# ウィンドウが閉じられるときの処理
def on_closing():
    update_window_position(root.winfo_x(), root.winfo_y())
    save_configuration()
    root.destroy()

def toggle_topmost():
    """
    トグルスイッチによってウィンドウの最前面表示を切り替える
    """
    if topmost_var.get():
        root.attributes('-topmost', 1)
    else:
        root.attributes('-topmost', 0)

# トグルスイッチのための変数
topmost_var = tkinter.IntVar(value=0)

def update_ui_language():
    selected_language = language_var.get()
    ui_texts = language_settings[selected_language]
    root.title(ui_texts["app_title"])

    if selected_language == "Japanese":
        input_box_coordinates_button.config(text="入力欄の座標取得")
        send_button_coordinates_button.config(text="送信ボタンの座標取得")
        wait_time_label.config(text="応答待ち時間（秒）:")
        save_button.config(text="設定を保存")
        start_button.config(text="開始")
        stop_button.config(text="停止")
        topmost_switch.config(text="常に最前面に表示")
    elif selected_language == "English":
        input_box_coordinates_button.config(text="Get Input Box Coordinates")
        send_button_coordinates_button.config(text="Get Send Button Coordinates")
        wait_time_label.config(text="Wait Time (seconds):")
        save_button.config(text="Save Settings")
        start_button.config(text="Start")
        stop_button.config(text="Stop")
        topmost_switch.config(text="Always on Top")

input_box_coordinates_label = tkinter.Label(root, text="X: 0, Y: 0")
input_box_coordinates_label.pack()

input_box_coordinates_button = tkinter.Button(root, text="メッセージボックス座標取得", command=input_box_coordinates_start_button)
input_box_coordinates_button.pack()

send_button_coordinates_label = tkinter.Label(root, text="X: 0, Y: 0")
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

# トグルスイッチの作成
topmost_switch = tkinter.Checkbutton(root, text="Always on top", variable=topmost_var, command=toggle_topmost)
topmost_switch.pack()

# 言語選択用の変数とUI要素を作成
language_var = tkinter.StringVar(value="English")
language_menu = tkinter.OptionMenu(root, language_var, "English", "Japanese", command=lambda _: update_ui_language())
language_menu.pack()

# プログラム起動時に設定を読み込む
config_data = read_configuration()
print("設定を読み込みました。")

update_window_data(config_data)
print("ウィンドウの設定値を更新しました")

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
