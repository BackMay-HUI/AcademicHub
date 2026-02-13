from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QPushButton, QComboBox, QLabel,
                             QHeaderView, QMessageBox, QScrollArea, QFrame)
from PyQt5.QtCore import Qt
from ..database import (add_grade, get_all_grades, update_grade,
                        delete_grade, get_grade_stats)
from ..config import COURSE_TYPES, SEMESTERS
from ..utils.theme import theme_manager
from ..widgets.dialogs import AddGradeDialog
from ..widgets.cards import StatCard

class GradesPage(QWidget):
    """成绩管理页面"""

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
        title = QLabel("成绩管理")
        title.setObjectName("pageTitle")
        header.addWidget(title)
        header.addStretch()

        add_btn = QPushButton("+ 添加成绩")
        add_btn.clicked.connect(self.add_grade)
        header.addWidget(add_btn)

        layout.addLayout(header)

        # 统计卡片
        self.stats_layout = QHBoxLayout()
        self.gpa_card = StatCard("GPA", "0.00", "📊")
        self.avg_card = StatCard("加权平均分", "0", "📈")
        self.credits_card = StatCard("已获学分", "0", "📚")
        self.stats_layout.addWidget(self.gpa_card)
        self.stats_layout.addWidget(self.avg_card)
        self.stats_layout.addWidget(self.credits_card)
        layout.addLayout(self.stats_layout)

        # 筛选栏
        filter_layout = QHBoxLayout()
        filter_label = QLabel("筛选:")
        filter_label.setObjectName("filterLabel")
        filter_layout.addWidget(filter_label)

        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["全部"] + SEMESTERS)
        self.filter_combo.currentTextChanged.connect(self.on_filter_changed)
        filter_layout.addWidget(self.filter_combo)

        filter_layout.addStretch()

        self.total_label = QLabel("共 0 门课程")
        filter_layout.addWidget(self.total_label)

        layout.addLayout(filter_layout)

        # 成绩表格
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "课程名称", "类型", "学分", "成绩", "学期"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.hideColumn(0)  # 隐藏ID列

        layout.addWidget(self.table)

        # 操作按钮
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        edit_btn = QPushButton("编辑")
        edit_btn.clicked.connect(self.edit_grade)
        btn_layout.addWidget(edit_btn)

        delete_btn = QPushButton("删除")
        delete_btn.clicked.connect(self.delete_grade)
        btn_layout.addWidget(delete_btn)

        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def load_data(self):
        grades = get_all_grades()
        stats = get_grade_stats()

        # 更新统计卡片
        self.gpa_card.set_value(stats['gpa'])
        self.avg_card.set_value(stats['weighted_avg'])
        self.credits_card.set_value(stats['total_credits'])

        # 筛选
        if self.current_filter != "全部":
            grades = [g for g in grades if g['semester'] == self.current_filter]

        # 更新表格
        self.table.setRowCount(len(grades))
        for row, grade in enumerate(grades):
            self.table.setItem(row, 0, QTableWidgetItem(str(grade['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(grade['course_name']))
            self.table.setItem(row, 2, QTableWidgetItem(grade['course_type']))
            self.table.setItem(row, 3, QTableWidgetItem(str(grade['credits'])))
            self.table.setItem(row, 4, QTableWidgetItem(str(grade['score'])))
            self.table.setItem(row, 5, QTableWidgetItem(grade['semester']))

        self.total_label.setText(f"共 {len(grades)} 门课程")

    def on_filter_changed(self, text):
        self.current_filter = text
        self.load_data()

    def add_grade(self):
        dialog = AddGradeDialog(self)
        if dialog.exec_():
            data = dialog.get_data()
            add_grade(**data)
            self.load_data()

    def edit_grade(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "提示", "请选择要编辑的成绩")
            return

        grade_id = int(self.table.item(row, 0).text())
        grades = get_all_grades()
        grade = next((g for g in grades if g['id'] == grade_id), None)

        dialog = AddGradeDialog(self, grade)
        if dialog.exec_():
            data = dialog.get_data()
            update_grade(grade_id, **data)
            self.load_data()

    def delete_grade(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "提示", "请选择要删除的成绩")
            return

        reply = QMessageBox.question(self, "确认删除",
                                      "确定要删除这条成绩记录吗?",
                                      QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            grade_id = int(self.table.item(row, 0).text())
            delete_grade(grade_id)
            self.load_data()

    def apply_theme(self):
        colors = theme_manager.colors
        self.setStyleSheet(f"""
            #pageTitle {{
                font-size: 24px;
                font-weight: bold;
                color: {colors['text_primary']};
            }}
            #filterLabel {{
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
            QPushButton:hover {{
                opacity: 0.9;
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
            QLabel {{
                color: {colors['text_secondary']};
            }}
        """)

    def on_theme_changed(self, theme_name):
        self.apply_theme()
        self.gpa_card.apply_theme()
        self.avg_card.apply_theme()
        self.credits_card.apply_theme()
