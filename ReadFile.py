from tkinter import filedialog
import tkinter as tk

def ChooseMd():
    # 檢查是否已經有 root
    if not tk._default_root:
        root = tk.Tk()
    else:
        return 0
    root.withdraw()  # 隱藏主視窗
    root.attributes('-topmost', True)  # 設置為最上層窗口
    #打開文件選擇對話框並設置文件類型為圖片
    file_path = filedialog.askopenfilename(
        title="選擇Markdown文件",
        filetypes=[("md Files", "*.md")]
    )
    root.destroy() #刪除root
    root = None
        
    #檢查用戶是否選擇了文件
    if file_path:
        print(f"Selected file: {file_path}")
        return file_path
    else:
        print("No file selected.")
        return 0
    
def ChooseSavePath():
    # 檢查是否已經有 root
    if not tk._default_root:
        root = tk.Tk()
    else:
        return 0
    root.withdraw()  # 隱藏主視窗
    root.attributes('-topmost', True)  # 設置為最上層窗口
    #打開文件選擇對話框並設置文件類型為圖片
    file_path = filedialog.askdirectory(
        title="選擇Markdown儲存位置"
    )
    root.destroy() #刪除root
    root = None
        
    #檢查用戶是否選擇了文件
    if file_path:
        print(f"Selected file: {file_path}")
        return file_path
    else:
        print("No file selected.")
        return 0
    