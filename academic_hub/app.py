from PyQt5.QtWidgets import QWidget, QStackedWidget, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from .widgets.navigation import NavigationWidget
from .pages.grades import GradesPage
from .pages.honors import HonorsPage
from .pages.graduation import GraduationPage
from .pages.graduate import GraduatePage
from .pages.notes import NotesPage
from .pages.resume import ResumePage
from .utils.theme import theme_manager
from .config import load_config

class AcademicHubApp(QWidget):
    """主应用窗口"""

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.apply_theme()

        # 连接主题变化信号
        theme_manager.theme_changed.connect(self.on_theme_changed)

    def init_ui(self):
        config = load_config()
        width = config.get("window", {}).get("width", 1880)
        height = config.get("window", {}).get("height", 1400)

        self.setWindowTitle("AcademicHub - 大学生学业与荣誉管理助手")
        self.setMinimumSize(1400, 1000)
        self.resize(width, height)

        # 布局
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 导航栏
        self.nav = NavigationWidget()
        self.nav.page_changed.connect(self.on_page_changed)
        self.nav.setFixedWidth(240)
        layout.addWidget(self.nav)

        # 页面容器
        self.stack = QStackedWidget()

        # 创建各页面
        self.grades_page = GradesPage()
        self.honors_page = HonorsPage()
        self.graduation_page = GraduationPage()
        self.graduate_page = GraduatePage()
        self.notes_page = NotesPage()
        self.resume_page = ResumePage()

        # 添加页面
        self.stack.addWidget(self.grades_page)      # 0
        self.stack.addWidget(self.honors_page)       # 1
        self.stack.addWidget(self.graduation_page)   # 2
        self.stack.addWidget(self.graduate_page)     # 3
        self.stack.addWidget(self.notes_page)         # 4
        self.stack.addWidget(self.resume_page)       # 5

        layout.addWidget(self.stack)

        self.setLayout(layout)

        # 默认显示成绩页面
        self.stack.setCurrentIndex(0)

    def on_page_changed(self, page_id):
        """切换页面"""
        page_map = {
            "grades": 0,
            "honors": 1,
            "graduation": 2,
            "graduate": 3,
            "notes": 4,
            "resume": 5
        }
        index = page_map.get(page_id, 0)
        self.stack.setCurrentIndex(index)

    def on_theme_changed(self, theme_name):
        self.apply_theme()

    def apply_theme(self):
        colors = theme_manager.colors
        self.setStyleSheet(f"""
            QWidget {{
                background: {colors['background_gradient']};
                font-family: "Microsoft YaHei", "Segoe UI", sans-serif;
            }}
            QMessageBox {{
                background: {colors['card']};
            }}
        """)

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, '确认退出',
            "确定要退出应用吗?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
