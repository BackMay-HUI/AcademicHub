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
        "width": 1880,
        "height": 1400
    },
    "gpa_method": "standard",  # standard: 标准算法, custom: 自定义绩点
    "custom_gpa": {
        "100-90": 4.0,
        "89-85": 3.7,
        "84-82": 3.3,
        "81-78": 3.0,
        "77-75": 2.7,
        "74-72": 2.3,
        "71-68": 2.0,
        "67-64": 1.3,
        "63-60": 1.0,
        "59-0": 0
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

def get_gpa_method():
    """获取绩点计算方式"""
    config = load_config()
    return config.get("gpa_method", "standard")

def get_custom_gpa():
    """获取自定义绩点映射"""
    config = load_config()
    return config.get("custom_gpa", {})

def set_gpa_method(method, custom_gpa=None):
    """设置绩点计算方式"""
    config = load_config()
    config["gpa_method"] = method
    if custom_gpa:
        config["custom_gpa"] = custom_gpa
    save_config(config)

# 颜色主题
COLORS = {
    "light": {
        "primary": "#1E88E5",
        "primary_light": "#42A5F5",
        "secondary": "#424242",
        "background": "#F5F7FA",
        "background_gradient": "qlineargradient(x1:0, y1:0, x2:1, y2:1, #F5F7FA 0%, #E8EEF5 100%)",
        "card": "#FFFFFF",
        "card_shadow": "0 4px 20px rgba(0,0,0,0.08)",
        "text_primary": "#212121",
        "text_secondary": "#757575",
        "border": "#E0E0E0",
        "success": "#4CAF50",
        "warning": "#FF9800",
        "error": "#F44336",
        "hover": "#E3F2FD",
        "chart_colors": ["#1E88E5", "#43A047", "#FB8C00", "#8E24AA", "#00ACC1"]
    },
    "dark": {
        "primary": "#64B5F6",
        "primary_light": "#90CAF9",
        "secondary": "#B0BEC5",
        "background": "#0D1117",
        "background_gradient": "qlineargradient(x1:0, y1:0, x2:1, y2:1, #0D1117 0%, #161B22 100%)",
        "card": "#1E1E1E",
        "card_shadow": "0 4px 20px rgba(0,0,0,0.3)",
        "text_primary": "#FFFFFF",
        "text_secondary": "#B0B0B0",
        "border": "#333333",
        "success": "#81C784",
        "warning": "#FFB74D",
        "error": "#E57373",
        "hover": "#2D2D2D",
        "chart_colors": ["#64B5F6", "#81C784", "#FFB74D", "#BA68C8", "#4DD0E1"]
    },
    "sakura": {
        "primary": "#FFB7C5",
        "primary_light": "#FFC0CB",
        "secondary": "#8B4557",
        "background": "#FFF0F5",
        "background_gradient": "qlineargradient(x1:0, y1:0, x2:1, y2:1, #FFF0F5 0%, #FFE4E1 100%)",
        "card": "#FFFFFF",
        "card_shadow": "0 4px 20px rgba(255,183,197,0.3)",
        "text_primary": "#5D3A3A",
        "text_secondary": "#8B6B6B",
        "border": "#FFD1DC",
        "success": "#98D8AA",
        "warning": "#FFD700",
        "error": "#FF6B6B",
        "hover": "#FFF5F8",
        "chart_colors": ["#FFB7C5", "#DDA0DD", "#FFB6C1", "#FF69B4", "#DB7093"]
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
