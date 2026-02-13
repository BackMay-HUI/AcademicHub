from PyQt5.QtCore import QObject, pyqtSignal
from ..config import COLORS, load_config, save_config

class ThemeManager(QObject):
    """主题管理器"""
    theme_changed = pyqtSignal(str)  # 发送当前主题名称

    def __init__(self):
        super().__init__()
        self._current_theme = load_config().get("theme", "light")

    @property
    def current_theme(self):
        return self._current_theme

    @property
    def colors(self):
        return COLORS[self._current_theme]

    def set_theme(self, theme_name):
        """设置主题"""
        if theme_name in COLORS:
            self._current_theme = theme_name
            # 保存配置
            config = load_config()
            config["theme"] = theme_name
            save_config(config)
            self.theme_changed.emit(theme_name)

    def toggle_theme(self):
        """切换主题"""
        new_theme = "dark" if self._current_theme == "light" else "light"
        self.set_theme(new_theme)

# 全局主题管理器实例
theme_manager = ThemeManager()
