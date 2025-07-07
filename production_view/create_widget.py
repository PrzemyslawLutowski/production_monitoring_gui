from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt


def create_plan_value_widget(content, baseFontSize=20, color="gray"):
    label = QLabel(content)
    label.setStyleSheet(
        f"background-color: {color}; font-weight: bold; padding: 5px;"
    )
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setProperty("baseFontSize", baseFontSize)
    return label


def create_time_widget(content, baseFontSize=20, color="rgba(0, 0, 0, 0)"):
    label = QLabel(content)
    label.setStyleSheet(
        f"background-color: {color}; font-weight: bold; padding: 5px; border-radius: 5px;"
    )
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setProperty("baseFontSize", baseFontSize)
    return label


def create_status_widget(content, baseFontSize=20, color="gray"):
    label = QLabel(content)
    label.setStyleSheet(
        f"background-color: {color}; font-weight: bold; padding: 5px; border-radius: 5px;"
    )
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setProperty("baseFontSize", baseFontSize)
    return label


def create_balance_value_widget(content, baseFontSize=20, color="black"):
    label = QLabel(content)
    label.setStyleSheet(
        f"background-color: white; color: {color}; font-weight: bold; padding: 5px;"
    )
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setProperty("baseFontSize", baseFontSize)
    return label


def create_section_widget(content, baseFontSize=20, color="gray"):
    label = QLabel(content)
    # label.
    label.setStyleSheet(
        f"background-color: {color}; font-weight: bold; padding: 5px; border-radius: 5px;"
    )
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setProperty("baseFontSize", baseFontSize)
    return label


def create_label_widget(content, baseFontSize=20):
    label = QLabel(content)
    label.setStyleSheet(
        "background-color: brown; color: white; font-weight: bold; padding: 5px; border-radius: 5px;"
    )
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setProperty("baseFontSize", baseFontSize)
    return label
