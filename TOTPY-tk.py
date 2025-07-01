from pyotp import TOTP
from tkinter import Tk, Toplevel, END, messagebox
from tkinter.ttk import *
import pyperclip as cb
import time
import ctypes

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except:
        pass

class code_dialog:
    def __init__(self, master, acode):
        self.master = master
        self.acode = acode
        self.font = ("Consolas", 10)
        self._initUI()
        
        # 设置窗口位置在父窗口中心
        self.master.update_idletasks()
        parent_x = self.master.winfo_parent().winfo_x()
        parent_y = self.master.winfo_parent().winfo_y()
        parent_width = self.master.winfo_parent().winfo_width()
        parent_height = self.master.winfo_parent().winfo_height()
        
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        x = parent_x + (parent_width - width) // 2
        y = parent_y + (parent_height - height) // 2
        self.master.geometry(f"+{x}+{y}")

    def _initUI(self):
        self.master.resizable(False, False)
        self.master.grid_columnconfigure(1, weight=1)
        
        Label(self.master, text="验证码:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.code = Entry(self.master, font=self.font, width=20)
        self.code.grid(row=0, column=1, padx=5, pady=5, sticky="we")
        
        try:
            # 尝试生成验证码
            current_code = TOTP(self.acode).now()
            self.valid = True
        except Exception as e:
            # 处理无效密钥
            current_code = "无效密钥!"
            self.valid = False
        
        self.code.delete(0, END)
        self.code.insert(END, current_code)
        self.code.config(state="readonly")  # 设置为只读
        
        # 添加按钮框架
        button_frame = Frame(self.master)
        button_frame.grid(row=1, column=0, columnspan=2, pady=5)
        
        Button(button_frame, text="复制", command=self.copy).pack(side="left", padx=5)
        Button(button_frame, text="关闭", command=self.master.destroy).pack(side="left", padx=5)

    def copy(self):
        if not self.valid:
            messagebox.showerror("错误", "无法复制无效的验证码!")
            return
            
        code = self.code.get()
        cb.copy(code)
        messagebox.showinfo("提示", "验证码已复制到剪贴板!")
        self.master.destroy()  # 复制后自动关闭窗口

class App:
    def __init__(self, root):
        self.root = root
        self._initUI()

    def _initUI(self):
        self.root.resizable(False, False)
        self.root.grid_columnconfigure(1, weight=1)
        
        Label(self.root, text="TOTP密钥:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.acode = Entry(self.root, font=("Consolas", 10))
        self.acode.grid(row=0, column=1, padx=5, pady=5, sticky="we")
        self.acode.focus_set()  # 设置初始焦点
        
        # 添加按钮框架
        button_frame = Frame(self.root)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        Button(button_frame, text="生成验证码", command=self.act).pack(side="left", padx=5)
        Button(button_frame, text="退出", command=self.root.destroy).pack(side="left", padx=5)
        
        # 绑定回车键
        self.root.bind('<Return>', lambda event: self.act())

    def act(self):
        acode = self.acode.get().strip()  # 去除空白字符
        if not acode:
            messagebox.showwarning("警告", "请输入TOTP密钥!")
            return
            
        d = Toplevel(self.root)
        d.title("验证码")
        code_dialog(d, acode)

def main():
    root = Tk()
    root.title("TOTP验证码生成器")
    root.geometry("300x120")
    App(root)
    root.mainloop()  # 添加缺失的主循环

if __name__ == "__main__":
    main()
