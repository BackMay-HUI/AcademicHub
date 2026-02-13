import os
import json
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "academic.db"
CONFIG_PATH = DATA_DIR / "config.json"

# 确保数据目录存在
DATA_DIR.mkdir(exist_ok=True)

# 默认配置
DEFAULT_CONFIG = {
    "theme": "light",
    "window": {
        "width": 1400,
        "height": 900
    }
}

def load_config():
    """加载配置"""
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return DEFAULT_CONFIG.copy()
    return DEFAULT_CONFIG.copy()

def save_config(config):
    """保存配置"""
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

# 颜色主题
COLORS = {
    "light": {
        "primary": "#1E88E5",
        "secondary": "#424242",
        "background": "#FAFAFA",
        "card": "#FFFFFF",
        "text_primary": "#212121",
        "text_secondary": "#757575",
        "border": "#E0E0E0",
        "success": "#4CAF50",
        "warning": "#FF9800",
        "error": "#F44336",
        "hover": "#E3F2FD"
    },
    "dark": {
        "primary": "#64B5F6",
        "secondary": "#B0BEC5",
        "background": "#121212",
        "card": "#1E1E1E",
        "text_primary": "#FFFFFF",
        "text_secondary": "#B0B0B0",
        "border": "#333333",
        "success": "#81C784",
        "warning": "#FFB74D",
        "error": "#E57373",
        "hover": "#2D2D2D"
    }
}

# 课程类型
COURSE_TYPES = ["必修", "选修", "限选"]

# 荣誉类型
HONOR_TYPES = ["奖学金", "竞赛获奖", "荣誉称号", "社会实践", "其他"]

# 荣誉级别
HONOR_LEVELS = ["校级", "省级", "国家级"]

# 学期列表 (大学阶段)
SEMESTERS = [
    "大一上", "大一下",
    "大二上", "大二下",
    "大三上", "大三下",
    "大四上", "大四下"
]
