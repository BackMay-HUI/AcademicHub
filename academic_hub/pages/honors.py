from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QPushButton, QLabel,
                             QHeaderView, QMessageBox, QComboBox)
from PyQt5.QtCore import Qt
from ..database import (add_honor, get_all_honors, update_honor,
                        delete_honor, get_honor_stats)
from ..utils.theme import theme_manager
from ..widgets.dialogs import AddHonorDialog
from ..widgets.cards import StatCard

class HonorsPage(QWidget):
    """荣誉档案页面"""

    def __init__(self):
        super().__init__()
        self.current_filter = "全部"
        self.init_ui()
        self.load_data()
        self.apply_theme()

        theme_manager.theme_changed.connect(self.on_theme_changed)

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        # 标题栏
        header = QHBoxLayout()
        title = QLabel("荣誉档案")
        title.setObjectName("pageTitle")
        header.addWidget(title)
        header.addStretch()

        add_btn = QPushButton("+ 添加荣誉")
        add_btn.clicked.connect(self.add_honor)
        header.addWidget(add_btn)

        layout.addLayout(header)

        # 统计卡片
        self.stats_layout = QHBoxLayout()
        self.total_card = StatCard("荣誉总数", "0", "🏆")
        self.scholarship_card = StatCard("奖学金", "0", "💰")
        self.competition_card = StatCard("竞赛获奖", "0", "🎯")
        self.title_card = StatCard("荣誉称号", "0", "⭐")
        self.stats_layout.addWidget(self.total_card)
        self.stats_layout.addWidget(self.scholarship_card)
        self.stats_layout.addWidget(self.competition_card)
        self.stats_layout.addWidget(self.title_card)
        layout.addLayout(self.stats_layout)

        # 筛选栏
        filter_layout = QHBoxLayout()
        filter_label = QLabel("筛选:")
        filter_layout.addWidget(filter_label)

        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["全部", "奖学金", "竞赛获奖", "荣誉称号", "社会实践", "其他"])
        self.filter_combo.currentTextChanged.connect(self.on_filter_changed)
        filter_layout.addWidget(self.filter_combo)

        filter_layout.addStretch()

        self.total_label = QLabel("共 0 条记录")
        filter_layout.addWidget(self.total_label)

        layout.addLayout(filter_layout)

        # 荣誉表格
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "荣誉名称", "类型", "级别", "获得日期", "描述"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.hideColumn(0)

        layout.addWidget(self.table)

        # 操作按钮
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        edit_btn = QPushButton("编辑")
        edit_btn.clicked.connect(self.edit_honor)
        btn_layout.addWidget(edit_btn)

        delete_btn = QPushButton("删除")
        delete_btn.clicked.connect(self.delete_honor)
        btn_layout.addWidget(delete_btn)

        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def load_data(self):
        honors = get_all_honors()
        stats = get_honor_stats()

        # 更新统计卡片
        by_type = stats.get('by_type', {})
        self.total_card.set_value(stats['total'])
        self.scholarship_card.set_value(by_type.get('奖学金', 0))
        self.competition_card.set_value(by_type.get('竞赛获奖', 0))
        self.title_card.set_value(by_type.get('荣誉称号', 0))

        # 筛选
        if self.current_filter != "全部":
            honors = [h for h in honors if h['type'] == self.current_filter]

        # 更新表格
        self.table.setRowCount(len(honors))
        for row, honor in enumerate(honors):
            self.table.setItem(row, 0, QTableWidgetItem(str(honor['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(honor['title']))
            self.table.setItem(row, 2, QTableWidgetItem(honor['type']))
            self.table.setItem(row, 3, QTableWidgetItem(honor['level']))
            self.table.setItem(row, 4, QTableWidgetItem(honor['date']))
            self.table.setItem(row, 5, QTableWidgetItem(honor['description'] or ""))

        self.total_label.setText(f"共 {len(honors)} 条记录")

    def on_filter_changed(self, text):
        self.current_filter = text
        self.load_data()

    def add_honor(self):
        dialog = AddHonorDialog(self)
        if dialog.exec_():
            data = dialog.get_data()
            add_honor(**data)
            self.load_data()

    def edit_honor(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "提示", "请选择要编辑的荣誉")
            return

        honor_id = int(self.table.item(row, 0).text())
        honors = get_all_honors()
        honor = next((h for h in honors if h['id'] == honor_id), None)

        dialog = AddHonorDialog(self, honor)
        if dialog.exec_():
            data = dialog.get_data()
            update_honor(honor_id, **data)
            self.load_data()

    def delete_honor(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "提示", "请选择要删除的荣誉")
            return

        reply = QMessageBox.question(self, "确认删除",
                                      "确定要删除这条荣誉记录吗?",
                                      QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            honor_id = int(self.table.item(row, 0).text())
            delete_honor(honor_id)
            self.load_data()

    def apply_theme(self):
        colors = theme_manager.colors
        self.setStyleSheet(f"""
            #pageTitle {{
                font-size: 24px;
                font-weight: bold;
                color: {colors['text_primary']};
            }}
            QLabel {{
                color: {colors['text_secondary']};
            }}
            QComboBox {{
                background: {colors['card']};
                color: {colors['text_primary']};
                border: 1px solid {colors['border']};
                padding: 6px;
                border-radius: 4px;
                min-width: 100px;
            }}
            QPushButton {{
                background: {colors['primary']};
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }}
            QTableWidget {{
                background: {colors['card']};
                color: {colors['text_primary']};
                border: 1px solid {colors['border']};
                gridline-color: {colors['border']};
            }}
            QHeaderView::section {{
                background: {colors['primary']};
                color: white;
                padding: 6px;
                border: none;
            }}
        """)

    def on_theme_changed(self, theme_name):
        self.apply_theme()
        for card in [self.total_card, self.scholarship_card, self.competition_card, self.title_card]:
            card.apply_theme()
