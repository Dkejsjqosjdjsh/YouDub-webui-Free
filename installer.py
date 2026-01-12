import os
import sys
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import urllib.request
import zipfile

class YouDubInstaller:
    def __init__(self, root):
        self.root = root
        self.root.title("YouDub-webui 免費版 一鍵安裝程序")
        self.root.geometry("500x400")
        
        self.install_path = tk.StringVar(value="C:\\YouDub-Free")
        
        self.create_widgets()
        
    def create_widgets(self):
        tk.Label(self.root, text="歡迎使用 YouDub-webui 免費版安裝程序", font=("Arial", 14, "bold")).pack(pady=20)
        
        # 安裝路徑選擇
        path_frame = tk.Frame(self.root)
        path_frame.pack(pady=10, fill="x", padx=20)
        tk.Label(path_frame, text="安裝目錄:").pack(side="left")
        tk.Entry(path_frame, textvariable=self.install_path).pack(side="left", fill="x", expand=True, padx=5)
        tk.Button(path_frame, text="瀏覽...", command=self.browse_path).pack(side="left")
        
        # 狀態顯示
        self.status_label = tk.Label(self.root, text="等待開始...", fg="blue")
        self.status_label.pack(pady=10)
        
        # 按鈕
        tk.Button(self.root, text="開始安裝", command=self.start_installation, bg="green", fg="white", font=("Arial", 12, "bold"), width=20).pack(pady=20)
        
        # 說明
        tk.Label(self.root, text="注意：安裝過程需要聯網下載必要組件", fg="gray").pack(side="bottom", pady=10)

    def browse_path(self):
        path = filedialog.askdirectory()
        if path:
            self.install_path.set(path)

    def check_python(self):
        try:
            subprocess.run(["python", "--version"], check=True, capture_output=True)
            return True
        except:
            return False

    def start_installation(self):
        # 1. 檢查 Python
        self.status_label.config(text="正在檢查 Python 環境...", fg="blue")
        self.root.update()
        if not self.check_python():
            messagebox.showerror("錯誤", "未檢測到 Python 環境！\n請先前往 https://www.python.org/ 下載並安裝 Python，並勾選 'Add Python to PATH'。")
            return

        # 2. 創建目錄
        dest = self.install_path.get()
        try:
            if not os.path.exists(dest):
                os.makedirs(dest)
            self.status_label.config(text=f"正在部署文件到 {dest}...", fg="blue")
            self.root.update()
        except Exception as e:
            messagebox.showerror("錯誤", f"無法創建目錄: {e}")
            return

        # 3. 下載/複製源代碼 (這裡模擬從 GitHub 下載)
        # 在實際 EXE 中，我們可以將源代碼打包在資源中，或者從 GitHub 下載 zip
        repo_url = "https://github.com/Dkejsjqosjdjsh/YouDub-webui-Free/archive/refs/heads/master.zip"
        zip_path = os.path.join(dest, "source.zip")
        
        try:
            self.status_label.config(text="正在從 GitHub 下載最新代碼...", fg="blue")
            self.root.update()
            urllib.request.urlretrieve(repo_url, zip_path)
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(dest)
            
            # 移動文件到根目錄
            extracted_dir = os.path.join(dest, "YouDub-webui-Free-master")
            for item in os.listdir(extracted_dir):
                s = os.path.join(extracted_dir, item)
                d = os.path.join(dest, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, dirs_exist_ok=True)
                else:
                    shutil.copy2(s, d)
            
            shutil.rmtree(extracted_dir)
            os.remove(zip_path)
            
        except Exception as e:
            messagebox.showerror("錯誤", f"下載或解壓失敗: {e}")
            return

        # 4. 安裝依賴
        self.status_label.config(text="正在安裝依賴庫 (這可能需要幾分鐘)...", fg="blue")
        self.root.update()
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", os.path.join(dest, "requirements.txt")], check=True)
        except:
            self.status_label.config(text="依賴安裝部分失敗，請稍後手動運行 setup_windows.bat", fg="orange")

        # 5. 創建捷徑 (Windows 特有)
        self.create_shortcut(dest)

        self.status_label.config(text="安裝完成！", fg="green")
        messagebox.showinfo("成功", "YouDub-webui 已成功安裝！\n您可以在桌面找到捷徑，或直接運行目錄下的 run_windows.bat。")
        self.root.destroy()

    def create_shortcut(self, target_dir):
        try:
            import winshell
            from win32com.client import Dispatch

            desktop = winshell.desktop()
            path = os.path.join(desktop, "YouDub-Free.lnk")
            target = os.path.join(target_dir, "run_windows.bat")
            wDir = target_dir
            icon = os.path.join(target_dir, "run_windows.bat") # 暫時用 bat 作為圖標

            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(path)
            shortcut.Targetpath = target
            shortcut.WorkingDirectory = wDir
            shortcut.IconLocation = icon
            shortcut.save()
        except:
            # 如果缺少 winshell 等庫，則跳過捷徑創建
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = YouDubInstaller(root)
    root.mainloop()
