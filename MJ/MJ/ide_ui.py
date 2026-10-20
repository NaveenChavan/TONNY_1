from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QSplitter, QFrame, QLabel, QPushButton, QTextEdit, 
                             QTreeWidget, QTreeWidgetItem, QTabBar, QMenuBar, QMenu)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon, QColor

QSS = """
/* Main Application Dark Theme QSS */
QMainWindow {
    background-color: #181818;
    color: #cccccc;
    font-family: 'Segoe UI', Arial, sans-serif;
}

QSplitter::handle {
    background-color: #2b2b2b;
}

/* Activity Bar */
QFrame#activityBar {
    background-color: #181818;
    border-right: 1px solid #2b2b2b;
}

/* Assistant Chat Panel */
QFrame#assistantPanel {
    background-color: #1e1e1e;
    border-left: 1px solid #2b2b2b;
}

/* Input Container Frame */
QFrame#inputContainer {
    background-color: #252526;
    border: 1px solid #3c3c3c;
    border-radius: 12px;
}

QTextEdit#chatInput {
    background-color: transparent;
    border: none;
    color: #ffffff;
    font-size: 13px;
}

/* Model Selector Button */
QPushButton#modelSelector {
    background-color: #2d2d2d;
    border: 1px solid #383838;
    border-radius: 6px;
    padding: 3px 8px;
    color: #d0d0d0;
    font-size: 11px;
}

QPushButton#modelSelector:hover {
    background-color: #37373d;
}

/* Send Button */
QPushButton#sendButton {
    background-color: #3a3a3a;
    border: none;
    border-radius: 14px;
    color: #ffffff;
}

QPushButton#sendButton:hover {
    background-color: #007acc;
}

/* Audio Player Container */
QFrame#audioPlayerBox {
    background-color: #252526;
    border: 1px solid #383838;
    border-radius: 8px;
}
"""

class IDEWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TONY - Antigravity IDE - tony.py")
        self.resize(1200, 800)
        self.setStyleSheet(QSS)
        
        # Central widget and layout
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 1. Activity Bar (Left)
        activity_bar = QFrame()
        activity_bar.setObjectName("activityBar")
        activity_bar.setFixedWidth(48)
        
        # 2. Central Splitter
        main_splitter = QSplitter(Qt.Horizontal)
        
        # 2a. Editor / Terminal Area
        editor_splitter = QSplitter(Qt.Vertical)
        
        # Editor Tab \u0026 View
        editor_container = QWidget()
        editor_layout = QVBoxLayout(editor_container)
        editor_layout.setContentsMargins(0, 0, 0, 0)
        editor_layout.setSpacing(0)
        
        tab_bar = QTabBar()
        tab_bar.addTab("tony.py")
        tab_bar.addTab("runtime_agent.py")
        tab_bar.setStyleSheet("QTabBar::tab { background: #252526; color: #969696; padding: 8px 15px; border: none; } QTabBar::tab:selected { background: #1e1e1e; color: white; border-top: 2px solid #007acc; }")
        
        editor_text = QTextEdit()
        editor_text.setStyleSheet("background-color: #1e1e1e; color: #dcdcdc; font-family: Consolas; font-size: 13px; border: none;")
        editor_text.setPlainText("def main():\n    print('Hello World')")
        
        editor_layout.addWidget(tab_bar)
        editor_layout.addWidget(editor_text)
        
        # Terminal Area
        terminal_container = QWidget()
        term_layout = QVBoxLayout(terminal_container)
        term_layout.setContentsMargins(0, 0, 0, 0)
        term_layout.setSpacing(0)
        
        term_tabs = QTabBar()
        term_tabs.addTab("Problems")
        term_tabs.addTab("Output")
        term_tabs.addTab("Terminal")
        term_tabs.setCurrentIndex(2)
        term_tabs.setStyleSheet("QTabBar::tab { background: #181818; color: #858585; padding: 5px 15px; border: none; } QTabBar::tab:selected { color: white; border-bottom: 2px solid #007acc; }")
        
        term_text = QTextEdit()
        term_text.setStyleSheet("background-color: #181818; color: #cccccc; font-family: Consolas; font-size: 12px; border: none; border-top: 1px solid #2b2b2b;")
        term_text.setPlainText("PS C:\\Users\\LENOVO\\Desktop\\TONY1\\MJ\\MJ> python main.py")
        
        term_layout.addWidget(term_tabs)
        term_layout.addWidget(term_text)
        
        editor_splitter.addWidget(editor_container)
        editor_splitter.addWidget(terminal_container)
        editor_splitter.setSizes([500, 200])
        
        # 3. Assistant Chat Panel (Right)
        assistant_panel = QFrame()
        assistant_panel.setObjectName("assistantPanel")
        assistant_panel.setMinimumWidth(350)
        ast_layout = QVBoxLayout(assistant_panel)
        ast_layout.setContentsMargins(10, 10, 10, 10)
        
        # Header
        header = QLabel("General Inquiry Assistance")
        header.setStyleSheet("font-weight: bold; color: #e0e0e0; font-size: 13px;")
        ast_layout.addWidget(header)
        
        # Chat History
        chat_history = QTextEdit()
        chat_history.setReadOnly(True)
        chat_history.setStyleSheet("background-color: transparent; border: none; color: #dcdcdc; font-size: 13px;")
        chat_history.setHtml("<p><b>Assistant:</b> How can I help you today?</p>")
        ast_layout.addWidget(chat_history)
        
        # Input Area
        input_container = QFrame()
        input_container.setObjectName("inputContainer")
        input_layout = QVBoxLayout(input_container)
        
        chat_input = QTextEdit()
        chat_input.setObjectName("chatInput")
        chat_input.setPlaceholderText("Ask anything, @ to mention, / for actions")
        chat_input.setFixedHeight(60)
        
        bottom_bar = QHBoxLayout()
        model_btn = QPushButton("Gemini 3.1 Pro High")
        model_btn.setObjectName("modelSelector")
        send_btn = QPushButton("→")
        send_btn.setObjectName("sendButton")
        send_btn.setFixedSize(28, 28)
        
        bottom_bar.addWidget(model_btn)
        bottom_bar.addStretch()
        bottom_bar.addWidget(send_btn)
        
        input_layout.addWidget(chat_input)
        input_layout.addLayout(bottom_bar)
        
        ast_layout.addWidget(input_container)
        
        main_splitter.addWidget(editor_splitter)
        main_splitter.addWidget(assistant_panel)
        main_splitter.setSizes([800, 350])
        
        main_layout.addWidget(activity_bar)
        main_layout.addWidget(main_splitter)
