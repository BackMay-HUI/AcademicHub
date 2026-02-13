from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QLineEdit, QFormLayout, QFrame,
                             QTextEdit, QScrollArea, QComboBox, QSlider)
from PyQt5.QtCore import Qt
from ..database import get_grade_stats, get_honor_stats, get_all_honors
from ..utils.theme import theme_manager

class GraduatePage(QWidget):
    """保研模拟页面"""

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.apply_theme()

        theme_manager.theme_changed.connect(self.on_theme_changed)

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(16)

        # 标题
        title = QLabel("保研模拟")
        title.setObjectName("pageTitle")
        main_layout.addWidget(title)

        # 内容区域 - 横向布局
        content_layout = QHBoxLayout()

        # 左侧: 输入参数
        input_frame = QFrame()
        input_layout = QVBoxLayout()

        input_title = QLabel("输入目标院校要求")
        input_title.setObjectName("sectionTitle")
        input_layout.addWidget(input_title)

        # 目标院校
        form = QFormLayout()
        self.target_school = QLineEdit()
        self.target_school.setPlaceholderText("如: 清华大学")
        form.addRow("目标院校:", self.target_school)

        # 绩点要求
        self.gpa_requirement = QComboBox()
        self.gpa_requirement.addItems(["3.0", "3.2", "3.4", "3.5", "3.6", "3.7", "3.8", "4.0"])
        self.gpa_requirement.setCurrentText("3.5")
        form.addRow("绩点要求:", self.gpa_requirement)

        # 排名要求
        self.rank_requirement = QLineEdit()
        self.rank_requirement.setPlaceholderText("如: 10%")
        form.addRow("排名要求:", self.rank_requirement)

        # 计算按钮
        calc_btn = QPushButton("开始模拟")
        calc_btn.clicked.connect(self.calculate)
        form.addRow("", calc_btn)

        input_layout.addLayout(form)
        input_frame.setLayout(input_layout)
        content_layout.addWidget(input_frame, 1)

        # 右侧: 模拟结果
        result_frame = QFrame()
        result_layout = QVBoxLayout()

        result_title = QLabel("模拟结果")
        result_title.setObjectName("sectionTitle")
        result_layout.addWidget(result_title)

        # 得分显示
        score_layout = QVBoxLayout()
        self.total_score_label = QLabel("0")
        self.total_score_label.setObjectName("totalScore")
        self.total_score_label.setAlignment(Qt.AlignCenter)

        score_desc = QLabel("竞争力得分")
        score_desc.setAlignment(Qt.AlignCenter)

        score_layout.addWidget(self.total_score_label)
        score_layout.addWidget(score_desc)
        result_layout.addLayout(score_layout)

        # 进度条
        self.score_bar = QFrame()
        self.score_bar.setFixedHeight(12)
        self.score_bar.setObjectName("scoreBarBg")
        self.score_inner = QFrame(self.score_bar)
        self.score_inner.setFixedHeight(12)
        self.score_inner.setObjectName("scoreBarInner")
        result_layout.addWidget(self.score_bar)

        # 详细分数
        detail_layout = QFormLayout()
        self.gpa_score_label = QLabel("0 / 80")
        self.honor_score_label = QLabel("0 / 10")
        self.competition_score_label = QLabel("0 / 10")

        detail_layout.addRow("绩点基础分:", self.gpa_score_label)
        detail_layout.addRow("荣誉加分:", self.honor_score_label)
        detail_layout.addRow("竞赛加分:", self.competition_score_label)
        result_layout.addLayout(detail_layout)

        # 评估结果
        self.evaluation_label = QLabel("")
        self.evaluation_label.setObjectName("evaluationLabel")
        self.evaluation_label.setWordWrap(True)
        result_layout.addWidget(self.evaluation_label)

        result_frame.setLayout(result_layout)
        content_layout.addWidget(result_frame, 1)

        main_layout.addLayout(content_layout)

        # 提升建议
        suggestion_frame = QFrame()
        suggestion_layout = QVBoxLayout()

        suggestion_title = QLabel("提升建议")
        suggestion_title.setObjectName("sectionTitle")
        suggestion_layout.addWidget(suggestion_title)

        self.suggestion_text = QLabel("添加成绩和荣誉后，点击\"开始模拟\"查看建议")
        self.suggestion_text.setWordWrap(True)
        self.suggestion_text.setObjectName("suggestionText")
        suggestion_layout.addWidget(self.suggestion_text)

        suggestion_frame.setLayout(suggestion_layout)
        main_layout.addWidget(suggestion_frame)

        self.setLayout(main_layout)

    def calculate(self):
        # 获取当前数据
        grade_stats = get_grade_stats()
        honor_stats = get_honor_stats()
        honors = get_all_honors()

        # 计算各项得分
        # 基础分: GPA * 20 (满分80)
        gpa = grade_stats.get('gpa', 0)
        gpa_score = min(gpa * 20, 80)

        # 荣誉加分: 国家级+5, 省级+3, 校级+1 (满分10)
        honor_score = 0
        competition_score = 0

        by_level = honor_stats.get('by_level', {})
        by_type = honor_stats.get('by_type', {})

        for honor in honors:
            level = honor['level']
            htype = honor['type']
            if htype == '竞赛获奖':
                if level == '国家级':
                    competition_score += 5
                elif level == '省级':
                    competition_score += 3
                else:
                    competition_score += 2
            else:
                if level == '国家级':
                    honor_score += 5
                elif level == '省级':
                    honor_score += 3
                else:
                    honor_score += 1

        # 限制最高分
        honor_score = min(honor_score, 10)
        competition_score = min(competition_score, 10)

        # 总分
        total_score = gpa_score + honor_score + competition_score

        # 更新界面
        self.total_score_label.setText(str(total_score))
        self.gpa_score_label.setText(f"{gpa_score:.1f} / 80")
        self.honor_score_label.setText(f"{honor_score} / 10")
        self.competition_score_label.setText(f"{competition_score} / 10")

        # 进度条
        bar_width = self.score_bar.width()
        inner_width = int((total_score / 100) * bar_width) if bar_width > 0 else 0
        self.score_inner.setFixedWidth(inner_width)

        # 评估结果
        target_gpa = float(self.gpa_requirement.currentText())
        self.evaluate(total_score, gpa, target_gpa, grade_stats, honor_stats)

        # 生成建议
        self.generate_suggestions(gpa, target_gpa, honor_stats)

    def evaluate(self, total_score, current_gpa, target_gpa, grade_stats, honor_stats):
        target_school = self.target_school.text() or "目标院校"

        if total_score >= 90:
            evaluation = f"🎉 竞争力极强! 您的综合得分{total_score}分，有很大机会获得{target_school}的保研资格。"
        elif total_score >= 75:
            evaluation = f"💪 竞争力较强。您的综合得分{total_score}分，有较大机会获得{target_school}的保研资格。"
        elif total_score >= 60:
            evaluation = f"⚠️ 竞争力一般。您的综合得分{total_score}分，需要继续提升才能达到{target_school}的要求。"
        else:
            evaluation = f"❌ 竞争力不足。您的综合得分{total_score}分，建议提升成绩或增加荣誉来提高竞争力。"

        self.evaluation_label.setText(evaluation)

    def generate_suggestions(self, current_gpa, target_gpa, honor_stats):
        suggestions = []

        # GPA建议
        if current_gpa < target_gpa:
            gap = target_gpa - current_gpa
            suggestions.append(f"1. 建议提升GPA {gap:.2f} 分以上，可通过提高课程成绩来实现")

        # 荣誉建议
        total_honors = honor_stats.get('total', 0)
        if total_honors < 5:
            suggestions.append("2. 建议多参加各类竞赛和评选活动，增加荣誉数量")

        national_honors = honor_stats.get('by_level', {}).get('国家级', 0)
        if national_honors == 0:
            suggestions.append("3. 建议争取国家级奖项，如国家级学科竞赛等")

        # 综合建议
        if not suggestions:
            suggestions.append("✅ 您的各项指标良好，继续保持!")

        self.suggestion_text.setText("\n".join(suggestions))

    def apply_theme(self):
        colors = theme_manager.colors
        self.setStyleSheet(f"""
            #pageTitle {{
                font-size: 24px;
                font-weight: bold;
                color: {colors['text_primary']};
            }}
            #sectionTitle {{
                font-size: 16px;
                font-weight: bold;
                color: {colors['text_primary']};
                margin-bottom: 12px;
            }}
            #totalScore {{
                font-size: 48px;
                font-weight: bold;
                color: {colors['primary']};
            }}
            #evaluationLabel {{
                color: {colors['text_primary']};
                font-size: 14px;
                padding: 12px;
                background: {colors['background']};
                border-radius: 6px;
            }}
            #suggestionText {{
                color: {colors['text_secondary']};
                font-size: 13px;
                line-height: 1.6;
            }}
            QFrame {{
                background: {colors['card']};
                border: 1px solid {colors['border']};
                border-radius: 8px;
                padding: 16px;
            }}
            QPushButton {{
                background: {colors['primary']};
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-weight: bold;
            }}
            QLineEdit, QComboBox {{
                background: {colors['background']};
                color: {colors['text_primary']};
                border: 1px solid {colors['border']};
                padding: 8px;
                border-radius: 4px;
            }}
            #scoreBarBg {{
                background: {colors['border']};
                border-radius: 6px;
            }}
            #scoreBarInner {{
                background: {colors['primary']};
                border-radius: 6px;
            }}
            QLabel {{
                color: {colors['text_primary']};
            }}
        """)

    def on_theme_changed(self, theme_name):
        self.apply_theme()
