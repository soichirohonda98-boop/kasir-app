from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QFont
import pandas as pd

class LaporanTab(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()
    
    def init_ui(self):
        main_layout = QVBoxLayout()
        
        # Header
        header = QLabel('LAPORAN TRANSAKSI')
        header.setFont(QFont('Arial', 14, QFont.Bold))
        header.setStyleSheet('color: #7b2cbf;')
        main_layout.addWidget(header)
        
        # Action buttons
        action_layout = QHBoxLayout()
        
        refresh_btn = QPushButton('Refresh')
        refresh_btn.clicked.connect(self.refresh_table)
        action_layout.addWidget(refresh_btn)
        
        export_excel_btn = QPushButton('Export Excel')
        export_excel_btn.clicked.connect(self.export_excel)
        action_layout.addWidget(export_excel_btn)
        
        action_layout.addStretch()
        main_layout.addLayout(action_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(
            ['No. Invoice', 'Tanggal', 'Pelanggan', 'Subtotal', 'Diskon', 'Total', 'Detail']
        )
        self.refresh_table()
        main_layout.addWidget(self.table)
        
        self.setLayout(main_layout)
    
    def refresh_table(self):
        transaksi_list = self.db.get_all_transaksi()
        self.table.setRowCount(len(transaksi_list))
        
        for idx, transaksi in enumerate(transaksi_list):
            self.table.setItem(idx, 0, QTableWidgetItem(transaksi[1]))
            self.table.setItem(idx, 1, QTableWidgetItem(str(transaksi[2])))
            self.table.setItem(idx, 2, QTableWidgetItem(str(transaksi[3])))
            self.table.setItem(idx, 3, QTableWidgetItem(f'Rp{transaksi[4]:,.0f}'))
            self.table.setItem(idx, 4, QTableWidgetItem(f'Rp{transaksi[5]:,.0f}'))
            self.table.setItem(idx, 5, QTableWidgetItem(f'Rp{transaksi[6]:,.0f}'))
            
            detail_btn = QPushButton('Lihat')
            detail_btn.clicked.connect(lambda checked, tid=transaksi[0]: self.show_detail(tid))
            self.table.setCellWidget(idx, 6, detail_btn)
    
    def show_detail(self, transaksi_id):
        pass
    
    def export_excel(self):
        transaksi_list = self.db.get_all_transaksi()
        
        data = []
        for t in transaksi_list:
            data.append({
                'No. Invoice': t[1],
                'Tanggal': t[2],
                'Pelanggan': t[3],
                'Subtotal': t[4],
                'Diskon': t[5],
                'Total': t[6]
            })
        
        df = pd.DataFrame(data)
        df.to_excel('Laporan_Transaksi.xlsx', index=False)
