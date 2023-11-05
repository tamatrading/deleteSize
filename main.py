import os
from collections import defaultdict
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


def choose_deletion_criteria():
    """
    ユーザーに削除基準を選択させる関数。
    ラジオボタンを使用して、削除の基準を選択させます。
    """

    # 選択した基準を取得してウィンドウを閉じる関数
    def submit_choice():
        user_choice.set(v.get())
        choice_window.destroy()

    # キャンセルしてウィンドウを閉じる関数
    def cancel_and_exit():
        user_choice.set(-1)
        choice_window.destroy()

    # 削除基準のオプション
    options = [
        "同じ名前のファイルを１つだけ残す",
        "同じサイズのファイルを１つだけ残す",
        "同じ名前、かつ、同じサイズのファイルを１つだけ残す"
    ]

    choice_window = tk.Tk()
    choice_window.title("削除基準を選択")

    v = tk.IntVar()
    v.set(0)

    # ラジオボタンの表示
    for i, option in enumerate(options):
        ttk.Radiobutton(choice_window, text=option, variable=v, value=i).pack(pady=5, padx=10, anchor='w')

    # サブミットボタンとキャンセルボタンの表示
    ttk.Button(choice_window, text="Submit", command=submit_choice).pack(pady=10, side='left', padx=10)
    ttk.Button(choice_window, text="Cancel", command=cancel_and_exit).pack(pady=10, side='right', padx=10)

    user_choice = tk.IntVar(value=-2)

    # ウィンドウを中央に配置
    choice_window.update_idletasks()
    width = choice_window.winfo_width()
    height = choice_window.winfo_height()
    x = (choice_window.winfo_screenwidth() // 2) - (width // 2)
    y = (choice_window.winfo_screenheight() // 2) - (height // 2)
    choice_window.geometry(f'{width}x{height}+{x}+{y}')

    choice_window.mainloop()

    return user_choice.get()


def select_directory():
    """
    ユーザーにディレクトリを選択させるダイアログを表示。
    選択したディレクトリのパスを返す。
    """

    root = tk.Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory()
    root.destroy()
    return folder_selected


def delete_duplicate_files(target_directory, criteria):
    """
    指定ディレクトリ内の重複ファイルを指定の基準に基づいて削除。
    :param target_directory: ターゲットとなるディレクトリのパス
    :param criteria: 削除の基準 (0, 1, or 2)
    """

    if not os.path.exists(target_directory):
        print(f"ディレクトリ {target_directory} が存在しません。")
        return

    collection = defaultdict(list)

    # ファイルの収集
    for root, _, files in os.walk(target_directory):
        for file in files:
            filepath = os.path.join(root, file)
            if os.path.isfile(filepath):
                key = file if criteria in [0, 2] else os.path.getsize(filepath)
                collection[key].append(filepath)

    # 重複ファイルの削除
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
    """ 処理の終了をユーザーに通知するダイアログを表示 """

    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("情報", "END")
    root.destroy()


def move_files_to_top(target_directory):
    """
    指定ディレクトリ内のファイルをディレクトリのトップレベルに移動。
    同名のファイルが存在する場合は連番を付けて重複を避ける。
    :param target_directory: ターゲットとなるディレクトリのパス
    """

    for root, _, files in os.walk(target_directory):
        for file in files:
            original_path = os.path.join(root, file)
            target_path = os.path.join(target_directory, file)

            if os.path.abspath(original_path) == os.path.abspath(target_path):
                continue

            # 同名ファイルの処理
            counter = 1
            while os.path.exists(target_path):
                base, ext = os.path.splitext(file)
                file = f"{base}({counter}){ext}"
                target_path = os.path.join(target_directory, file)
                counter += 1

            os.rename(original_path, target_path)


if __name__ == "__main__":
    # 削除基準の選択
    criteria = choose_deletion_criteria()
    if criteria != -1 and criteria != -2:
        # ディレクトリの選択
        target_directory = select_directory()
        if target_directory:
            delete_duplicate_files(target_directory, criteria)
            # ファイルの移動
            move_files_to_top(target_directory)
            # 終了通知
            show_end_dialog()
        else:
            print("フォルダが選択されませんでした。")
    elif criteria == -1:
        print("キャンセルされました。")
    else:
        print("削除基準が選択されませんでした。")
