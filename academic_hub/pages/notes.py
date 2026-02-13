from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QLineEdit, QTextEdit, QListWidget,
                             QListWidgetItem, QDialog, QFormLayout, QSplitter,
                             QMessageBox, QComboBox, QFrame)
from PyQt5.QtCore import Qt
from markdown import markdown
from ..database import (add_note, get_all_notes, update_note,
                        delete_note)
from ..utils.theme import theme_manager

class NoteDialog(QDialog):
    """笔记对话框"""

    def __init__(self, parent=None, note_data=None):
        super().__init__(parent)
        self.note_data = note_data
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("添加笔记" if not self.note_data else "编辑笔记")
        self.setMinimumWidth(400)

        layout = QFormLayout()

        self.title = QLineEdit()
        self.title.setPlaceholderText("笔记标题")
        layout.addRow("标题:", self.title)

        self.category = QComboBox()
        self.category.addItems(["通用", "课程笔记", "学习计划", "考研资料", "其他"])
        layout.addRow("分类:", self.category)

        self.tags = QLineEdit()
        self.tags.setPlaceholderText("标签，用逗号分隔")
        layout.addRow("标签:", self.tags)

        self.content = QTextEdit()
        self.content.setPlaceholderText("使用Markdown编写...")
        self.content.setMinimumHeight(200)
        layout.addRow("内容:", self.content)

        buttons = QPushButton("保存")
        buttons.clicked.connect(self.accept)
        cancel = QPushButton("取消")
        cancel.clicked.connect(self.reject)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(buttons)
        btn_layout.addWidget(cancel)
        layout.addRow(btn_layout)

        if self.note_data:
            self.title.setText(self.note_data['title'])
            self.category.setCurrentText(self.note_data['category'] or "通用")
            self.tags.setText(self.note_data['tags'] or "")
            self.content.setPlainText(self.note_data['content'] or "")

        self.setLayout(layout)
        self.apply_theme()

    def get_data(self):
        return {
            'title': self.title.text(),
            'content': self.content.toPlainText(),
            'category': self.category.currentText(),
            'tags': self.tags.text()
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

class NotesPage(QWidget):
    """Markdown笔记页面"""

    def __init__(self):
        super().__init__()
        self.current_note_id = None
        self.init_ui()
        self.load_notes()
        self.apply_theme()

        theme_manager.theme_changed.connect(self.on_theme_changed)

    def init_ui(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(16)

        # 左侧: 笔记列表
        left_panel = QFrame()
        left_layout = QVBoxLayout()

        # 标题栏
        header = QHBoxLayout()
        title = QLabel("Markdown笔记")
        title.setObjectName("pageTitle")
        header.addWidget(title)
        header.addStretch()

        add_btn = QPushButton("+ 新建")
        add_btn.clicked.connect(self.add_note)
        header.addWidget(add_btn)

        left_layout.addLayout(header)

        # 搜索框
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("搜索笔记...")
        self.search_box.textChanged.connect(self.on_search)
        left_layout.addWidget(self.search_box)

        # 笔记列表
        self.note_list = QListWidget()
        self.note_list.itemClicked.connect(self.on_note_selected)
        left_layout.addWidget(self.note_list)

        left_panel.setLayout(left_layout)
        main_layout.addWidget(left_panel, 1)

        # 右侧: 编辑器
        right_panel = QFrame()
        right_layout = QVBoxLayout()

        # 编辑器标题栏
        editor_header = QHBoxLayout()
        self.note_title = QLabel("选择或创建笔记")
        self.note_title.setObjectName("editorTitle")
        editor_header.addWidget(self.note_title)
        editor_header.addStretch()

        self.edit_btn = QPushButton("编辑")
        self.edit_btn.clicked.connect(self.edit_note)
        self.edit_btn.setEnabled(False)
        editor_header.addWidget(self.edit_btn)

        delete_btn = QPushButton("删除")
        delete_btn.clicked.connect(self.delete_note)
        editor_header.addWidget(delete_btn)

        right_layout.addLayout(editor_header)

        # 标签页切换
        tab_layout = QHBoxLayout()
        self.edit_tab_btn = QPushButton("编辑")
        self.preview_tab_btn = QPushButton("预览")
        self.edit_tab_btn.setCheckable(True)
        self.preview_tab_btn.setCheckable(True)
        self.edit_tab_btn.setChecked(True)
        self.edit_tab_btn.clicked.connect(lambda: self.switch_tab("edit"))
        self.preview_tab_btn.clicked.connect(lambda: self.switch_tab("preview"))
        tab_layout.addWidget(self.edit_tab_btn)
        tab_layout.addWidget(self.preview_tab_btn)
        tab_layout.addStretch()

        right_layout.addLayout(tab_layout)

        # 编辑区
        self.editor = QTextEdit()
        self.editor.setPlaceholderText("使用Markdown编写笔记内容...")
        self.editor.textChanged.connect(self.on_content_changed)
        right_layout.addWidget(self.editor, 1)

        # 预览区
        self.preview = QLabel()
        self.preview.setWordWrap(True)
        self.preview.setObjectName("previewContent")
        self.preview.hide()
        right_layout.addWidget(self.preview, 1)

        right_panel.setLayout(right_layout)
        main_layout.addWidget(right_panel, 2)

        self.setLayout(main_layout)

    def load_notes(self):
        self.note_list.clear()
        notes = get_all_notes()
        self.notes_data = {n['id']: n for n in notes}

        for note in notes:
            item = QListWidgetItem(f"{note['title']}")
            item.setData(Qt.UserRole, note['id'])
            self.note_list.addItem(item)

    def on_search(self, text):
        for i in range(self.note_list.count()):
            item = self.note_list.item(i)
            note_id = item.data(Qt.UserRole)
            note = self.notes_data.get(note_id)
            if note:
                if text.lower() in note['title'].lower():
                    item.setHidden(False)
                else:
                    item.setHidden(True)

    def on_note_selected(self, item):
        note_id = item.data(Qt.UserRole)
        self.current_note_id = note_id
        note = self.notes_data.get(note_id)

        if note:
            self.note_title.setText(note['title'])
            self.editor.setPlainText(note['content'] or "")
            self.update_preview()
            self.edit_btn.setEnabled(True)

    def on_content_changed(self):
        if self.preview.isVisible():
            self.update_preview()

    def switch_tab(self, tab):
        if tab == "edit":
            self.editor.show()
            self.preview.hide()
            self.edit_tab_btn.setChecked(True)
            self.preview_tab_btn.setChecked(False)
        else:
            self.editor.hide()
            self.preview.show()
            self.edit_tab_btn.setChecked(False)
            self.preview_tab_btn.setChecked(True)
            self.update_preview()

    def update_preview(self):
        content = self.editor.toPlainText()
        html = markdown(content, extensions=['tables', 'fenced_code'])
        colors = theme_manager.colors

        styled_html = f"""
        <html>
        <head>
        <style>
            body {{
                font-family: "Microsoft YaHei", sans-serif;
                color: {colors['text_primary']};
                padding: 10px;
                line-height: 1.6;
            }}
            h1, h2, h3 {{ color: {colors['primary']}; }}
            code {{
                background: {colors['hover']};
                padding: 2px 4px;
                border-radius: 3px;
                font-family: Consolas, monospace;
            }}
            pre {{
                background: {colors['hover']};
                padding: 10px;
                border-radius: 5px;
                overflow-x: auto;
            }}
            pre code {{
                background: none;
                padding: 0;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
            }}
            th, td {{
                border: 1px solid {colors['border']};
                padding: 8px;
                text-align: left;
            }}
            th {{
                background: {colors['hover']};
            }}
            blockquote {{
                border-left: 4px solid {colors['primary']};
                margin: 10px 0;
                padding-left: 10px;
                color: {colors['text_secondary']};
            }}
            a {{
                color: {colors['primary']};
            }}
        </style>
        </head>
        <body>{html}</body>
        </html>
        """
        self.preview.setText(styled_html)

    def add_note(self):
        dialog = NoteDialog(self)
        if dialog.exec_():
            data = dialog.get_data()
            note_id = add_note(**data)
            self.load_notes()
            # 选中新笔记
            for i in range(self.note_list.count()):
                item = self.note_list.item(i)
                if item.data(Qt.UserRole) == note_id:
                    self.note_list.setCurrentItem(item)
                    break

    def edit_note(self):
        if not self.current_note_id:
            return

        note = self.notes_data.get(self.current_note_id)
        dialog = NoteDialog(self, note)
        if dialog.exec_():
            data = dialog.get_data()
            update_note(self.current_note_id, **data)
            self.load_notes()

    def delete_note(self):
        if not self.current_note_id:
            QMessageBox.warning(self, "提示", "请选择要删除的笔记")
            return

        reply = QMessageBox.question(self, "确认删除",
                                      "确定要删除这篇笔记吗?",
                                      QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            delete_note(self.current_note_id)
            self.current_note_id = None
            self.note_title.setText("选择或创建笔记")
            self.editor.clear()
            self.edit_btn.setEnabled(False)
            self.load_notes()

    def apply_theme(self):
        colors = theme_manager.colors
        self.setStyleSheet(f"""
            #pageTitle {{
                font-size: 24px;
                font-weight: bold;
                color: {colors['text_primary']};
            }}
            #editorTitle {{
                font-size: 18px;
                font-weight: bold;
                color: {colors['text_primary']};
            }}
            #previewContent {{
                color: {colors['text_primary']};
            }}
            QFrame {{
                background: {colors['card']};
                border: 1px solid {colors['border']};
                border-radius: 8px;
            }}
            QLineEdit {{
                background: {colors['background']};
                color: {colors['text_primary']};
                border: 1px solid {colors['border']};
                padding: 8px;
                border-radius: 4px;
            }}
            QPushButton {{
                background: {colors['primary']};
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                opacity: 0.9;
            }}
            QListWidget {{
                background: {colors['background']};
                color: {colors['text_primary']};
                border: 1px solid {colors['border']};
            }}
            QListWidget::item:selected {{
                background: {colors['primary']};
                color: white;
            }}
            QTextEdit {{
                background: {colors['background']};
                color: {colors['text_primary']};
                border: 1px solid {colors['border']};
                font-family: Consolas, "Courier New", monospace;
            }}
        """)

    def on_theme_changed(self, theme_name):
        self.apply_theme()
        if self.preview.isVisible():
            self.update_preview()
