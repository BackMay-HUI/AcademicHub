from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt5.QtCore import Qt
from ..utils.theme import theme_manager

class StatCard(QWidget):
    """统计卡片组件"""

    def __init__(self, title, value, icon="", color=""):
        super().__init__()
        self.title = title
        self.value = value
        self.icon = icon
        self.color = color or theme_manager.colors['primary']
        self.init_ui()

    def init_ui(self):
        self.setMinimumSize(180, 110)
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # 图标和标题行
        header = QHBoxLayout()
        if self.icon:
            icon_label = QLabel(self.icon)
            icon_label.setStyleSheet("font-size: 24px;")
            header.addWidget(icon_label)
        header.addStretch()
        title_label = QLabel(self.title)
        title_label.setObjectName("cardTitle")
        header.addWidget(title_label)

        # 值 - 居中显示
        value_label = QLabel(str(self.value))
        value_label.setObjectName("cardValue")
        value_label.setAlignment(Qt.AlignCenter)

        layout.addLayout(header)
        layout.addWidget(value_label)
        self.setLayout(layout)
        self.apply_theme()

    def set_value(self, value):
        self.value = value
        for child in self.findChildren(QLabel):
            if child.objectName() == "cardValue":
                child.setText(str(value))

    def apply_theme(self):
        colors = theme_manager.colors
        self.setStyleSheet(f"""
            StatCard {{
                background: {colors['card']};
                border: 1px solid {colors['border']};
                border-radius: 8px;
            }}
            #cardTitle {{
                color: {colors['text_secondary']};
                font-size: 13px;
            }}
            #cardValue {{
                color: {colors['primary']};
                font-size: 28px;
                font-weight: bold;
            }}
        """)

class InfoCard(QWidget):
    """信息卡片组件"""

    def __init__(self, title=""):
        super().__init__()
        self.title = title
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)

        if self.title:
            title_label = QLabel(self.title)
            title_label.setObjectName("cardTitle")
            layout.addWidget(title_label)

        self.content_widget = QWidget()
        layout.addWidget(self.content_widget)

        self.setLayout(layout)
        self.apply_theme()

    def get_content_layout(self):
        return self.content_widget.layout()

    def apply_theme(self):
        colors = theme_manager.colors
        self.setStyleSheet(f"""
            InfoCard {{
                background: {colors['card']};
                border: 1px solid {colors['border']};
                border-radius: 8px;
            }}
            #cardTitle {{
                color: {colors['text_primary']};
                font-size: 16px;
                font-weight: bold;
                padding-bottom: 8px;
                border-bottom: 1px solid {colors['border']};
            }}
        """)

class ProgressCard(QWidget):
    """进度卡片组件"""

    def __init__(self, title, current, total, unit="学分"):
        super().__init__()
        self.title = title
        self.current = current
        self.total = total
        self.unit = unit
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)

        # 标题和进度
        header = QHBoxLayout()
        self.title_label = QLabel(self.title)
        self.title_label.setObjectName("cardTitle")
        header.addWidget(self.title_label)
        header.addStretch()

        percent = (self.current / self.total * 100) if self.total > 0 else 0
        self.progress_label = QLabel(f"{self.current}/{self.total} {self.unit} ({percent:.1f}%)")
        self.progress_label.setObjectName("progressText")
        header.addWidget(self.progress_label)

        # 进度条
        self.progress_bar = QFrame()
        self.progress_bar.setFixedHeight(8)
        self.progress_bar.setObjectName("progressBarBg")

        self.progress_inner = QFrame(self.progress_bar)
        self.progress_inner.setFixedWidth(int(percent * 2))
        self.progress_inner.setFixedHeight(8)
        self.progress_inner.setObjectName("progressBarInner")
        self.progress_inner.move(0, 0)

        layout.addLayout(header)
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)
        self.apply_theme()

    def set_title(self, title):
        """更新标题"""
        self.title = title
        if hasattr(self, 'title_label'):
            self.title_label.setText(title)

    def update_progress(self, current, total):
        """更新进度"""
        self.current = current
        self.total = total
        percent = (current / total * 100) if total > 0 else 0
        self.progress_label.setText(f"{current}/{total} {self.unit} ({percent:.1f}%)")
        self.progress_inner.setFixedWidth(int(percent * 2))

    def apply_theme(self):
        colors = theme_manager.colors
        self.setStyleSheet(f"""
            ProgressCard {{
                background: {colors['card']};
                border: 1px solid {colors['border']};
                border-radius: 8px;
            }}
            #cardTitle {{
                color: {colors['text_primary']};
                font-size: 14px;
                font-weight: bold;
            }}
            #progressText {{
                color: {colors['text_secondary']};
                font-size: 12px;
            }}
            #progressBarBg {{
                background: {colors['border']};
                border-radius: 4px;
            }}
            #progressBarInner {{
                background: {colors['primary']};
                border-radius: 4px;
            }}
        """)
