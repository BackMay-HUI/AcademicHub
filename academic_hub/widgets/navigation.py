from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import pyqtSignal, Qt
from ..utils.theme import theme_manager

class NavigationWidget(QWidget):
    """导航栏组件"""
    page_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.current_page = "grades"
        self.buttons = {}
        self.init_ui()
        self.apply_theme()

        # 连接主题变化信号
        theme_manager.theme_changed.connect(self.on_theme_changed)

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 标题
        title = QLabel("AcademicHub")
        title.setObjectName("navTitle")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # 导航项
        nav_items = [
            ("grades", "📊", "成绩管理"),
            ("honors", "🏆", "荣誉档案"),
            ("graduation", "🎓", "毕业追踪"),
            ("graduate", "📈", "保研模拟"),
            ("notes", "📝", "Markdown笔记"),
            ("resume", "📄", "简历导出")
        ]

        for page_id, icon, text in nav_items:
            btn = QPushButton(f"{icon}  {text}")
            btn.setObjectName("navButton")
            btn.clicked.connect(lambda checked, p=page_id: self.change_page(p))
            self.buttons[page_id] = btn
            layout.addWidget(btn)

        # 主题切换按钮
        layout.addStretch()
        self.theme_btn = QPushButton("🌙 切换主题")
        self.theme_btn.setObjectName("themeButton")
        self.theme_btn.clicked.connect(self.toggle_theme)
        layout.addWidget(self.theme_btn)

        self.setLayout(layout)
        self.update_buttons()

    def change_page(self, page_id):
        self.current_page = page_id
        self.update_buttons()
        self.page_changed.emit(page_id)

    def update_buttons(self):
        for page_id, btn in self.buttons.items():
            if page_id == self.current_page:
                btn.setProperty("active", True)
            else:
                btn.setProperty("active", False)
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    def toggle_theme(self):
        theme_manager.toggle_theme()

    def on_theme_changed(self, theme_name):
        self.apply_theme()

    def apply_theme(self):
        colors = theme_manager.colors
        self.setStyleSheet(f"""
            #navTitle {{
                font-size: 20px;
                font-weight: bold;
                color: {colors['primary']};
                padding: 20px 10px;
            }}
            QPushButton#navButton {{
                background: transparent;
                border: none;
                padding: 12px 20px;
                text-align: left;
                font-size: 14px;
                color: {colors['text_primary']};
                border-radius: 0;
            }}
            QPushButton#navButton:hover {{
                background: {colors['hover']};
            }}
            QPushButton#navButton[active="true"] {{
                background: {colors['primary']};
                color: white;
            }}
            QPushButton#themeButton {{
                background: {colors['card']};
                border: 1px solid {colors['border']};
                padding: 10px;
                border-radius: 6px;
                color: {colors['text_primary']};
            }}
            QPushButton#themeButton:hover {{
                background: {colors['hover']};
            }}
        """)
