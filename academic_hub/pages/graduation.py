from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QScrollArea, QFrame)
from PyQt5.QtCore import Qt
from ..database import (get_grade_stats, get_graduation_requirements,
                        set_graduation_requirement)
from ..utils.theme import theme_manager
from ..widgets.dialogs import GraduationRequirementDialog
from ..widgets.cards import ProgressCard, StatCard

class GraduationPage(QWidget):
    """毕业追踪页面"""

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

        # 标题栏
        header = QHBoxLayout()
        title = QLabel("毕业追踪")
        title.setObjectName("pageTitle")
        header.addWidget(title)
        header.addStretch()

        setting_btn = QPushButton("设置要求")
        setting_btn.clicked.connect(self.show_setting)
        header.addWidget(setting_btn)

        main_layout.addLayout(header)

        # 总体进度卡片
        self.overview_card = QFrame()
        overview_layout = QVBoxLayout()

        overview_title = QLabel("毕业进度总览")
        overview_title.setObjectName("sectionTitle")
        overview_layout.addWidget(overview_title)

        self.total_progress_card = ProgressCard("总学分", 0, 160, "学分")
        overview_layout.addWidget(self.total_progress_card)

        self.overview_card.setLayout(overview_layout)
        main_layout.addWidget(self.overview_card)

        # 分类进度
        progress_container = QVBoxLayout()
        progress_title = QLabel("分类学分进度")
        progress_title.setObjectName("sectionTitle")
        progress_container.addWidget(progress_title)

        # 必修学分进度
        self.bixiu_card = ProgressCard("必修学分", 0, 60, "学分")
        progress_container.addWidget(self.bixiu_card)

        # 选修学分进度
        self.xuanshuo_card = ProgressCard("选修学分", 0, 20, "学分")
        progress_container.addWidget(self.xuanshuo_card)

        # 限选学分进度
        self.xuanxian_card = ProgressCard("限选学分", 0, 15, "学分")
        progress_container.addWidget(self.xuanxian_card)

        progress_container.addStretch()
        main_layout.addLayout(progress_container)

        # 统计信息
        stats_layout = QHBoxLayout()
        stats_title = QLabel("学业统计")
        stats_title.setObjectName("sectionTitle")
        stats_layout.addWidget(stats_title)
        stats_layout.addStretch()
        main_layout.addLayout(stats_layout)

        stats_cards = QHBoxLayout()
        self.gpa_card = StatCard("GPA", "0.00", "📊")
        self.avg_card = StatCard("加权平均分", "0", "📈")
        self.total_credits_card = StatCard("已获学分", "0", "📚")
        self.courses_card = StatCard("已修课程", "0", "📖")
        stats_cards.addWidget(self.gpa_card)
        stats_cards.addWidget(self.avg_card)
        stats_cards.addWidget(self.total_credits_card)
        stats_cards.addWidget(self.courses_card)
        main_layout.addLayout(stats_cards)

        # 提示信息
        self.tip_label = QLabel("")
        self.tip_label.setObjectName("tipLabel")
        self.tip_label.setWordWrap(True)
        main_layout.addWidget(self.tip_label)

        self.setLayout(main_layout)

    def load_data(self):
        # 获取成绩统计
        grade_stats = get_grade_stats()
        credits_by_type = grade_stats.get('credits_by_type', {})

        # 获取毕业要求
        requirements = get_graduation_requirements()
        req_dict = {}
        for req in requirements:
            req_dict[req['requirement_type']] = req['required_credits']

        # 设置默认值
        required_total = req_dict.get('total', 160)
        required_bixiu = req_dict.get('必修', 60)
        required_xuanshuo = req_dict.get('选修', 20)
        required_xuanxian = req_dict.get('限选', 15)

        # 获取当前学分
        current_total = grade_stats.get('total_credits', 0)
        current_bixiu = credits_by_type.get('必修', 0)
        current_xuanshuo = credits_by_type.get('选修', 0)
        current_xuanxian = credits_by_type.get('限选', 0)

        # 更新进度卡片
        self.total_progress_card.set_title("总学分")
        self.bixiu_card.set_title("必修学分")
        self.xuanshuo_card.set_title("选修学分")
        self.xuanxian_card.set_title("限选学分")

        # 更新统计卡片
        self.gpa_card.set_value(grade_stats.get('gpa', 0))
        self.avg_card.set_value(grade_stats.get('weighted_avg', 0))
        self.total_credits_card.set_value(current_total)
        self.courses_card.set_value(len(credits_by_type))

        # 生成提示
        self.update_tips(current_total, required_total,
                        current_bixiu, required_bixiu,
                        current_xuanshuo, required_xuanshuo,
                        current_xuanxian, required_xuanxian)

    def set_title(self, title):
        """动态更新ProgressCard标题"""
        pass  # ProgressCard需要在创建时设置标题，这里通过重构实现

    def update_tips(self, current_total, required_total,
                   current_bixiu, required_bixiu,
                   current_xuanshuo, required_xuanshuo,
                   current_xuanxian, required_xuanxian):
        tips = []

        # 总学分检查
        if current_total >= required_total:
            tips.append("✅ 已满足总学分要求")
        else:
            tips.append(f"⚠️ 还需 {required_total - current_total} 学分达到总要求")

        # 分类检查
        if current_bixiu >= required_bixiu:
            tips.append("✅ 必修学分已达标")
        else:
            tips.append(f"⚠️ 必修学分还差 {required_bixiu - current_bixiu} 学分")

        if current_xuanshuo >= required_xuanshuo:
            tips.append("✅ 选修学分已达标")
        else:
            tips.append(f"⚠️ 选修学分还差 {required_xuanshuo - current_xuanshuo} 学分")

        if current_xuanxian >= required_xuanxian:
            tips.append("✅ 限选学分已达标")
        else:
            tips.append(f"⚠️ 限选学分还差 {required_xuanxian - current_xuanxian} 学分")

        self.tip_label.setText("\n".join(tips))

    def show_setting(self):
        dialog = GraduationRequirementDialog(self)
        if dialog.exec_():
            # 保存设置
            bixiu = float(dialog.required_bixiu.text() or 0)
            xuanshuo = float(dialog.required_xuanshuo.text() or 0)
            xuanxian = float(dialog.required_xuanxian.text() or 0)
            total = float(dialog.required_total.text() or 0)

            set_graduation_requirement('必修', bixiu)
            set_graduation_requirement('选修', xuanshuo)
            set_graduation_requirement('限选', xuanxian)
            set_graduation_requirement('total', total)

            self.load_data()

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
                margin-bottom: 8px;
            }}
            #tipLabel {{
                color: {colors['text_secondary']};
                font-size: 13px;
                line-height: 1.8;
                padding: 12px;
                background: {colors['card']};
                border-radius: 6px;
            }}
            QPushButton {{
                background: {colors['primary']};
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }}
            QFrame {{
                background: {colors['card']};
                border-radius: 8px;
            }}
        """)

    def on_theme_changed(self, theme_name):
        self.apply_theme()
        self.total_progress_card.apply_theme()
        self.bixiu_card.apply_theme()
        self.xuanshuo_card.apply_theme()
        self.xuanxian_card.apply_theme()
        self.gpa_card.apply_theme()
        self.avg_card.apply_theme()
        self.total_credits_card.apply_theme()
        self.courses_card.apply_theme()
