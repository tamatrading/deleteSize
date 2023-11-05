import os
from collections import defaultdict
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def choose_deletion_criteria():
    """
    ユーザーに削除の基準を選択させる関数。
    ラジオボタンを使って3つの基準から選ぶことができます。
    """
    def submit_choice():
        user_choice.set(v.get())
        choice_window.destroy()

    def cancel_and_exit():
        user_choice.set(-1)
        choice_window.destroy()

    # 選択肢
    options = [
        "同じ名前のファイルを１つだけ残す",
        "同じサイズのファイルを１つだけ残す",
        "同じ名前、かつ、同じサイズのファイルを１つだけ残す"
    ]

    choice_window = tk.Tk()
    choice_window.title("削除基準を選択")

    v = tk.IntVar()
    v.set(0)

    # ラジオボタンの設定
    for i, option in enumerate(options):
        ttk.Radiobutton(choice_window, text=option, variable=v, value=i).pack(pady=5, padx=10, anchor='w')

    # ボタンの設定
    ttk.Button(choice_window, text="Submit", command=submit_choice).pack(pady=10, side='left', padx=10)
    ttk.Button(choice_window, text="Cancel", command=cancel_and_exit).pack(pady=10, side='right', padx=10)

    user_choice = tk.IntVar(value=-2)
    choice_window.mainloop()

    return user_choice.get()

def select_directory():
    """
    ユーザーにフォルダを選択させる関数。
    選択したフォルダのパスを返します。
    """
    root = tk.Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory()
    root.destroy()
    return folder_selected

def delete_duplicate_files(target_directory, criteria):
    """
    重複するファイルを削除する関数。
    criteriaに応じて、名前やサイズでの重複を判定します。
    """
    if not os.path.exists(target_directory):
        print(f"ディレクトリ {target_directory} が存在しません。")
        return

    collection = defaultdict(list)

    # 指定されたディレクトリ内のすべてのファイルを調べる
    for root, _, files in os.walk(target_directory):
        for file in files:
            filepath = os.path.join(root, file)
            if os.path.isfile(filepath):
                key = file if criteria in [0, 2] else os.path.getsize(filepath)
                collection[key].append(filepath)
    # 重複するファイルを削除する
    for files in collection.values():
        if len(files) > 1:
            files_to_delete = files[1:] if criteria != 2 else [f for f in files[1:] if os.path.getsize(f) == os.path.getsize(files[0])]
            for filepath in files_to_delete:
                try:
                    os.remove(filepath)
                    print(f"削除されたファイル: {filepath}")
                except Exception as e:
                    print(f"ファイル {filepath} を削除中にエラーが発生しました: {e}")

def show_end_dialog():
    """ 処理終了時に"END"と表示するダイアログを出す関数 """
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("情報", "END")
    root.destroy()

if __name__ == "__main__":
    # 削除基準を選択
    criteria = choose_deletion_criteria()
    if criteria != -1 and criteria != -2:
        # フォルダを選択
        target_directory = select_directory()
        if target_directory:
            # 重複するファイルを削除
            delete_duplicate_files(target_directory, criteria)
            # 処理終了のダイアログを表示
            show_end_dialog()
        else:
            print("フォルダが選択されませんでした。")
    elif criteria == -1:
        print("キャンセルされました。")
    else:
        print("削除基準が選択されませんでした。")
