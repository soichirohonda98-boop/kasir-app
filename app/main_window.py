from PyQt5.QtWidgets import QMainWindow, QTabWidget, QMessageBox, QVBoxLayout, QWidget, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from app.styles import MAIN_STYLE
from app.tabs.transaksi_tab import TransaksiTab
from app.tabs.barang_tab import BarangTab
from app.tabs.pelanggan_tab import PelangganTab
from app.tabs.laporan_tab import LaporanTab

class MainWindow(QMainWindow):
    def __init__(self, user, db):
        super().__init__()
        self.user = user
        self.db = db
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle(f'Aplikasi Kasir - {self.user["nama"]}')
        self.setGeometry(100, 50, 1200, 700)
        self.setStyleSheet(MAIN_STYLE)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Top bar
        top_bar = QWidget()
        top_bar.setStyleSheet('background-color: #7b2cbf; color: white; padding: 10px;')
        top_layout = QHBoxLayout(top_bar)
        
        title = QLabel(f'Welcome, {self.user["nama"]}!')
        title.setFont(QFont('Arial', 14, QFont.Bold))
        title.setStyleSheet('color: white;')
        top_layout.addWidget(title)
        
        top_layout.addStretch()
        
        logout_btn = QPushButton('Logout')
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #7b2cbf;
                border: none;
                padding: 5px 15px;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        logout_btn.clicked.connect(self.logout)
        top_layout.addWidget(logout_btn)
        
        main_layout.addWidget(top_bar)
        
        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setFont(QFont('Arial', 10))
        
        self.transaksi_tab = TransaksiTab(self.db, self.user)
        self.barang_tab = BarangTab(self.db)
        self.pelanggan_tab = PelangganTab(self.db)
        self.laporan_tab = LaporanTab(self.db)
        
        self.tabs.addTab(self.transaksi_tab, '💳 Transaksi')
        self.tabs.addTab(self.barang_tab, '📦 Data Barang')
        self.tabs.addTab(self.pelanggan_tab, '👥 Pelanggan')
        self.tabs.addTab(self.laporan_tab, '📊 Laporan')
        
        main_layout.addWidget(self.tabs)
        
        self.show()
    
    def logout(self):
        reply = QMessageBox.question(self, 'Konfirmasi', 'Yakin ingin logout?',
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            from app.login_window import LoginWindow
            self.login_window = LoginWindow()
            self.login_window.show()
            self.close()
