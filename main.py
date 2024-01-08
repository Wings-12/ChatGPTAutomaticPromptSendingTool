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

def on_coordinates_button_click(x, y, button, pressed):
    global listener_running
    if not listener_running:
        return False
    if pressed and button == Button.left:
        # print(f"Mouse clicked at ({x}, {y})")
        # メインスレッドでラベルを更新する　理由：https://stackoverflow.com/a/22835289/9263761
        root.after(0, lambda: coordinates_label.config(text=f"X: {x}, Y: {y}"))

def start_listener():
    with Listener(on_click=on_coordinates_button_click) as listener:
        listener.join()

# グローバル変数の初期化
listener_thread = None
listener_running = False

def toggle_coordinates_button():
    global listener_thread, listener_running
    if not listener_running:
        coordinates_button.config(text='座標取得終了')
        listener_running = True
        listener_thread = threading.Thread(target=start_listener)
        listener_thread.start()
    else:
        coordinates_button.config(text='座標取得')
        listener_running = False

def detect_chatgpt_response():
    try:
        # 特定の画像（回答完了のインジケーター）が画面上にあるかを確認
        response_indicator = pyautogui.locateOnScreen('response_complete_indicator.png')
        if response_indicator is not None:
            print("回答完了のインジケーターを見つけました。")
            return True
    except pyautogui.ImageNotFoundException:
        # 画像が見つからない例外は無視する
        pass
    return False

def start_function():
    try:
        # ChatGPTが回答を書き終わるのを待つ
        while not detect_chatgpt_response():
            print("回答が書き終わるのを待っています。")
            time.sleep(5)  # 1秒ごとにチェック

            # ChatGPTの入力欄の位置を検出
            input_box_location = pyautogui.locateOnScreen('chatgpt_input_box.png', confidence=.5)

            if input_box_location is not None:
                print("入力欄を見つけました。")
                # 入力欄の中心にカーソルを移動し、クリックする
                pyautogui.click(pyautogui.center(input_box_location))
            else:
                print("入力欄が見つかりませんでした。")
                return 0

            # ChatGPTの入力欄に「続きを書いてください。」と入力
            pyautogui.write('続きを書いてください。', interval=0.25)
            
            # 送信ボタンの位置を検出
            send_button_location = pyautogui.locateOnScreen('chatgpt_send_button.png')
            if send_button_location is not None:
                print("送信ボタンを見つけました。")
                # 送信ボタンをクリック
                pyautogui.click(pyautogui.center(send_button_location))
            else:
                print("送信ボタンが見つかりませんでした。")

    except Exception as e:
        traceback.print_exc()  # 例外の詳細を出力

def stop_function():
    # ストップボタンの機能
    pass

def resume_function():
    # 再開ボタンの機能
    pass

coordinates_button = tkinter.Button(root, text="メッセージボックス座標取得", command=toggle_coordinates_button)
start_button = tkinter.Button(root, text="Start", command=start_function)
stop_button = tkinter.Button(root, text="Stop", command=stop_function)
resume_button = tkinter.Button(root, text="Resume", command=resume_function)

coordinates_button.pack()
start_button.pack()
stop_button.pack()
resume_button.pack()
root.mainloop()
