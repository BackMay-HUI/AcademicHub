from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtChart import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis, QPieSeries, QLineSeries, QSplineSeries
from PyQt5.QtGui import QPainter, QColor, QBrush
from ..utils.theme import theme_manager
from ..database import get_all_grades, get_grade_stats

class GradeChartWidget(QWidget):
    """成绩图表组件"""

    def __init__(self):
        super().__init__()
        self.last_data_hash = None  # 用于检测数据变化
        self.init_ui()
        self.apply_theme()

        theme_manager.theme_changed.connect(self.on_theme_changed)

        # 设置定时器，每3秒自动刷新图表
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_and_refresh)
        self.timer.start(3000)

    def check_and_refresh(self):
        """检查数据是否变化，如有变化则刷新图表"""
        grades = get_all_grades()
        stats = get_grade_stats()

        # 计算数据hash来判断是否有变化
        current_hash = hash((
            tuple(sorted(g['score'] for g in grades)),
            tuple(sorted(stats.get('credits_by_type', {}).items()))
        ))

        if self.last_data_hash != current_hash:
            self.last_data_hash = current_hash
            self.load_data()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(16)

        # 学期成绩柱状图
        self.bar_chart_view = QChartView()
        self.bar_chart_view.setRenderHint(QPainter.Antialiasing)
        layout.addWidget(self.bar_chart_view)

        # 学分占比饼图
        self.pie_chart_view = QChartView()
        self.pie_chart_view.setRenderHint(QPainter.Antialiasing)
        layout.addWidget(self.pie_chart_view)

        self.setLayout(layout)
        self.load_data()

    def load_data(self):
        grades = get_all_grades()
        stats = get_grade_stats()

        # 按学期分组计算平均成绩
        semester_data = {}
        for grade in grades:
            semester = grade['semester']
            if semester not in semester_data:
                semester_data[semester] = []
            semester_data[semester].append(grade['score'])

        # 计算每学期平均分
        semesters = []
        avg_scores = []
        for semester in sorted(semester_data.keys()):
            semesters.append(semester)
            scores = semester_data[semester]
            avg_scores.append(sum(scores) / len(scores))

        # 创建柱状图
        self.create_bar_chart(semesters, avg_scores)

        # 创建饼图
        credits_by_type = stats.get('credits_by_type', {})
        self.create_pie_chart(credits_by_type)

    def create_bar_chart(self, categories, values):
        chart = QChart()
        chart.setTitle("各学期平均成绩")

        series = QBarSeries()
        bar_set = QBarSet("平均成绩")

        for v in values:
            bar_set.append(v)

        series.append(bar_set)
        chart.addSeries(series)

        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setRange(0, 100)
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)

        colors = theme_manager.colors
        chart.setBackgroundBrush(QBrush(QColor(colors['card'])))
        chart.setTitleBrush(QBrush(QColor(colors['text_primary'])))

        self.bar_chart_view.setChart(chart)
        self.bar_chart_view.setStyleSheet(f"""
            background: {colors['card']};
            border-radius: 8px;
        """)

    def create_pie_chart(self, data_dict):
        chart = QChart()
        chart.setTitle("学分占比")

        series = QPieSeries()
        colors_list = theme_manager.colors['chart_colors']

        for i, (label, value) in enumerate(data_dict.items()):
            if value > 0:
                slice_ = series.append(label, value)
                color_str = colors_list[i % len(colors_list)]
                slice_.setBrush(QBrush(QColor(color_str)))

        chart.addSeries(series)
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignRight)

        colors = theme_manager.colors
        chart.setBackgroundBrush(QBrush(QColor(colors['card'])))
        chart.setTitleBrush(QBrush(QColor(colors['text_primary'])))

        self.pie_chart_view.setChart(chart)
        self.pie_chart_view.setStyleSheet(f"""
            background: {colors['card']};
            border-radius: 8px;
        """)

    def apply_theme(self):
        colors = theme_manager.colors
        self.setStyleSheet(f"""
            GradeChartWidget {{
                background: {colors['card']};
                border-radius: 12px;
            }}
        """)
        self.load_data()

    def on_theme_changed(self, theme_name):
        self.apply_theme()

    def start_timer(self):
        """启动定时器（当切换到图表页面时调用）"""
        if not self.timer.isActive():
            self.timer.start(3000)
            # 立即刷新一次
            self.last_data_hash = None
            self.load_data()

    def stop_timer(self):
        """停止定时器（当离开图表页面时调用）"""
        if self.timer.isActive():
            self.timer.stop()
