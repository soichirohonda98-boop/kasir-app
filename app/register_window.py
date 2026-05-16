from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from app.styles import MAIN_STYLE

class RegisterWindow(QWidget):
    def __init__(self, db, parent):
        super().__init__()
        self.db = db
        self.parent = parent
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Daftar Akun - Kasir App')
        self.setGeometry(100, 100, 400, 500)
        self.setStyleSheet(MAIN_STYLE)
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title = QLabel('DAFTAR AKUN')
        title.setFont(QFont('Arial', 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet('color: #7b2cbf;')
        main_layout.addWidget(title)
        
        main_layout.addSpacing(10)
        
        # NIK
        nik_label = QLabel('NIK:')
        nik_label.setFont(QFont('Arial', 10, QFont.Bold))
        main_layout.addWidget(nik_label)
        self.nik_input = QLineEdit()
        self.nik_input.setPlaceholderText('Masukkan NIK')
        self.nik_input.setMinimumHeight(35)
        main_layout.addWidget(self.nik_input)
        
        # Nama
        nama_label = QLabel('Nama:')
        nama_label.setFont(QFont('Arial', 10, QFont.Bold))
        main_layout.addWidget(nama_label)
        self.nama_input = QLineEdit()
        self.nama_input.setPlaceholderText('Masukkan Nama')
        self.nama_input.setMinimumHeight(35)
        main_layout.addWidget(self.nama_input)
        
        # Password
        password_label = QLabel('Password:')
        password_label.setFont(QFont('Arial', 10, QFont.Bold))
        main_layout.addWidget(password_label)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Masukkan Password')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(35)
        main_layout.addWidget(self.password_input)
        
        # Confirm Password
        confirm_label = QLabel('Konfirmasi Password:')
        confirm_label.setFont(QFont('Arial', 10, QFont.Bold))
        main_layout.addWidget(confirm_label)
        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText('Konfirmasi Password')
        self.confirm_input.setEchoMode(QLineEdit.Password)
        self.confirm_input.setMinimumHeight(35)
        main_layout.addWidget(self.confirm_input)
        
        main_layout.addSpacing(10)
        
        # Button Layout
        button_layout = QHBoxLayout()
        
        register_btn = QPushButton('Daftar')
        register_btn.setMinimumHeight(40)
        register_btn.clicked.connect(self.register)
        button_layout.addWidget(register_btn)
        
        back_btn = QPushButton('Kembali')
        back_btn.setMinimumHeight(40)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #d0a5e6;
                color: #333333;
                border: none;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
            }
        """)
        back_btn.clicked.connect(self.back_to_login)
        button_layout.addWidget(back_btn)
        
        main_layout.addLayout(button_layout)
        main_layout.addStretch()
        
        self.setLayout(main_layout)
    
    def register(self):
        nik = self.nik_input.text().strip()
        nama = self.nama_input.text().strip()
        password = self.password_input.text().strip()
        confirm = self.confirm_input.text().strip()
        
        if not nik or not nama or not password or not confirm:
            QMessageBox.warning(self, 'Peringatan', 'Semua field harus diisi!')
            return
        
        if password != confirm:
            QMessageBox.warning(self, 'Peringatan', 'Password tidak cocok!')
            return
        
        if len(password) < 6:
            QMessageBox.warning(self, 'Peringatan', 'Password minimal 6 karakter!')
            return
        
        if self.db.add_user(nik, password, nama):
            QMessageBox.information(self, 'Sukses', 'Akun berhasil dibuat! Silakan login.')
            self.back_to_login()
        else:
            QMessageBox.critical(self, 'Error', 'NIK sudah terdaftar!')
    
    def back_to_login(self):
        self.parent.show()
        self.close()
