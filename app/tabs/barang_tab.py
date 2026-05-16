from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QDoubleSpinBox, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox, QDialog, QFormLayout
)
from PyQt5.QtGui import QFont

class BarangTab(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()
    
    def init_ui(self):
        main_layout = QVBoxLayout()
        
        # Header
        header = QLabel('DATA BARANG')
        header.setFont(QFont('Arial', 14, QFont.Bold))
        header.setStyleSheet('color: #7b2cbf;')
        main_layout.addWidget(header)
        
        # Form inputs
        form_layout = QHBoxLayout()
        
        kode_label = QLabel('Kode:')
        self.kode_input = QLineEdit()
        form_layout.addWidget(kode_label)
        form_layout.addWidget(self.kode_input)
        
        nama_label = QLabel('Nama:')
        self.nama_input = QLineEdit()
        form_layout.addWidget(nama_label)
        form_layout.addWidget(self.nama_input)
        
        harga_r_label = QLabel('Harga R:')
        self.harga_r_input = QDoubleSpinBox()
        self.harga_r_input.setMaximum(999999)
        form_layout.addWidget(harga_r_label)
        form_layout.addWidget(self.harga_r_input)
        
        harga_ws_label = QLabel('Harga WS:')
        self.harga_ws_input = QDoubleSpinBox()
        self.harga_ws_input.setMaximum(999999)
        form_layout.addWidget(harga_ws_label)
        form_layout.addWidget(self.harga_ws_input)
        
        harga_so_label = QLabel('Harga SO:')
        self.harga_so_input = QDoubleSpinBox()
        self.harga_so_input.setMaximum(999999)
        form_layout.addWidget(harga_so_label)
        form_layout.addWidget(self.harga_so_input)
        
        add_btn = QPushButton('Tambah')
        add_btn.clicked.connect(self.add_barang)
        form_layout.addWidget(add_btn)
        
        main_layout.addLayout(form_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(
            ['ID', 'Kode', 'Nama', 'Stok', 'Harga R', 'Harga WS', 'Harga SO', 'Aksi']
        )
        self.refresh_table()
        main_layout.addWidget(self.table)
        
        self.setLayout(main_layout)
    
    def add_barang(self):
        kode = self.kode_input.text().strip()
        nama = self.nama_input.text().strip()
        harga_r = self.harga_r_input.value()
        harga_ws = self.harga_ws_input.value()
        harga_so = self.harga_so_input.value()
        
        if not kode or not nama:
            QMessageBox.warning(self, 'Peringatan', 'Kode dan Nama harus diisi!')
            return
        
        if self.db.add_barang(kode, nama, harga_r, harga_ws, harga_so):
            QMessageBox.information(self, 'Sukses', 'Barang berhasil ditambahkan!')
            self.clear_form()
            self.refresh_table()
        else:
            QMessageBox.critical(self, 'Error', 'Kode barang sudah ada!')
    
    def refresh_table(self):
        barang_list = self.db.get_all_barang()
        self.table.setRowCount(len(barang_list))
        
        for idx, barang in enumerate(barang_list):
            self.table.setItem(idx, 0, QTableWidgetItem(str(barang[0])))
            self.table.setItem(idx, 1, QTableWidgetItem(barang[1]))
            self.table.setItem(idx, 2, QTableWidgetItem(barang[2]))
            self.table.setItem(idx, 3, QTableWidgetItem(str(barang[3])))
            self.table.setItem(idx, 4, QTableWidgetItem(f'Rp{barang[4]:,.0f}'))
            self.table.setItem(idx, 5, QTableWidgetItem(f'Rp{barang[5]:,.0f}'))
            self.table.setItem(idx, 6, QTableWidgetItem(f'Rp{barang[6]:,.0f}'))
            
            action_layout = QHBoxLayout()
            edit_btn = QPushButton('Edit')
            edit_btn.clicked.connect(lambda checked, bid=barang[0]: self.edit_barang(bid))
            delete_btn = QPushButton('Hapus')
            delete_btn.clicked.connect(lambda checked, bid=barang[0]: self.delete_barang(bid))
            
            action_widget = QWidget()
            action_widget.setLayout(action_layout)
            action_layout.addWidget(edit_btn)
            action_layout.addWidget(delete_btn)
            
            self.table.setCellWidget(idx, 7, action_widget)
    
    def edit_barang(self, barang_id):
        QMessageBox.information(self, 'Info', 'Feature edit akan segera datang!')
    
    def delete_barang(self, barang_id):
        reply = QMessageBox.question(self, 'Konfirmasi', 'Yakin ingin menghapus barang ini?',
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.db.delete_barang(barang_id)
            self.refresh_table()
    
    def clear_form(self):
        self.kode_input.clear()
        self.nama_input.clear()
        self.harga_r_input.setValue(0)
        self.harga_ws_input.setValue(0)
        self.harga_so_input.setValue(0)
