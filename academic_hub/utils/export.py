import os
import tempfile
from datetime import datetime
from jinja2 import Template
from xhtml2pdf import pisa
from io import BytesIO
from ..database import get_all_grades, get_all_honors, get_grade_stats, get_honor_stats, get_student_info

# 简历HTML模板
RESUME_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{{ student.name }} - 简历</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: "Microsoft YaHei", Arial, sans-serif; line-height: 1.6; color: #333; padding: 40px; }
        .header { text-align: center; margin-bottom: 30px; border-bottom: 2px solid #1E88E5; padding-bottom: 20px; }
        .header h1 { font-size: 28px; color: #1E88E5; margin-bottom: 10px; }
        .header .info { font-size: 14px; color: #666; }
        .section { margin-bottom: 25px; }
        .section h2 { font-size: 18px; color: #1E88E5; border-left: 4px solid #1E88E5; padding-left: 10px; margin-bottom: 15px; }
        .info-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; font-size: 14px; }
        .info-item { padding: 8px; background: #f5f5f5; border-radius: 4px; }
        .info-item strong { color: #1E88E5; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 13px; }
        th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
        th { background: #1E88E5; color: white; }
        tr:nth-child(even) { background: #f9f9f9; }
        .stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-bottom: 20px; }
        .stat-box { background: #f5f5f5; padding: 15px; border-radius: 8px; text-align: center; }
        .stat-box .value { font-size: 24px; font-weight: bold; color: #1E88E5; }
        .stat-box .label { font-size: 12px; color: #666; }
        .honor-list { list-style: none; }
        .honor-list li { padding: 8px 0; border-bottom: 1px solid #eee; }
        .honor-list .title { font-weight: bold; }
        .honor-list .meta { font-size: 12px; color: #888; }
    </style>
</head>
<body>
    <div class="header">
        <h1>{{ student.name }}</h1>
        <div class="info">
            {{ student.major }} | {{ student.grade }}级 | 学号: {{ student.student_id }}
        </div>
        <div class="info" style="margin-top: 5px;">
            {% if student.phone %}手机: {{ student.phone }}{% endif %}
            {% if student.email %} | 邮箱: {{ student.email }}{% endif %}
        </div>
    </div>

    <div class="section">
        <h2>学业概况</h2>
        <div class="stats">
            <div class="stat-box">
                <div class="value">{{ stats.gpa }}</div>
                <div class="label">GPA</div>
            </div>
            <div class="stat-box">
                <div class="value">{{ stats.weighted_avg }}</div>
                <div class="label">加权平均分</div>
            </div>
            <div class="stat-box">
                <div class="value">{{ stats.total_credits }}</div>
                <div class="label">已获学分</div>
            </div>
            <div class="stat-box">
                <div class="value">{{ honor_stats.total }}</div>
                <div class="label">荣誉奖项</div>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>成绩单 (部分)</h2>
        <table>
            <thead>
                <tr>
                    <th>学期</th>
                    <th>课程名称</th>
                    <th>类型</th>
                    <th>学分</th>
                    <th>成绩</th>
                </tr>
            </thead>
            <tbody>
                {% for grade in grades[:10] %}
                <tr>
                    <td>{{ grade.semester }}</td>
                    <td>{{ grade.course_name }}</td>
                    <td>{{ grade.course_type }}</td>
                    <td>{{ grade.credits }}</td>
                    <td>{{ grade.score }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

    <div class="section">
        <h2>荣誉奖励</h2>
        <ul class="honor-list">
            {% for honor in honors %}
            <li>
                <span class="title">{{ honor.title }}</span>
                <span class="meta"> - {{ honor.level }} | {{ honor.type }} | {{ honor.date }}</span>
            </li>
            {% endfor %}
        </ul>
    </div>
</body>
</html>
"""

def export_resume_pdf(output_path):
    """导出简历为PDF"""
    # 获取数据
    student = get_student_info()
    grades = get_all_grades()
    honors = get_all_honors()
    stats = get_grade_stats()
    honor_stats = get_honor_stats()

    # 如果没有学生信息，创建一个空的
    if not student:
        student = {
            "name": "未设置",
            "student_id": "未设置",
            "major": "未设置",
            "grade": "未设置",
            "phone": "",
            "email": ""
        }
    else:
        student = dict(student)

    # 渲染模板
    template = Template(RESUME_TEMPLATE)
    html_content = template.render(
        student=student,
        grades=grades,
        honors=honors,
        stats=stats,
        honor_stats=honor_stats
    )

    # 使用xhtml2pdf生成PDF
    with open(output_path, "wb") as pdf_file:
        pisa_status = pisa.CreatePDF(
            html_content,
            dest=pdf_file
        )

    return output_path
