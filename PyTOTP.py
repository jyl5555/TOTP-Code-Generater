import sys
from pyotp import TOTP
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QDialog, QWidget, QLabel, QLineEdit, 
    QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QSizePolicy
)
from PyQt5.QtGui import QFont, QClipboard
from PyQt5.QtCore import Qt, QSize

class CodeDialog(QDialog):
    def __init__(self, parent, acode):
        super().__init__(parent)
        self.acode = acode
        self.setWindowTitle("验证码")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setFixedSize(300, 150)
        
        # 设置字体
        code_font = QFont("Consolas", 14, QFont.Bold)
        label_font = QFont("Arial", 10)
        button_font = QFont("Arial", 9)
        
        # 创建UI元素
        self.code_label = QLabel("验证码:")
        self.code_label.setFont(label_font)
        
        self.code_entry = QLineEdit()
        self.code_entry.setFont(code_font)
        self.code_entry.setReadOnly(True)
        self.code_entry.setAlignment(Qt.AlignCenter)
        self.code_entry.setMinimumHeight(40)
        
        # 尝试生成验证码
        try:
            current_code = TOTP(self.acode).now()
            self.valid = True
            # 格式化验证码显示 (添加空格)
            formatted_code = " ".join([current_code[i:i+3] for i in range(0, len(current_code), 3)])
            self.code_entry.setText(formatted_code)
        except Exception:
            self.code_entry.setText("无效密钥!")
            self.valid = False
        
        # 创建按钮
        self.copy_button = QPushButton("复制验证码")
        self.copy_button.setFont(button_font)
        self.copy_button.setMinimumHeight(35)
        self.copy_button.setStyleSheet(
            "QPushButton { background-color: #4CAF50; color: white; border-radius: 4px; }"
            "QPushButton:hover { background-color: #45a049; }"
            "QPushButton:pressed { background-color: #3d8b40; }"
            "QPushButton:disabled { background-color: #cccccc; }"
        )
        self.copy_button.clicked.connect(self.copy_code)
        
        self.close_button = QPushButton("关 闭")
        self.close_button.setFont(button_font)
        self.close_button.setMinimumHeight(35)
        self.close_button.setStyleSheet(
            "QPushButton { background-color: #f44336; color: white; border-radius: 4px; }"
            "QPushButton:hover { background-color: #d32f2f; }"
            "QPushButton:pressed { background-color: #b71c1c; }"
        )
        self.close_button.clicked.connect(self.accept)
        
        # 布局
        main_layout = QVBoxLayout()
        input_layout = QHBoxLayout()
        button_layout = QHBoxLayout()
        
        input_layout.addWidget(self.code_label)
        input_layout.addWidget(self.code_entry)
        
        button_layout.addWidget(self.copy_button)
        button_layout.addWidget(self.close_button)
        
        main_layout.addLayout(input_layout)
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
        
        # 设置无效状态
        if not self.valid:
            self.copy_button.setEnabled(False)
    
    def copy_code(self):
        if not self.valid:
            return
            
        # 获取原始验证码（不带空格）
        code = self.code_entry.text().replace(" ", "")
        clipboard = QApplication.clipboard()
        clipboard.setText(code)
        
        QMessageBox.information(self, "成功", "验证码已复制到剪贴板!")
        self.accept()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TOTP 验证码生成器")
        self.setFixedSize(400, 200)
        
        # 创建中央部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # 设置字体
        title_font = QFont("Arial", 12, QFont.Bold)
        label_font = QFont("Arial", 10)
        entry_font = QFont("Consolas", 10)
        button_font = QFont("Arial", 10, QFont.Bold)
        
        # 创建标题
        title_label = QLabel("TOTP 验证码生成器")
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50; padding: 5px;")
        main_layout.addWidget(title_label)
        
        # 创建输入区域
        input_layout = QHBoxLayout()
        input_layout.setSpacing(10)
        
        acode_label = QLabel("TOTP 密钥:")
        acode_label.setFont(label_font)
        self.acode_entry = QLineEdit()
        self.acode_entry.setFont(entry_font)
        self.acode_entry.setPlaceholderText("输入您的 TOTP 密钥...")
        self.acode_entry.setMinimumHeight(35)
        
        input_layout.addWidget(acode_label)
        input_layout.addWidget(self.acode_entry)
        
        main_layout.addLayout(input_layout)
        
        # 创建按钮区域
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        self.generate_button = QPushButton("生成验证码")
        self.generate_button.setFont(button_font)
        self.generate_button.setMinimumHeight(40)
        self.generate_button.setStyleSheet(
            "QPushButton { background-color: #3498db; color: white; border-radius: 5px; }"
            "QPushButton:hover { background-color: #2980b9; }"
            "QPushButton:pressed { background-color: #1c6ea4; }"
        )
        self.generate_button.clicked.connect(self.generate_code)
        
        self.quit_button = QPushButton("退 出")
        self.quit_button.setFont(button_font)
        self.quit_button.setMinimumHeight(40)
        self.quit_button.setStyleSheet(
            "QPushButton { background-color: #95a5a6; color: white; border-radius: 5px; }"
            "QPushButton:hover { background-color: #7f8c8d; }"
            "QPushButton:pressed { background-color: #6c7a7d; }"
        )
        self.quit_button.clicked.connect(self.close)
        
        button_layout.addWidget(self.generate_button)
        button_layout.addWidget(self.quit_button)
        
        main_layout.addLayout(button_layout)
        
        # 状态栏
        self.statusBar().showMessage("就绪")
        
        # 设置焦点
        self.acode_entry.setFocus()
        
        # 连接回车键
        self.acode_entry.returnPressed.connect(self.generate_code)
    
    def generate_code(self):
        acode = self.acode_entry.text().strip()
        if not acode:
            QMessageBox.warning(self, "警告", "请输入 TOTP 密钥!")
            return
        
        # 创建并显示验证码对话框
        dialog = CodeDialog(self, acode)
        dialog.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 设置应用样式
    app.setStyle("Fusion")
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
