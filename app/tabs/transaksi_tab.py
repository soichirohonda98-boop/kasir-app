from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QDialog, QFormLayout, QTextEdit
)
from PyQt5.QtCore import Qt, QDate, QDateTime
from PyQt5.QtGui import QFont
from datetime import datetime
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

class TransaksiTab(QWidget):
    def __init__(self, db, user):
        super().__init__()
        self.db = db
        self.user = user
        self.current_transaksi_id = None
        self.current_items = []
        self.init_ui()
    
    def init_ui(self):
        main_layout = QVBoxLayout()
        
        # Header
        header = QLabel('TRANSAKSI PENJUALAN')
        header.setFont(QFont('Arial', 14, QFont.Bold))
        header.setStyleSheet('color: #7b2cbf;')
        main_layout.addWidget(header)
        
        # Tanggal
        tgl_layout = QHBoxLayout()
        tgl_label = QLabel('Tanggal:')
        tgl_label.setFont(QFont('Arial', 10, QFont.Bold))
        self.tgl_input = QLineEdit()
        self.tgl_input.setText(datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
        self.tgl_input.setReadOnly(True)
        tgl_layout.addWidget(tgl_label)
        tgl_layout.addWidget(self.tgl_input)
        tgl_layout.addStretch()
        main_layout.addLayout(tgl_layout)
        
        # Form inputs
        form_layout = QHBoxLayout()
        
        # No Invoice
        inv_label = QLabel('No. Invoice:')
        self.inv_input = QLineEdit()
        self.inv_input.setText(self.db.generate_no_inv())
        self.inv_input.setReadOnly(True)
        form_layout.addWidget(inv_label)
        form_layout.addWidget(self.inv_input)
        
        # Pelanggan
        pelanggan_label = QLabel('Pelanggan:')
        self.pelanggan_combo = QComboBox()
        self.load_pelanggan_combo()
        form_layout.addWidget(pelanggan_label)
        form_layout.addWidget(self.pelanggan_combo)
        
        form_layout.addStretch()
        main_layout.addLayout(form_layout)
        
        # Items form
        items_layout = QHBoxLayout()
        
        barang_label = QLabel('Barang:')
        self.barang_combo = QComboBox()
        self.load_barang_combo()
        self.barang_combo.currentIndexChanged.connect(self.on_barang_changed)
        items_layout.addWidget(barang_label)
        items_layout.addWidget(self.barang_combo)
        
        # Strata harga
        strata_label = QLabel('Strata:')
        self.strata_combo = QComboBox()
        self.strata_combo.addItems(['R', 'WS', 'SO'])
        self.strata_combo.currentIndexChanged.connect(self.on_barang_changed)
        items_layout.addWidget(strata_label)
        items_layout.addWidget(self.strata_combo)
        
        # Harga
        harga_label = QLabel('Harga:')
        self.harga_input = QLineEdit()
        self.harga_input.setReadOnly(True)
        items_layout.addWidget(harga_label)
        items_layout.addWidget(self.harga_input)
        
        # Qty
        qty_label = QLabel('Qty:')
        self.qty_input = QSpinBox()
        self.qty_input.setMinimum(1)
        self.qty_input.setValue(1)
        items_layout.addWidget(qty_label)
        items_layout.addWidget(self.qty_input)
        
        # Diskon item
        diskon_label = QLabel('Diskon:')
        self.diskon_item_input = QDoubleSpinBox()
        self.diskon_item_input.setMinimum(0)
        self.diskon_item_input.setMaximum(999999)
        items_layout.addWidget(diskon_label)
        items_layout.addWidget(self.diskon_item_input)
        
        # Add button
        add_btn = QPushButton('Tambah')
        add_btn.setMaximumWidth(100)
        add_btn.clicked.connect(self.add_item)
        items_layout.addWidget(add_btn)
        
        items_layout.addStretch()
        main_layout.addLayout(items_layout)
        
        # Items table
        self.items_table = QTableWidget()
        self.items_table.setColumnCount(7)
        self.items_table.setHorizontalHeaderLabels(
            ['No', 'Barang', 'Qty', 'Harga Satuan', 'Diskon Item', 'Subtotal', 'Aksi']
        )
        self.items_table.setColumnWidth(0, 40)
        self.items_table.setColumnWidth(1, 150)
        self.items_table.setColumnWidth(2, 60)
        self.items_table.setColumnWidth(3, 100)
        self.items_table.setColumnWidth(4, 100)
        self.items_table.setColumnWidth(5, 100)
        self.items_table.setColumnWidth(6, 80)
        main_layout.addWidget(self.items_table)
        
        # Summary
        summary_layout = QHBoxLayout()
        summary_layout.addStretch()
        
        # Subtotal
        subtotal_label = QLabel('Subtotal:')
        subtotal_label.setFont(QFont('Arial', 10, QFont.Bold))
        self.subtotal_input = QLineEdit()
        self.subtotal_input.setText('Rp0')
        self.subtotal_input.setReadOnly(True)
        self.subtotal_input.setMaximumWidth(150)
        summary_layout.addWidget(subtotal_label)
        summary_layout.addWidget(self.subtotal_input)
        
        # Diskon total
        diskon_label = QLabel('Diskon Total:')
        diskon_label.setFont(QFont('Arial', 10, QFont.Bold))
        self.diskon_total_input = QDoubleSpinBox()
        self.diskon_total_input.setMaximumWidth(150)
        self.diskon_total_input.valueChanged.connect(self.update_total)
        summary_layout.addWidget(diskon_label)
        summary_layout.addWidget(self.diskon_total_input)
        
        # Diskon percentage
        diskon_pct_label = QLabel('Diskon %:')
        diskon_pct_label.setFont(QFont('Arial', 10, QFont.Bold))
        self.diskon_pct_input = QDoubleSpinBox()
        self.diskon_pct_input.setMaximumWidth(150)
        self.diskon_pct_input.setSuffix('%')
        self.diskon_pct_input.valueChanged.connect(self.update_diskon_percentage)
        summary_layout.addWidget(diskon_pct_label)
        summary_layout.addWidget(self.diskon_pct_input)
        
        # Total
        total_label = QLabel('Total:')
        total_label.setFont(QFont('Arial', 12, QFont.Bold))
        total_label.setStyleSheet('color: #7b2cbf;')
        self.total_input = QLineEdit()
        self.total_input.setText('Rp0')
        self.total_input.setReadOnly(True)
        self.total_input.setMaximumWidth(150)
        self.total_input.setFont(QFont('Arial', 12, QFont.Bold))
        self.total_input.setStyleSheet('background-color: #d0a5e6; color: #333333;')
        summary_layout.addWidget(total_label)
        summary_layout.addWidget(self.total_input)
        
        main_layout.addLayout(summary_layout)
        
        # Catatan
        catatan_label = QLabel('Catatan:')
        catatan_label.setFont(QFont('Arial', 10, QFont.Bold))
        self.catatan_input = QTextEdit()
        self.catatan_input.setMaximumHeight(80)
        main_layout.addWidget(catatan_label)
        main_layout.addWidget(self.catatan_input)
        
        # Action buttons
        action_layout = QHBoxLayout()
        
        clear_btn = QPushButton('Clear')
        clear_btn.clicked.connect(self.clear_form)
        action_layout.addWidget(clear_btn)
        
        action_layout.addStretch()
        
        save_btn = QPushButton('Simpan Transaksi')
        save_btn.setMinimumWidth(150)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        save_btn.clicked.connect(self.save_transaksi)
        action_layout.addWidget(save_btn)
        
        print_btn = QPushButton('🖨️ Cetak')
        print_btn.setMinimumWidth(100)
        print_btn.clicked.connect(self.print_receipt)
        action_layout.addWidget(print_btn)
        
        pdf_btn = QPushButton('📄 Export PDF')
        pdf_btn.setMinimumWidth(120)
        pdf_btn.clicked.connect(self.export_pdf)
        action_layout.addWidget(pdf_btn)
        
        excel_btn = QPushButton('📊 Export Excel')
        excel_btn.setMinimumWidth(120)
        excel_btn.clicked.connect(self.export_excel)
        action_layout.addWidget(excel_btn)
        
        main_layout.addLayout(action_layout)
        
        self.setLayout(main_layout)
    
    def load_pelanggan_combo(self):
        self.pelanggan_combo.clear()
        pelanggan = self.db.get_all_pelanggan()
        for p in pelanggan:
            self.pelanggan_combo.addItem(f'{p[1]} ({p[4]})', p[0])
    
    def load_barang_combo(self):
        self.barang_combo.clear()
        barang = self.db.get_all_barang()
        for b in barang:
            self.barang_combo.addItem(f'{b[1]} - {b[2]}', b[0])
    
    def on_barang_changed(self):
        if self.barang_combo.count() == 0:
            return
        
        barang_id = self.barang_combo.currentData()
        barang = self.db.get_all_barang()
        
        for b in barang:
            if b[0] == barang_id:
                strata = self.strata_combo.currentText()
                if strata == 'R':
                    harga = b[4]
                elif strata == 'WS':
                    harga = b[5]
                else:
                    harga = b[6]
                
                self.harga_input.setText(f'Rp{harga:,.0f}')
                break
    
    def add_item(self):
        if self.barang_combo.count() == 0:
            QMessageBox.warning(self, 'Peringatan', 'Tambahkan barang terlebih dahulu!')
            return
        
        barang_id = self.barang_combo.currentData()
        barang_text = self.barang_combo.currentText()
        qty = self.qty_input.value()
        harga_text = self.harga_input.text().replace('Rp', '').replace('.', '').replace(',', '.')
        harga = float(harga_text) if harga_text else 0
        diskon = self.diskon_item_input.value()
        
        subtotal = (qty * harga) - diskon
        
        self.current_items.append({
            'barang_id': barang_id,
            'barang_text': barang_text.split(' - ')[1] if ' - ' in barang_text else barang_text,
            'qty': qty,
            'harga': harga,
            'diskon': diskon,
            'subtotal': subtotal
        })
        
        self.update_items_table()
        self.diskon_item_input.setValue(0)
        self.qty_input.setValue(1)
    
    def update_items_table(self):
        self.items_table.setRowCount(len(self.current_items))
        
        for idx, item in enumerate(self.current_items):
            self.items_table.setItem(idx, 0, QTableWidgetItem(str(idx + 1)))
            self.items_table.setItem(idx, 1, QTableWidgetItem(item['barang_text']))
            self.items_table.setItem(idx, 2, QTableWidgetItem(str(item['qty'])))
            self.items_table.setItem(idx, 3, QTableWidgetItem(f'Rp{item["harga"]:,.0f}'))
            self.items_table.setItem(idx, 4, QTableWidgetItem(f'Rp{item["diskon"]:,.0f}'))
            self.items_table.setItem(idx, 5, QTableWidgetItem(f'Rp{item["subtotal"]:,.0f}'))
            
            delete_btn = QPushButton('Hapus')
            delete_btn.clicked.connect(lambda checked, i=idx: self.delete_item(i))
            self.items_table.setCellWidget(idx, 6, delete_btn)
        
        self.update_total()
    
    def delete_item(self, idx):
        del self.current_items[idx]
        self.update_items_table()
    
    def update_diskon_percentage(self):
        subtotal = sum(item['subtotal'] for item in self.current_items)
        pct = self.diskon_pct_input.value()
        diskon = (subtotal * pct) / 100
        self.diskon_total_input.blockSignals(True)
        self.diskon_total_input.setValue(diskon)
        self.diskon_total_input.blockSignals(False)
        self.update_total()
    
    def update_total(self):
        subtotal = sum(item['subtotal'] for item in self.current_items)
        diskon = self.diskon_total_input.value()
        total = subtotal - diskon
        
        self.subtotal_input.setText(f'Rp{subtotal:,.0f}')
        self.total_input.setText(f'Rp{total:,.0f}')
    
    def save_transaksi(self):
        if not self.current_items:
            QMessageBox.warning(self, 'Peringatan', 'Tambahkan item terlebih dahulu!')
            return
        
        pelanggan_id = self.pelanggan_combo.currentData()
        catatan = self.catatan_input.toPlainText()
        
        no_inv = self.inv_input.text()
        transaksi_id = self.db.create_transaksi(no_inv, pelanggan_id, self.user['id'], catatan)
        
        for item in self.current_items:
            self.db.add_detail_transaksi(
                transaksi_id,
                item['barang_id'],
                item['qty'],
                item['harga'],
                item['diskon']
            )
        
        subtotal = sum(item['subtotal'] for item in self.current_items)
        diskon = self.diskon_total_input.value()
        total = subtotal - diskon
        
        self.db.update_transaksi_total(transaksi_id, subtotal, diskon, total)
        self.current_transaksi_id = transaksi_id
        
        QMessageBox.information(self, 'Sukses', 'Transaksi berhasil disimpan!')
        self.clear_form()
    
    def clear_form(self):
        self.inv_input.setText(self.db.generate_no_inv())
        self.tgl_input.setText(datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
        self.current_items = []
        self.update_items_table()
        self.diskon_total_input.setValue(0)
        self.diskon_pct_input.setValue(0)
        self.catatan_input.clear()
    
    def print_receipt(self):
        if not self.current_transaksi_id:
            QMessageBox.warning(self, 'Peringatan', 'Simpan transaksi terlebih dahulu!')
            return
        
        transaksi = self.db.get_transaksi(self.current_transaksi_id)
        detail = self.db.get_detail_transaksi(self.current_transaksi_id)
        
        receipt_data = self._format_receipt(transaksi, detail)
        
        # For now, just show a message (Bluetooth implementation would go here)
        QMessageBox.information(self, 'Cetak', 'Struk siap dicetak ke printer Bluetooth!')
    
    def export_pdf(self):
        if not self.current_transaksi_id:
            QMessageBox.warning(self, 'Peringatan', 'Simpan transaksi terlebih dahulu!')
            return
        
        transaksi = self.db.get_transaksi(self.current_transaksi_id)
        detail = self.db.get_detail_transaksi(self.current_transaksi_id)
        
        filename = f'Invoice_{transaksi[1]}.pdf'
        doc = SimpleDocTemplate(filename, pagesize=letter)
        elements = []
        
        styles = getSampleStyleSheet()
        
        # Title
        title = Paragraph(f'<b>INVOICE {transaksi[1]}</b>', styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 0.2*inch))
        
        # Details
        details_data = [
            ['Tanggal:', transaksi[2]],
            ['Catatan:', transaksi[8]]
        ]
        details_table = Table(details_data)
        details_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
        ]))
        elements.append(details_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Items table
        items_data = [['No', 'Barang', 'Qty', 'Harga', 'Diskon', 'Subtotal']]
        for idx, item in enumerate(detail, 1):
            items_data.append([
                str(idx),
                item[1],
                str(item[3]),
                f"Rp{item[4]:,.0f}",
                f"Rp{item[5]:,.0f}",
                f"Rp{item[6]:,.0f}"
            ])
        
        items_table = Table(items_data)
        items_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(items_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Summary
        summary_data = [
            ['Subtotal:', f'Rp{transaksi[5]:,.0f}'],
            ['Diskon:', f'Rp{transaksi[6]:,.0f}'],
            ['Total:', f'Rp{transaksi[7]:,.0f}']
        ]
        summary_table = Table(summary_data)
        summary_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ]))
        elements.append(summary_table)
        
        doc.build(elements)
        QMessageBox.information(self, 'Sukses', f'PDF berhasil disimpan: {filename}')
    
    def export_excel(self):
        if not self.current_transaksi_id:
            QMessageBox.warning(self, 'Peringatan', 'Simpan transaksi terlebih dahulu!')
            return
        
        transaksi = self.db.get_transaksi(self.current_transaksi_id)
        detail = self.db.get_detail_transaksi(self.current_transaksi_id)
        
        # Create DataFrame
        data = []
        for item in detail:
            data.append({
                'No': item[0],
                'Barang': item[1],
                'Kode': item[2],
                'Qty': item[3],
                'Harga Satuan': item[4],
                'Diskon': item[5],
                'Subtotal': item[6]
            })
        
        df = pd.DataFrame(data)
        filename = f'Invoice_{transaksi[1]}.xlsx'
        df.to_excel(filename, index=False, sheet_name='Invoice')
        
        QMessageBox.information(self, 'Sukses', f'Excel berhasil disimpan: {filename}')
    
    def _format_receipt(self, transaksi, detail):
        lines = []
        lines.append('=== STRUK PENJUALAN ===')
        lines.append(f'Invoice: {transaksi[1]}')
        lines.append(f'Tanggal: {transaksi[2]}')
        lines.append('')
        lines.append('DETAIL ITEM')
        lines.append('-' * 40)
        
        for item in detail:
            lines.append(f'{item[1]}')
            lines.append(f'Qty: {item[3]} x Rp{item[4]:,.0f}')
            lines.append(f'Subtotal: Rp{item[6]:,.0f}')
            lines.append('')
        
        lines.append('-' * 40)
        lines.append(f'Total: Rp{transaksi[7]:,.0f}')
        lines.append('=== TERIMA KASIH ===')
        
        return lines
