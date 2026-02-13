from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QLineEdit, QComboBox, QPushButton, QTextEdit,
                             QLabel, QDialogButtonBox, QDateEdit)
from PyQt5.QtCore import Qt, QDate
from ..config import COURSE_TYPES, HONOR_TYPES, HONOR_LEVELS, SEMESTERS
from ..utils.theme import theme_manager
from ..database import get_student_info, save_student_info

class AddGradeDialog(QDialog):
    """添加/编辑成绩对话框"""

    def __init__(self, parent=None, grade_data=None):
        super().__init__(parent)
        self.grade_data = grade_data
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("添加成绩" if not self.grade_data else "编辑成绩")
        self.setMinimumWidth(400)

        layout = QFormLayout()

        # 课程名称
        self.course_name = QLineEdit()
        layout.addRow("课程名称:", self.course_name)

        # 课程类型
        self.course_type = QComboBox()
        self.course_type.addItems(COURSE_TYPES)
        layout.addRow("课程类型:", self.course_type)

        # 学分
        self.credits = QLineEdit()
        self.credits.setPlaceholderText("如: 3.0")
        layout.addRow("学分:", self.credits)

        # 成绩
        self.score = QLineEdit()
        self.score.setPlaceholderText("如: 85")
        layout.addRow("成绩:", self.score)

        # 学期
        self.semester = QComboBox()
        self.semester.addItems(SEMESTERS)
        layout.addRow("学期:", self.semester)

        # 按钮
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

        # 填充数据
        if self.grade_data:
            self.course_name.setText(self.grade_data['course_name'])
            self.course_type.setCurrentText(self.grade_data['course_type'])
            self.credits.setText(str(self.grade_data['credits']))
            self.score.setText(str(self.grade_data['score']))
            self.semester.setCurrentText(self.grade_data['semester'])

        self.setLayout(layout)
        self.apply_theme()

    def get_data(self):
        return {
            'course_name': self.course_name.text(),
            'course_type': self.course_type.currentText(),
            'credits': float(self.credits.text()) if self.credits.text() else 0,
            'score': float(self.score.text()) if self.score.text() else 0,
            'semester': self.semester.currentText()
        }

    def apply_theme(self):
        colors = theme_manager.colors
        self.setStyleSheet(f"""
            QDialog {{
                background: {colors['background']};
            }}
            QLabel {{
                color: {colors['text_primary']};
            }}
            QLineEdit, QComboBox, QTextEdit {{
                background: {colors['card']};
                color: {colors['text_primary']};
                border: 1px solid {colors['border']};
                padding: 6px;
                border-radius: 4px;
            }}
            QPushButton {{
                background: {colors['primary']};
                color: white;
                border: none;
                padding: 6px 16px;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                opacity: 0.9;
            }}
        """)

class AddHonorDialog(QDialog):
    """添加/编辑荣誉对话框"""

    def __init__(self, parent=None, honor_data=None):
        super().__init__(parent)
        self.honor_data = honor_data
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("添加荣誉" if not self.honor_data else "编辑荣誉")
        self.setMinimumWidth(450)

        layout = QFormLayout()

        # 荣誉名称
        self.title = QLineEdit()
        layout.addRow("荣誉名称:", self.title)

        # 类型
        self.type = QComboBox()
        self.type.addItems(HONOR_TYPES)
        layout.addRow("荣誉类型:", self.type)

        # 级别
        self.level = QComboBox()
        self.level.addItems(HONOR_LEVELS)
        layout.addRow("获奖级别:", self.level)

        # 日期
        self.date = QDateEdit()
        self.date.setCalendarPopup(True)
        self.date.setDate(QDate.currentDate())
        layout.addRow("获得日期:", self.date)

        # 描述
        self.description = QTextEdit()
        self.description.setPlaceholderText("可填写获奖说明...")
        self.description.setMinimumHeight(80)
        layout.addRow("描述:", self.description)

        # 按钮
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

        # 填充数据
        if self.honor_data:
            self.title.setText(self.honor_data['title'])
            self.type.setCurrentText(self.honor_data['type'])
            self.level.setCurrentText(self.honor_data['level'])
            self.date.setDate(QDate.fromString(self.honor_data['date'], "yyyy-MM-dd"))
            self.description.setText(self.honor_data['description'] or "")

        self.setLayout(layout)
        self.apply_theme()

    def get_data(self):
        return {
            'title': self.title.text(),
            'type': self.type.currentText(),
            'level': self.level.currentText(),
            'date': self.date.date().toString("yyyy-MM-dd"),
            'description': self.description.toPlainText()
        }

    def apply_theme(self):
        colors = theme_manager.colors
        self.setStyleSheet(f"""
            QDialog {{
                background: {colors['background']};
            }}
            QLabel {{
                color: {colors['text_primary']};
            }}
            QLineEdit, QComboBox, QTextEdit {{
                background: {colors['card']};
                color: {colors['text_primary']};
                border: 1px solid {colors['border']};
                padding: 6px;
                border-radius: 4px;
            }}
            QPushButton {{
                background: {colors['primary']};
                color: white;
                border: none;
                padding: 6px 16px;
                border-radius: 4px;
            }}
        """)

class StudentInfoDialog(QDialog):
    """学生信息对话框"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.load_data()

    def init_ui(self):
        self.setWindowTitle("学生信息")
        self.setMinimumWidth(400)

        layout = QFormLayout()

        self.name = QLineEdit()
        self.name.setPlaceholderText("请输入姓名")
        layout.addRow("姓名:", self.name)

        self.student_id = QLineEdit()
        self.student_id.setPlaceholderText("请输入学号")
        layout.addRow("学号:", self.student_id)

        self.major = QLineEdit()
        self.major.setPlaceholderText("请输入专业")
        layout.addRow("专业:", self.major)

        self.grade = QLineEdit()
        self.grade.setPlaceholderText("如: 2024")
        layout.addRow("年级:", self.grade)

        self.phone = QLineEdit()
        self.phone.setPlaceholderText("请输入手机号")
        layout.addRow("手机:", self.phone)

        self.email = QLineEdit()
        self.email.setPlaceholderText("请输入邮箱")
        layout.addRow("邮箱:", self.email)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.save)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

        self.setLayout(layout)
        self.apply_theme()

    def load_data(self):
        info = get_student_info()
        if info:
            self.name.setText(info['name'] or "")
            self.student_id.setText(info['student_id'] or "")
            self.major.setText(info['major'] or "")
            self.grade.setText(info['grade'] or "")
            self.phone.setText(info['phone'] or "")
            self.email.setText(info['email'] or "")

    def save(self):
        save_student_info(
            self.name.text(),
            self.student_id.text(),
            self.major.text(),
            self.grade.text(),
            self.phone.text(),
            self.email.text()
        )
        self.accept()

    def apply_theme(self):
        colors = theme_manager.colors
        self.setStyleSheet(f"""
            QDialog {{
                background: {colors['background']};
            }}
            QLabel {{
                color: {colors['text_primary']};
            }}
            QLineEdit {{
                background: {colors['card']};
                color: {colors['text_primary']};
                border: 1px solid {colors['border']};
                padding: 6px;
                border-radius: 4px;
            }}
            QPushButton {{
                background: {colors['primary']};
                color: white;
                border: none;
                padding: 6px 16px;
                border-radius: 4px;
            }}
        """)

class GraduationRequirementDialog(QDialog):
    """毕业要求设置对话框"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("设置毕业要求")
        self.setMinimumWidth(350)

        layout = QFormLayout()

        self.required_bixiu = QLineEdit()
        self.required_bixiu.setPlaceholderText("如: 60")
        layout.addRow("必修学分要求:", self.required_bixiu)

        self.required_xuanshuo = QLineEdit()
        self.required_xuanshuo.setPlaceholderText("如: 20")
        layout.addRow("选修学分要求:", self.required_xuanshuo)

        self.required_xuanxian = QLineEdit()
        self.required_xuanxian.setPlaceholderText("如: 15")
        layout.addRow("限选学分要求:", self.required_xuanxian)

        self.required_total = QLineEdit()
        self.required_total.setPlaceholderText("如: 160")
        layout.addRow("总学分要求:", self.required_total)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

        self.setLayout(layout)
        self.apply_theme()

    def apply_theme(self):
        colors = theme_manager.colors
        self.setStyleSheet(f"""
            QDialog {{
                background: {colors['background']};
            }}
            QLabel {{
                color: {colors['text_primary']};
            }}
            QLineEdit {{
                background: {colors['card']};
                color: {colors['text_primary']};
                border: 1px solid {colors['border']};
                padding: 6px;
                border-radius: 4px;
            }}
            QPushButton {{
                background: {colors['primary']};
                color: white;
                border: none;
                padding: 6px 16px;
                border-radius: 4px;
            }}
        """)
