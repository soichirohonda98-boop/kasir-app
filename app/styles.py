MAIN_STYLE = """
QMainWindow {
    background-color: #f5f5f5;
}

QWidget {
    background-color: #f5f5f5;
    color: #333333;
}

QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {
    border: 2px solid #d0a5e6;
    border-radius: 5px;
    padding: 5px;
    background-color: white;
    color: #333333;
}

QLineEdit:focus, QComboBox:focus {
    border: 2px solid #7b2cbf;
}

QPushButton {
    background-color: #7b2cbf;
    color: white;
    border: none;
    padding: 8px 15px;
    border-radius: 5px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #6a0dad;
}

QPushButton:pressed {
    background-color: #5a0a9d;
}

QTableWidget {
    background-color: white;
    gridline-color: #e0e0e0;
    border: 1px solid #d0a5e6;
}

QTableWidget::item {
    padding: 5px;
}

QTableWidget::item:selected {
    background-color: #d0a5e6;
}

QHeaderView::section {
    background-color: #7b2cbf;
    color: white;
    padding: 5px;
    border: none;
}

QTabBar::tab {
    background-color: #e8d5f2;
    color: #333333;
    padding: 8px 20px;
    border: 1px solid #d0a5e6;
}

QTabBar::tab:selected {
    background-color: #7b2cbf;
    color: white;
}

QLabel {
    color: #333333;
}

QMenuBar {
    background-color: #7b2cbf;
    color: white;
}

QMenuBar::item:selected {
    background-color: #6a0dad;
}

QMenu {
    background-color: white;
    color: #333333;
}

QMenu::item:selected {
    background-color: #d0a5e6;
}

QDialog {
    background-color: #f5f5f5;
}

QGroupBox {
    border: 2px solid #d0a5e6;
    border-radius: 5px;
    margin-top: 10px;
    padding-top: 10px;
    color: #7b2cbf;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 3px 0 3px;
}
"""
