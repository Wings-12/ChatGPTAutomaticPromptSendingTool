import sys
import tkinter

root = tkinter.Tk()
root.title("ChatGPT 自動送信ツール")
root.geometry("400x300")  # Set the window size to 400 pixels wide and 300 pixels tall

def start_function():
    # スタートボタンの機能
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
