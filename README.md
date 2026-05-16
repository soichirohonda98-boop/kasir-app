# Aplikasi Kasir Lengkap

Aplikasi Desktop untuk sistem kasir modern dengan fitur lengkap:

## Fitur Utama

✅ **Login & Keamanan**
- Login menggunakan NIK dan Password
- Sistem registrasi user baru
- Password encryption dengan bcrypt

✅ **Transaksi Penjualan**
- Pembuatan invoice otomatis
- Manajemen item dengan Qty dan harga
- Diskon per item dan diskon total (% atau nominal)
- Struk cetak via Bluetooth printer
- Export ke PDF dan Excel
- Catatan transaksi

✅ **Data Master**
- **Barang**: Kode, Nama, Stok, Harga R (Retail), Harga WS (Wholesaler), Harga SO (Semi Wholesaler)
- **Pelanggan**: Nama, Alamat, No Telp, Tipe (R/WS/SO)

✅ **Laporan**
- Daftar semua transaksi
- Export laporan ke Excel
- Detail setiap transaksi

✅ **Interface**
- Tema ungu putih yang profesional
- Design modern dan user-friendly
- Tab-based navigation

## Instalasi

```bash
pip install -r requirements.txt
python main.py
```

## Database

Aplikasi menggunakan SQLite dengan struktur:
- **users**: Akun login kasir
- **barang**: Data barang/produk
- **pelanggan**: Data customer
- **transaksi**: Header transaksi
- **detail_transaksi**: Item dalam transaksi

## Setup Pertama

1. Jalankan aplikasi
2. Klik "Daftar" untuk membuat akun pertama
3. Login dengan NIK dan password
4. Tambahkan data barang dan pelanggan
5. Mulai membuat transaksi

## Printer Bluetooth

Untuk menggunakan fitur cetak Bluetooth:
1. Pasangkan printer dengan komputer
2. Tentukan port COM pada konfigurasi
3. Klik "Cetak" untuk mengirim struk

## Lisensi

Free for personal use
