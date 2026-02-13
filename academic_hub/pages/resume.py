from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame, QMessageBox, QFileDialog,
                             QFormLayout, QLineEdit, QTextEdit, QScrollArea)
from PyQt5.QtCore import Qt
from ..database import (get_student_info, save_student_info,
                        get_grade_stats, get_honor_stats,
                        get_all_grades, get_all_honors)
from ..utils.theme import theme_manager
from ..utils.export import export_resume_pdf
from ..widgets.dialogs import StudentInfoDialog

class ResumePage(QWidget):
    """简历导出页面"""

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_data()
        self.apply_theme()

        theme_manager.theme_changed.connect(self.on_theme_changed)

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(16)

        # 标题
        title = QLabel("简历导出")
        title.setObjectName("pageTitle")
        main_layout.addWidget(title)

        # 提示信息
        tip = QLabel("生成一份包含您的学业成绩、荣誉奖励等信息的专业简历")
        tip.setObjectName("tipLabel")
        main_layout.addWidget(tip)

        # 学生信息卡片
        info_card = QFrame()
        info_layout = QVBoxLayout()

        info_header = QHBoxLayout()
        info_title = QLabel("学生信息")
        info_title.setObjectName("sectionTitle")
        info_header.addWidget(info_title)
        info_header.addStretch()

        edit_info_btn = QPushButton("编辑信息")
        edit_info_btn.clicked.connect(self.edit_student_info)
        info_header.addWidget(edit_info_btn)

        info_layout.addLayout(info_header)

        # 信息展示
        self.info_form = QFormLayout()
        self.name_label = QLabel("-")
        self.student_id_label = QLabel("-")
        self.major_label = QLabel("-")
        self.grade_label = QLabel("-")
        self.phone_label = QLabel("-")
        self.email_label = QLabel("-")

        self.info_form.addRow("姓名:", self.name_label)
        self.info_form.addRow("学号:", self.student_id_label)
        self.info_form.addRow("专业:", self.major_label)
        self.info_form.addRow("年级:", self.grade_label)
        self.info_form.addRow("手机:", self.phone_label)
        self.info_form.addRow("邮箱:", self.email_label)

        info_layout.addLayout(self.info_form)
        info_card.setLayout(info_layout)
        main_layout.addWidget(info_card)

        # 学业概况卡片
        stats_card = QFrame()
        stats_layout = QVBoxLayout()

        stats_title = QLabel("学业概况预览")
        stats_title.setObjectName("sectionTitle")
        stats_layout.addWidget(stats_title)

        self.stats_form = QFormLayout()
        self.gpa_label = QLabel("-")
        self.avg_score_label = QLabel("-")
        self.credits_label = QLabel("-")
        self.honors_label = QLabel("-")

        self.stats_form.addRow("GPA:", self.gpa_label)
        self.stats_form.addRow("加权平均分:", self.avg_score_label)
        self.stats_form.addRow("已获学分:", self.credits_label)
        self.stats_form.addRow("荣誉数量:", self.honors_label)

        stats_layout.addLayout(self.stats_form)
        stats_card.setLayout(stats_layout)
        main_layout.addWidget(stats_card)

        # 导出按钮
        export_btn = QPushButton("导出PDF简历")
        export_btn.setObjectName("exportButton")
        export_btn.clicked.connect(self.export_pdf)
        main_layout.addWidget(export_btn)

        # 底部提示
        footer = QLabel("提示: 请先完善学生信息，以确保简历内容完整")
        footer.setObjectName("footerLabel")
        main_layout.addWidget(footer)

        self.setLayout(main_layout)

    def load_data(self):
        # 加载学生信息
        student = get_student_info()
        if student:
            self.name_label.setText(student['name'] or "-")
            self.student_id_label.setText(student['student_id'] or "-")
            self.major_label.setText(student['major'] or "-")
            self.grade_label.setText(student['grade'] or "-")
            self.phone_label.setText(student['phone'] or "-")
            self.email_label.setText(student['email'] or "-")
        else:
            self.name_label.setText("-")
            self.student_id_label.setText("-")
            self.major_label.setText("-")
            self.grade_label.setText("-")
            self.phone_label.setText("-")
            self.email_label.setText("-")

        # 加载学业统计
        grade_stats = get_grade_stats()
        honor_stats = get_honor_stats()

        self.gpa_label.setText(str(grade_stats.get('gpa', 0)))
        self.avg_score_label.setText(str(grade_stats.get('weighted_avg', 0)))
        self.credits_label.setText(str(grade_stats.get('total_credits', 0)))
        self.honors_label.setText(str(honor_stats.get('total', 0)))

    def edit_student_info(self):
        dialog = StudentInfoDialog(self)
        if dialog.exec_():
            self.load_data()

    def export_pdf(self):
        # 检查是否有学生信息
        student = get_student_info()
        if not student or not student['name']:
            reply = QMessageBox.question(self, "提示",
                                          "学生信息未完善，是否先编辑信息?",
                                          QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.edit_student_info()
                return

        # 选择保存路径
        default_name = f"{student['name'] if student and student['name'] else '简历'}.pdf"
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存简历", default_name, "PDF文件 (*.pdf)"
        )

        if file_path:
            try:
                export_resume_pdf(file_path)
                QMessageBox.information(self, "导出成功",
                                        f"简历已导出到:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "导出失败",
                                    f"导出时发生错误:\n{str(e)}")

    def apply_theme(self):
        colors = theme_manager.colors
        self.setStyleSheet(f"""
            #pageTitle {{
                font-size: 24px;
                font-weight: bold;
                color: {colors['text_primary']};
            }}
            #tipLabel {{
                color: {colors['text_secondary']};
                font-size: 13px;
            }}
            #sectionTitle {{
                font-size: 16px;
                font-weight: bold;
                color: {colors['text_primary']};
                margin-bottom: 12px;
            }}
            #exportButton {{
                background: {colors['primary']};
                color: white;
                border: none;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 6px;
            }}
            #exportButton:hover {{
                opacity: 0.9;
            }}
            #footerLabel {{
                color: {colors['text_secondary']};
                font-size: 12px;
            }}
            QFrame {{
                background: {colors['card']};
                border: 1px solid {colors['border']};
                border-radius: 8px;
                padding: 16px;
            }}
            QLabel {{
                color: {colors['text_primary']};
            }}
            QPushButton {{
                background: {colors['primary']};
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
            }}
        """)

    def on_theme_changed(self, theme_name):
        self.apply_theme()
