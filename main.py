"""
AcademicHub - 大学生学业与荣誉管理助手
入口文件
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtCore import Qt
from academic_hub.app import AcademicHubApp
from academic_hub.database import init_db

def main():
    # 初始化数据库
    init_db()

    # 创建应用
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    # 设置中文字体
    font_id = QFontDatabase.addApplicationFont("C:/Windows/Fonts/msyh.ttc")
    if font_id != -1:
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        app.setFont(QFont(font_family))

    # 创建并显示主窗口
    window = AcademicHubApp()
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
