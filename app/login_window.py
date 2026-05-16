from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from app.database import Database
from app.main_window import MainWindow
from app.styles import MAIN_STYLE

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Login Aplikasi Kasir')
        self.setGeometry(100, 100, 400, 500)
        self.setStyleSheet(MAIN_STYLE)
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title = QLabel('KASIR APP')
        title.setFont(QFont('Arial', 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet('color: #7b2cbf;')
        main_layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel('Sistem Kasir Modern')
        subtitle.setFont(QFont('Arial', 12))
        subtitle.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(subtitle)
        
        main_layout.addSpacing(20)
        
        # NIK Label & Input
        nik_label = QLabel('NIK (Nomor Induk Karyawan):')
        nik_label.setFont(QFont('Arial', 10, QFont.Bold))
        main_layout.addWidget(nik_label)
        
        self.nik_input = QLineEdit()
        self.nik_input.setPlaceholderText('Masukkan NIK Anda')
        self.nik_input.setMinimumHeight(40)
        main_layout.addWidget(self.nik_input)
        
        # Password Label & Input
        password_label = QLabel('Password:')
        password_label.setFont(QFont('Arial', 10, QFont.Bold))
        main_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Masukkan Password')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(40)
        main_layout.addWidget(self.password_input)
        
        main_layout.addSpacing(10)
        
        # Button Layout
        button_layout = QHBoxLayout()
        
        # Login Button
        login_btn = QPushButton('Login')
        login_btn.setMinimumHeight(45)
        login_btn.setFont(QFont('Arial', 11, QFont.Bold))
        login_btn.clicked.connect(self.login)
        button_layout.addWidget(login_btn)
        
        # Register Button
        register_btn = QPushButton('Daftar')
        register_btn.setMinimumHeight(45)
        register_btn.setFont(QFont('Arial', 11, QFont.Bold))
        register_btn.setStyleSheet("""
            QPushButton {
                background-color: #d0a5e6;
                color: #333333;
                border: none;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c08fd9;
            }
        """)
        register_btn.clicked.connect(self.show_register)
        button_layout.addWidget(register_btn)
        
        main_layout.addLayout(button_layout)
        main_layout.addStretch()
        
        self.setLayout(main_layout)
    
    def login(self):
        nik = self.nik_input.text().strip()
        password = self.password_input.text().strip()
        
        if not nik or not password:
            QMessageBox.warning(self, 'Peringatan', 'NIK dan Password harus diisi!')
            return
        
        user = self.db.verify_user(nik, password)
        if user:
            self.open_main_window(user)
        else:
            QMessageBox.critical(self, 'Error', 'NIK atau Password salah!')
    
    def show_register(self):
        from app.register_window import RegisterWindow
        self.register_window = RegisterWindow(self.db, self)
        self.register_window.show()
        self.hide()
    
    def open_main_window(self, user):
        self.main_window = MainWindow(user, self.db)
        self.main_window.show()
        self.close()
