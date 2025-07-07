from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QHBoxLayout, QVBoxLayout, QPushButton,
    QStackedWidget, QLabel
)
from planning import PlanningPage
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplikacja Planowania")

        central_widget = QWidget()
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        nav_widget = QWidget()
        nav_layout = QHBoxLayout()
        nav_widget.setLayout(nav_layout)

        self.btn_planowanie = QPushButton("PLANOWANIE")
        self.btn_przestoje = QPushButton("PRZESTOJE")
        self.btn_konfiguracja = QPushButton("KONFIGURACJA")

        nav_layout.addWidget(self.btn_planowanie)
        nav_layout.addWidget(self.btn_przestoje)
        nav_layout.addWidget(self.btn_konfiguracja)
        nav_layout.addStretch()

        self.stack = QStackedWidget()

        page_planowanie = PlanningPage()

        page_przestoje = QWidget()
        page_przestoje_layout = QVBoxLayout()
        page_przestoje.setLayout(page_przestoje_layout)
        page_przestoje_layout.addWidget(QLabel("Tutaj zawartość okna Konfiguracja"))

        page_konfiguracja = QWidget()
        page_konfiguracja_layout = QVBoxLayout()
        page_konfiguracja.setLayout(page_konfiguracja_layout)
        page_konfiguracja_layout.addWidget(QLabel("Tutaj zawartość okna Konfiguracja"))

        self.stack.addWidget(page_planowanie)  # index 0
        self.stack.addWidget(page_przestoje)  # index 1
        self.stack.addWidget(page_konfiguracja)  # index 2

        self.btn_planowanie.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.btn_przestoje.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.btn_konfiguracja.clicked.connect(lambda: self.stack.setCurrentIndex(2))

        main_layout.addWidget(nav_widget)
        main_layout.addWidget(self.stack)

        self.stack.setCurrentIndex(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())