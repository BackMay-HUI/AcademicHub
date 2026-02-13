import sqlite3
from contextlib import contextmanager
from .config import DB_PATH, get_gpa_method, get_custom_gpa

def init_db():
    """初始化数据库表"""
    with get_db() as conn:
        cursor = conn.cursor()

        # 成绩表 - 添加gpa字段
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS grades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_name TEXT NOT NULL,
                course_type TEXT NOT NULL,
                credits REAL NOT NULL,
                score REAL NOT NULL,
                gpa REAL,
                semester TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 检查gpa列是否存在，不存在则添加
        cursor.execute("PRAGMA table_info(grades)")
        columns = [row[1] for row in cursor.fetchall()]
        if 'gpa' not in columns:
            cursor.execute("ALTER TABLE grades ADD COLUMN gpa REAL")

        # 荣誉表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS honors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                type TEXT NOT NULL,
                level TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 毕业要求表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS graduation_requirements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                requirement_type TEXT NOT NULL,
                required_credits REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 笔记表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT,
                category TEXT,
                tags TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 学生信息表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS student_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                student_id TEXT,
                major TEXT,
                grade TEXT,
                phone TEXT,
                email TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()

@contextmanager
def get_db():
    """获取数据库连接"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

# ===== 成绩操作 =====
def add_grade(course_name, course_type, credits, score, semester, gpa=None):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO grades (course_name, course_type, credits, score, gpa, semester) VALUES (?, ?, ?, ?, ?, ?)",
            (course_name, course_type, credits, score, gpa, semester)
        )
        conn.commit()
        return cursor.lastrowid

def get_all_grades():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, course_name, course_type, credits, score, gpa, semester, created_at FROM grades ORDER BY semester DESC, created_at DESC")
        return cursor.fetchall()

def update_grade(id, course_name, course_type, credits, score, semester, gpa=None):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE grades SET course_name=?, course_type=?, credits=?, score=?, gpa=?, semester=? WHERE id=?",
            (course_name, course_type, credits, score, gpa, semester, id)
        )
        conn.commit()

def delete_grade(id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM grades WHERE id=?", (id,))
        conn.commit()

# ===== 荣誉操作 =====
def add_honor(title, type, level, date, description):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO honors (title, type, level, date, description) VALUES (?, ?, ?, ?, ?)",
            (title, type, level, date, description)
        )
        conn.commit()
        return cursor.lastrowid

def get_all_honors():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM honors ORDER BY date DESC")
        return cursor.fetchall()

def update_honor(id, title, type, level, date, description):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE honors SET title=?, type=?, level=?, date=?, description=? WHERE id=?",
            (title, type, level, date, description, id)
        )
        conn.commit()

def delete_honor(id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM honors WHERE id=?", (id,))
        conn.commit()

# ===== 毕业要求操作 =====
def get_graduation_requirements():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM graduation_requirements")
        return cursor.fetchall()

def set_graduation_requirement(requirement_type, required_credits):
    with get_db() as conn:
        cursor = conn.cursor()
        # 检查是否存在
        cursor.execute("SELECT id FROM graduation_requirements WHERE requirement_type=?", (requirement_type,))
        existing = cursor.fetchone()
        if existing:
            cursor.execute("UPDATE graduation_requirements SET required_credits=? WHERE requirement_type=?",
                          (required_credits, requirement_type))
        else:
            cursor.execute("INSERT INTO graduation_requirements (requirement_type, required_credits) VALUES (?, ?)",
                          (requirement_type, required_credits))
        conn.commit()

# ===== 笔记操作 =====
def add_note(title, content, category, tags):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO notes (title, content, category, tags) VALUES (?, ?, ?, ?)",
            (title, content, category, tags)
        )
        conn.commit()
        return cursor.lastrowid

def get_all_notes():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM notes ORDER BY updated_at DESC")
        return cursor.fetchall()

def update_note(id, title, content, category, tags):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE notes SET title=?, content=?, category=?, tags=?, updated_at=CURRENT_TIMESTAMP WHERE id=?",
            (title, content, category, tags, id)
        )
        conn.commit()

def delete_note(id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM notes WHERE id=?", (id,))
        conn.commit()

# ===== 学生信息操作 =====
def get_student_info():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM student_info ORDER BY id DESC LIMIT 1")
        return cursor.fetchone()

def save_student_info(name, student_id, major, grade, phone, email):
    with get_db() as conn:
        cursor = conn.cursor()
        # 检查是否存在
        cursor.execute("SELECT id FROM student_info LIMIT 1")
        existing = cursor.fetchone()
        if existing:
            cursor.execute(
                "UPDATE student_info SET name=?, student_id=?, major=?, grade=?, phone=?, email=?, updated_at=CURRENT_TIMESTAMP WHERE id=?",
                (name, student_id, major, grade, phone, email, existing[0])
            )
        else:
            cursor.execute(
                "INSERT INTO student_info (name, student_id, major, grade, phone, email) VALUES (?, ?, ?, ?, ?, ?)",
                (name, student_id, major, grade, phone, email)
            )
        conn.commit()

# ===== 统计查询 =====
def get_grade_stats():
    with get_db() as conn:
        cursor = conn.cursor()

        # 总学分
        cursor.execute("SELECT SUM(credits) FROM grades")
        total_credits = cursor.fetchone()[0] or 0

        # 各类型学分
        cursor.execute("""
            SELECT course_type, SUM(credits) as total
            FROM grades
            GROUP BY course_type
        """)
        credits_by_type = {row[0]: row[1] for row in cursor.fetchall()}

        # 获取所有成绩用于GPA计算 - 包含gpa字段
        cursor.execute("SELECT credits, score, gpa FROM grades")
        grades = cursor.fetchall()

        # GPA计算: Σ(绩点 × 学分) / Σ学分
        def score_to_gpa_standard(score):
            """标准绩点转换"""
            if score >= 90:
                return 4.0
            elif score >= 85:
                return 3.7
            elif score >= 82:
                return 3.3
            elif score >= 78:
                return 3.0
            elif score >= 75:
                return 2.7
            elif score >= 72:
                return 2.3
            elif score >= 68:
                return 2.0
            elif score >= 64:
                return 1.3
            elif score >= 60:
                return 1.0
            else:
                return 0.0

        def score_to_gpa_custom(score):
            """自定义绩点转换"""
            custom_gpa = get_custom_gpa()
            for range_str, gpa_value in custom_gpa.items():
                parts = range_str.split('-')
                if len(parts) == 2:
                    max_score = int(parts[0])
                    min_score = int(parts[1])
                    if min_score <= score <= max_score:
                        return float(gpa_value)
            return 0.0

        # 根据配置选择GPA计算方法
        gpa_method = get_gpa_method()
        if gpa_method == "custom":
            score_to_gpa = score_to_gpa_custom
        else:
            score_to_gpa = score_to_gpa_standard

        total_grade_points = 0
        total_gpa_credits = 0
        weighted_avg = 0
        if grades:
            for credit, score, gpa in grades:
                # 优先使用直接输入的绩点，如果没有则根据分数计算
                if gpa is not None:
                    grade_gpa = float(gpa)
                else:
                    grade_gpa = score_to_gpa(score)
                total_grade_points += grade_gpa * credit
                total_gpa_credits += credit
                weighted_avg += score * credit

            gpa = total_grade_points / total_gpa_credits if total_gpa_credits > 0 else 0
            weighted_avg = weighted_avg / total_gpa_credits if total_gpa_credits > 0 else 0
        else:
            gpa = 0
            weighted_avg = 0

        return {
            "total_credits": total_credits,
            "credits_by_type": credits_by_type,
            "gpa": round(gpa, 2),
            "weighted_avg": round(weighted_avg, 2)
        }

def get_honor_stats():
    with get_db() as conn:
        cursor = conn.cursor()

        # 各类型荣誉数量
        cursor.execute("""
            SELECT type, COUNT(*) as count
            FROM honors
            GROUP BY type
        """)
        by_type = {row[0]: row[1] for row in cursor.fetchall()}

        # 各级别荣誉数量
        cursor.execute("""
            SELECT level, COUNT(*) as count
            FROM honors
            GROUP BY level
        """)
        by_level = {row[0]: row[1] for row in cursor.fetchall()}

        # 总数
        cursor.execute("SELECT COUNT(*) FROM honors")
        total = cursor.fetchone()[0]

        return {
            "total": total,
            "by_type": by_type,
            "by_level": by_level
        }

# ===== 数据导入/导出 =====
import csv
import json
import os

def export_grades_to_csv(file_path):
    """导出成绩到CSV文件"""
    grades = get_all_grades()
    with open(file_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['课程名称', '类型', '学分', '成绩', '绩点', '学期'])
        for grade in grades:
            writer.writerow([
                grade['course_name'],
                grade['course_type'],
                grade['credits'],
                grade['score'],
                grade['gpa'] or '',
                grade['semester']
            ])

def import_grades_from_csv(file_path):
    """从CSV文件导入成绩"""
    imported_count = 0
    errors = []
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        next(reader)  # 跳过表头
        for row in reader:
            if len(row) >= 6:
                try:
                    course_name = row[0].strip()
                    course_type = row[1].strip()
                    credits = float(row[2])
                    score = float(row[3])
                    gpa = float(row[4]) if row[4].strip() else None
                    semester = row[5].strip()
                    add_grade(course_name, course_type, credits, score, semester, gpa)
                    imported_count += 1
                except Exception as e:
                    errors.append(f"行 {row}: {str(e)}")
    return imported_count, errors

def export_all_data(file_path):
    """导出所有数据为JSON备份"""
    data = {
        'grades': [dict(row) for row in get_all_grades()],
        'honors': [dict(row) for row in get_all_honors()],
        'notes': [dict(row) for row in get_all_notes()],
        'graduation_requirements': [dict(row) for row in get_graduation_requirements()],
        'student_info': dict(get_all_grades()) if get_all_grades() else {}
    }

    # 添加学生信息
    student = get_student_info()
    if student:
        data['student_info'] = dict(student)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def import_all_data(file_path):
    """从JSON备份导入所有数据"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    with get_db() as conn:
        cursor = conn.cursor()

        # 导入成绩
        if 'grades' in data:
            for grade in data['grades']:
                cursor.execute(
                    "INSERT INTO grades (course_name, course_type, credits, score, gpa, semester) VALUES (?, ?, ?, ?, ?, ?)",
                    (grade['course_name'], grade['course_type'], grade['credits'], grade['score'], grade.get('gpa'), grade['semester'])
                )

        # 导入荣誉
        if 'honors' in data:
            for honor in data['honors']:
                cursor.execute(
                    "INSERT INTO honors (title, type, level, date, description) VALUES (?, ?, ?, ?, ?)",
                    (honor['title'], honor['type'], honor['level'], honor['date'], honor.get('description'))
                )

        # 导入笔记
        if 'notes' in data:
            for note in data['notes']:
                cursor.execute(
                    "INSERT INTO notes (title, content, category, tags) VALUES (?, ?, ?, ?)",
                    (note['title'], note.get('content'), note.get('category'), note.get('tags'))
                )

        # 导入毕业要求
        if 'graduation_requirements' in data:
            for req in data['graduation_requirements']:
                cursor.execute(
                    "INSERT INTO graduation_requirements (requirement_type, required_credits) VALUES (?, ?)",
                    (req['requirement_type'], req['required_credits'])
                )

        # 导入学生信息
        if 'student_info' in data and data['student_info']:
            info = data['student_info']
            cursor.execute(
                "INSERT INTO student_info (name, student_id, major, grade, phone, email) VALUES (?, ?, ?, ?, ?, ?)",
                (info.get('name'), info.get('student_id'), info.get('major'), info.get('grade'), info.get('phone'), info.get('email'))
            )

        conn.commit()

# 初始化数据库
init_db()
