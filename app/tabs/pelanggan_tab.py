from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox
)
from PyQt5.QtGui import QFont

class PelangganTab(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()
    
    def init_ui(self):
        main_layout = QVBoxLayout()
        
        # Header
        header = QLabel('DATA PELANGGAN')
        header.setFont(QFont('Arial', 14, QFont.Bold))
        header.setStyleSheet('color: #7b2cbf;')
        main_layout.addWidget(header)
        
        # Form inputs
        form_layout = QHBoxLayout()
        
        nama_label = QLabel('Nama:')
        self.nama_input = QLineEdit()
        form_layout.addWidget(nama_label)
        form_layout.addWidget(self.nama_input)
        
        alamat_label = QLabel('Alamat:')
        self.alamat_input = QLineEdit()
        form_layout.addWidget(alamat_label)
        form_layout.addWidget(self.alamat_input)
        
        telp_label = QLabel('No. Telp:')
        self.telp_input = QLineEdit()
        form_layout.addWidget(telp_label)
        form_layout.addWidget(self.telp_input)
        
        tipe_label = QLabel('Tipe:')
        self.tipe_combo = QComboBox()
        self.tipe_combo.addItems(['R', 'WS', 'SO'])
        form_layout.addWidget(tipe_label)
        form_layout.addWidget(self.tipe_combo)
        
        add_btn = QPushButton('Tambah')
        add_btn.clicked.connect(self.add_pelanggan)
        form_layout.addWidget(add_btn)
        
        main_layout.addLayout(form_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ['ID', 'Nama', 'Alamat', 'No. Telp', 'Tipe', 'Aksi']
        )
        self.refresh_table()
        main_layout.addWidget(self.table)
        
        self.setLayout(main_layout)
    
    def add_pelanggan(self):
        nama = self.nama_input.text().strip()
        alamat = self.alamat_input.text().strip()
        telp = self.telp_input.text().strip()
        tipe = self.tipe_combo.currentText()
        
        if not nama:
            QMessageBox.warning(self, 'Peringatan', 'Nama harus diisi!')
            return
        
        pelanggan_id = self.db.add_pelanggan(nama, alamat, telp, tipe)
        if pelanggan_id:
            QMessageBox.information(self, 'Sukses', 'Pelanggan berhasil ditambahkan!')
            self.clear_form()
            self.refresh_table()
        else:
            QMessageBox.critical(self, 'Error', 'Gagal menambahkan pelanggan!')
    
    def refresh_table(self):
        pelanggan_list = self.db.get_all_pelanggan()
        self.table.setRowCount(len(pelanggan_list))
        
        for idx, pelanggan in enumerate(pelanggan_list):
            self.table.setItem(idx, 0, QTableWidgetItem(str(pelanggan[0])))
            self.table.setItem(idx, 1, QTableWidgetItem(pelanggan[1]))
            self.table.setItem(idx, 2, QTableWidgetItem(pelanggan[2] or ''))
            self.table.setItem(idx, 3, QTableWidgetItem(pelanggan[3] or ''))
            self.table.setItem(idx, 4, QTableWidgetItem(pelanggan[4]))
            
            delete_btn = QPushButton('Hapus')
            delete_btn.clicked.connect(lambda checked, pid=pelanggan[0]: self.delete_pelanggan(pid))
            self.table.setCellWidget(idx, 5, delete_btn)
    
    def delete_pelanggan(self, pelanggan_id):
        reply = QMessageBox.question(self, 'Konfirmasi', 'Yakin ingin menghapus pelanggan ini?',
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.db.delete_pelanggan(pelanggan_id)
            self.refresh_table()
    
    def clear_form(self):
        self.nama_input.clear()
        self.alamat_input.clear()
        self.telp_input.clear()
        self.tipe_combo.setCurrentIndex(0)
