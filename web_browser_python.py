import sys
import re
from PyQt5.QtWidgets import QApplication, QSizePolicy, QWidget, QVBoxLayout, QHBoxLayout, QMainWindow, QLineEdit, \
    QPushButton, QTabWidget, QToolButton, QTabBar
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QFont

class WebEngineWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.browser = QWebEngineView(self)
        layout.addWidget(self.browser)
        self.browser.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

class WebBrowserApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Web Browser")
        self.setGeometry(100, 100, 800, 600)
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.tabBarClicked.connect(self.clear_search_bar)
        self.setCentralWidget(self.tab_widget)
        self.create_widgets()

    def create_widgets(self):
        self.url_entry = QLineEdit(self)
        self.url_entry.returnPressed.connect(lambda: self.load_url(self.url_entry, self.tab_widget.currentWidget()))
        self.url_entry.setPlaceholderText("Enter URL here")
        self.url_entry.setMaximumHeight(30)
        self.url_entry.setStyleSheet(
            "padding: 5px; background-color: #fff; border: 1px solid #ccc; font-size: 14px;"
        )
        go_button = QPushButton("Go")
        go_button.clicked.connect(lambda: self.load_url(self.url_entry, self.tab_widget.currentWidget()))
        go_button.setStyleSheet(
            "background-color: #0078D4; color: #fff; padding: 8px 16px; font-size: 14px;"
        )
        new_tab_button = QPushButton("New Tab")
        new_tab_button.clicked.connect(self.create_new_tab)
        new_tab_button.setStyleSheet(
            "background-color: #0078D4; color: #fff; padding: 8px 16px; font-size: 14px;"
        )
        new_window_button = QPushButton("New Window")
        new_window_button.clicked.connect(self.open_new_window)
        new_window_button.setStyleSheet(
            "background-color: #0078D4; color: #fff; padding: 8px 16px; font-size: 14px;"
        )
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.url_entry)
        top_layout.addWidget(go_button)
        top_layout.addWidget(new_tab_button)
        top_layout.addWidget(new_window_button)
        top_widget = QWidget()
        top_widget.setLayout(top_layout)
        self.setMenuWidget(top_widget)
        self.create_new_tab()

    def create_new_tab(self):
        web_engine_widget = WebEngineWidget()
        new_tab_index = self.tab_widget.addTab(web_engine_widget, "New Tab")
        close_button = QToolButton(self)
        close_button.setText("x")
        close_button.setStyleSheet(
            "QToolButton { font-family: 'Material Icons'; font-size: 18px; background-color: #444; border: none; color: #fff; }"
            "QToolButton::menu-indicator { image: none; }"
            "QToolButton:hover { background-color: #666; }"
        )
        close_button.clicked.connect(lambda: self.close_tab(new_tab_index))
        self.tab_widget.tabBar().setTabButton(new_tab_index, QTabBar.RightSide, close_button)

    def load_url(self, url_entry, web_engine_widget):
        input_url = url_entry.text().strip()
        if not input_url:
            return
        url_regex = re.compile(
            r"^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)+([\/?].*)?$"
        )
        if url_regex.match(input_url):
            if not input_url.startswith("http://") and not input_url.startswith("https://"):
                input_url = "http://" + input_url
            web_engine_widget.browser.setUrl(QUrl(input_url))
        else:
            search_query = "https://www.google.com/search?q=" + "+".join(input_url.split())
            web_engine_widget.browser.setUrl(QUrl(search_query))

    def close_tab(self, index):
        if self.tab_widget.count() > 1:
            self.tab_widget.removeTab(index)

    def open_new_window(self):
        new_window = WebBrowserApp()
        new_window.show()

    def clear_search_bar(self, index):
        self.url_entry.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Arial", 12)
    app.setFont(font)
    browser_app = WebBrowserApp()
    browser_app.show()
    sys.exit(app.exec_())
