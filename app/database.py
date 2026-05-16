import sqlite3
import os
import bcrypt
from datetime import datetime

DB_PATH = 'kasir_app.db'

class Database:
    def __init__(self):
        self.init_db()
    
    def get_connection(self):
        return sqlite3.connect(DB_PATH)
    
    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabel User
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                nik TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                nama TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabel Barang
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS barang (
                id INTEGER PRIMARY KEY,
                kode TEXT UNIQUE NOT NULL,
                nama TEXT NOT NULL,
                stok INTEGER DEFAULT 0,
                harga_r REAL NOT NULL,
                harga_ws REAL NOT NULL,
                harga_so REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabel Pelanggan
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pelanggan (
                id INTEGER PRIMARY KEY,
                nama TEXT NOT NULL,
                alamat TEXT,
                no_telp TEXT,
                tipe TEXT DEFAULT 'R',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabel Transaksi
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transaksi (
                id INTEGER PRIMARY KEY,
                no_inv TEXT UNIQUE NOT NULL,
                tgl_transaksi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                pelanggan_id INTEGER,
                user_id INTEGER,
                subtotal REAL DEFAULT 0,
                diskon REAL DEFAULT 0,
                total REAL DEFAULT 0,
                catatan TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (pelanggan_id) REFERENCES pelanggan(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Tabel Detail Transaksi
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS detail_transaksi (
                id INTEGER PRIMARY KEY,
                transaksi_id INTEGER,
                barang_id INTEGER,
                qty INTEGER DEFAULT 1,
                harga_satuan REAL NOT NULL,
                diskon_item REAL DEFAULT 0,
                subtotal REAL DEFAULT 0,
                FOREIGN KEY (transaksi_id) REFERENCES transaksi(id),
                FOREIGN KEY (barang_id) REFERENCES barang(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    # ===== USER METHODS =====
    def add_user(self, nik, password, nama):
        try:
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (nik, password, nama) VALUES (?, ?, ?)
            ''', (nik, hashed, nama))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def verify_user(self, nik, password):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, password, nama FROM users WHERE nik = ?', (nik,))
        result = cursor.fetchone()
        conn.close()
        
        if result and bcrypt.checkpw(password.encode(), result[1]):
            return {'id': result[0], 'nama': result[2]}
        return None
    
    # ===== BARANG METHODS =====
    def add_barang(self, kode, nama, harga_r, harga_ws, harga_so):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO barang (kode, nama, harga_r, harga_ws, harga_so)
                VALUES (?, ?, ?, ?, ?)
            ''', (kode, nama, harga_r, harga_ws, harga_so))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def get_all_barang(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, kode, nama, stok, harga_r, harga_ws, harga_so FROM barang')
        data = cursor.fetchall()
        conn.close()
        return data
    
    def update_barang(self, barang_id, **kwargs):
        conn = self.get_connection()
        cursor = conn.cursor()
        for key, value in kwargs.items():
            cursor.execute(f'UPDATE barang SET {key} = ? WHERE id = ?', (value, barang_id))
        conn.commit()
        conn.close()
    
    def delete_barang(self, barang_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM barang WHERE id = ?', (barang_id,))
        conn.commit()
        conn.close()
    
    # ===== PELANGGAN METHODS =====
    def add_pelanggan(self, nama, alamat, no_telp, tipe):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO pelanggan (nama, alamat, no_telp, tipe)
                VALUES (?, ?, ?, ?)
            ''', (nama, alamat, no_telp, tipe))
            conn.commit()
            pelanggan_id = cursor.lastrowid
            conn.close()
            return pelanggan_id
        except:
            return None
    
    def get_all_pelanggan(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, nama, alamat, no_telp, tipe FROM pelanggan')
        data = cursor.fetchall()
        conn.close()
        return data
    
    def update_pelanggan(self, pelanggan_id, **kwargs):
        conn = self.get_connection()
        cursor = conn.cursor()
        for key, value in kwargs.items():
            cursor.execute(f'UPDATE pelanggan SET {key} = ? WHERE id = ?', (value, pelanggan_id))
        conn.commit()
        conn.close()
    
    def delete_pelanggan(self, pelanggan_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM pelanggan WHERE id = ?', (pelanggan_id,))
        conn.commit()
        conn.close()
    
    # ===== TRANSAKSI METHODS =====
    def create_transaksi(self, no_inv, pelanggan_id, user_id, catatan=''):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO transaksi (no_inv, pelanggan_id, user_id, catatan)
            VALUES (?, ?, ?, ?)
        ''', (no_inv, pelanggan_id, user_id, catatan))
        conn.commit()
        transaksi_id = cursor.lastrowid
        conn.close()
        return transaksi_id
    
    def add_detail_transaksi(self, transaksi_id, barang_id, qty, harga_satuan, diskon_item=0):
        conn = self.get_connection()
        cursor = conn.cursor()
        subtotal = (qty * harga_satuan) - diskon_item
        cursor.execute('''
            INSERT INTO detail_transaksi (transaksi_id, barang_id, qty, harga_satuan, diskon_item, subtotal)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (transaksi_id, barang_id, qty, harga_satuan, diskon_item, subtotal))
        conn.commit()
        conn.close()
    
    def update_transaksi_total(self, transaksi_id, subtotal, diskon, total):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE transaksi SET subtotal = ?, diskon = ?, total = ?
            WHERE id = ?
        ''', (subtotal, diskon, total, transaksi_id))
        conn.commit()
        conn.close()
    
    def get_transaksi(self, transaksi_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, no_inv, tgl_transaksi, pelanggan_id, user_id, subtotal, diskon, total, catatan
            FROM transaksi WHERE id = ?
        ''', (transaksi_id,))
        data = cursor.fetchone()
        conn.close()
        return data
    
    def get_detail_transaksi(self, transaksi_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT dt.id, b.nama, b.kode, dt.qty, dt.harga_satuan, dt.diskon_item, dt.subtotal
            FROM detail_transaksi dt
            JOIN barang b ON dt.barang_id = b.id
            WHERE dt.transaksi_id = ?
        ''', (transaksi_id,))
        data = cursor.fetchall()
        conn.close()
        return data
    
    def get_all_transaksi(self, limit=100):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, no_inv, tgl_transaksi, pelanggan_id, subtotal, diskon, total
            FROM transaksi ORDER BY tgl_transaksi DESC LIMIT ?
        ''', (limit,))
        data = cursor.fetchall()
        conn.close()
        return data
    
    def generate_no_inv(self):
        from datetime import datetime
        conn = self.get_connection()
        cursor = conn.cursor()
        today = datetime.now().strftime('%Y%m%d')
        cursor.execute('SELECT COUNT(*) FROM transaksi WHERE no_inv LIKE ?', (f'{today}%',))
        count = cursor.fetchone()[0] + 1
        conn.close()
        return f'{today}{str(count).zfill(4)}'
