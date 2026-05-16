// Aplikasi Kasir Web Version
const app = {
    // Data Storage (menggunakan localStorage)
    users: [],
    barang: [],
    pelanggan: [],
    transaksi: [],
    currentUser: null,
    currentItems: [],
    currentTransaksiId: null,

    // Inisialisasi
    init() {
        this.loadData();
        this.setCurrentDate();
        this.attachEventListeners();
        console.log('App initialized');
    },

    // Load data dari localStorage
    loadData() {
        this.users = JSON.parse(localStorage.getItem('users')) || [];
        this.barang = JSON.parse(localStorage.getItem('barang')) || [];
        this.pelanggan = JSON.parse(localStorage.getItem('pelanggan')) || [];
        this.transaksi = JSON.parse(localStorage.getItem('transaksi')) || [];
        this.currentUser = JSON.parse(localStorage.getItem('currentUser')) || null;

        // Jika sudah login, tampilkan main page
        if (this.currentUser) {
            this.showMainPage();
        }
    },

    // Save data ke localStorage
    saveData() {
        localStorage.setItem('users', JSON.stringify(this.users));
        localStorage.setItem('barang', JSON.stringify(this.barang));
        localStorage.setItem('pelanggan', JSON.stringify(this.pelanggan));
        localStorage.setItem('transaksi', JSON.stringify(this.transaksi));
        localStorage.setItem('currentUser', JSON.stringify(this.currentUser));
    },

    // Attach event listeners
    attachEventListeners() {
        document.getElementById('loginPassword').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.login();
        });
        document.getElementById('regConfirm').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.register();
        });
        document.getElementById('barangSelect').addEventListener('change', () => this.updateHarga());
    },

    // ===== LOGIN & REGISTER =====
    login() {
        const nik = document.getElementById('loginNik').value.trim();
        const password = document.getElementById('loginPassword').value.trim();

        if (!nik || !password) {
            alert('NIK dan Password harus diisi!');
            return;
        }

        const user = this.users.find(u => u.nik === nik && u.password === password);
        if (user) {
            this.currentUser = user;
            this.saveData();
            this.showMainPage();
        } else {
            alert('NIK atau Password salah!');
        }
    },

    register() {
        const nik = document.getElementById('regNik').value.trim();
        const nama = document.getElementById('regNama').value.trim();
        const password = document.getElementById('regPassword').value.trim();
        const confirm = document.getElementById('regConfirm').value.trim();

        if (!nik || !nama || !password || !confirm) {
            alert('Semua field harus diisi!');
            return;
        }

        if (password !== confirm) {
            alert('Password tidak cocok!');
            return;
        }

        if (password.length < 6) {
            alert('Password minimal 6 karakter!');
            return;
        }

        if (this.users.find(u => u.nik === nik)) {
            alert('NIK sudah terdaftar!');
            return;
        }

        this.users.push({
            id: Date.now(),
            nik,
            nama,
            password
        });

        this.saveData();
        alert('Akun berhasil dibuat! Silakan login.');
        this.showLogin();
    },

    showLogin() {
        document.getElementById('loginForm').classList.remove('hidden');
        document.getElementById('registerForm').classList.add('hidden');
    },

    showRegister() {
        document.getElementById('loginForm').classList.add('hidden');
        document.getElementById('registerForm').classList.remove('hidden');
    },

    logout() {
        if (confirm('Yakin ingin logout?')) {
            this.currentUser = null;
            this.currentItems = [];
            this.saveData();
            this.showLoginPage();
        }
    },

    showLoginPage() {
        document.getElementById('loginPage').classList.add('active');
        document.getElementById('mainPage').classList.remove('active');
        document.getElementById('loginNik').value = '';
        document.getElementById('loginPassword').value = '';
        document.getElementById('regNik').value = '';
        document.getElementById('regNama').value = '';
        document.getElementById('regPassword').value = '';
        document.getElementById('regConfirm').value = '';
        this.showLogin();
    },

    showMainPage() {
        document.getElementById('loginPage').classList.remove('active');
        document.getElementById('mainPage').classList.add('active');
        document.getElementById('userName').textContent = this.currentUser.nama;
        this.refreshAllSelects();
        this.refreshAllTables();
        this.clearForm();
    },

    // ===== TAB SWITCHING =====
    switchTab(tabName) {
        // Hide all tabs
        document.querySelectorAll('.tab-pane').forEach(el => {
            el.classList.remove('active');
        });

        // Remove active from all buttons
        document.querySelectorAll('.tab-btn').forEach(el => {
            el.classList.remove('active');
        });

        // Show selected tab
        document.getElementById(tabName + 'Tab').classList.add('active');

        // Add active to clicked button
        event.target.classList.add('active');

        // Refresh data
        if (tabName === 'barang') {
            this.refreshBarangTable();
        } else if (tabName === 'pelanggan') {
            this.refreshPelangganTable();
        } else if (tabName === 'laporan') {
            this.refreshLaporan();
        }
    },

    // ===== BARANG =====
    addBarang() {
        const kode = document.getElementById('kodeBarang').value.trim();
        const nama = document.getElementById('namaBarang').value.trim();
        const hargaR = parseFloat(document.getElementById('hargaR').value) || 0;
        const hargaWS = parseFloat(document.getElementById('hargaWS').value) || 0;
        const hargaSO = parseFloat(document.getElementById('hargaSO').value) || 0;

        if (!kode || !nama) {
            alert('Kode dan Nama harus diisi!');
            return;
        }

        if (this.barang.find(b => b.kode === kode)) {
            alert('Kode barang sudah ada!');
            return;
        }

        this.barang.push({
            id: Date.now(),
            kode,
            nama,
            hargaR,
            hargaWS,
            hargaSO
        });

        this.saveData();
        alert('Barang berhasil ditambahkan!');
        this.clearBarangForm();
        this.refreshBarangTable();
        this.refreshBarangSelect();
    },

    deleteBarang(id) {
        if (confirm('Yakin ingin menghapus barang ini?')) {
            this.barang = this.barang.filter(b => b.id !== id);
            this.saveData();
            this.refreshBarangTable();
            this.refreshBarangSelect();
        }
    },

    clearBarangForm() {
        document.getElementById('kodeBarang').value = '';
        document.getElementById('namaBarang').value = '';
        document.getElementById('hargaR').value = '';
        document.getElementById('hargaWS').value = '';
        document.getElementById('hargaSO').value = '';
    },

    refreshBarangTable() {
        const tbody = document.querySelector('#barangTable tbody');
        tbody.innerHTML = '';

        this.barang.forEach(b => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${b.id}</td>
                <td>${b.kode}</td>
                <td>${b.nama}</td>
                <td>Rp${b.hargaR.toLocaleString('id-ID')}</td>
                <td>Rp${b.hargaWS.toLocaleString('id-ID')}</td>
                <td>Rp${b.hargaSO.toLocaleString('id-ID')}</td>
                <td><button class="btn-danger" onclick="app.deleteBarang(${b.id})">Hapus</button></td>
            `;
            tbody.appendChild(row);
        });
    },

    refreshBarangSelect() {
        const select = document.getElementById('barangSelect');
        const currentValue = select.value;
        select.innerHTML = '<option value="">-- Pilih Barang --</option>';

        this.barang.forEach(b => {
            const option = document.createElement('option');
            option.value = b.id;
            option.textContent = `${b.kode} - ${b.nama}`;
            select.appendChild(option);
        });

        select.value = currentValue;
    },

    // ===== PELANGGAN =====
    addPelanggan() {
        const nama = document.getElementById('namaPelanggan').value.trim();
        const alamat = document.getElementById('alamatPelanggan').value.trim();
        const telp = document.getElementById('telpPelanggan').value.trim();
        const tipe = document.getElementById('tipePelanggan').value;

        if (!nama) {
            alert('Nama harus diisi!');
            return;
        }

        this.pelanggan.push({
            id: Date.now(),
            nama,
            alamat,
            telp,
            tipe
        });

        this.saveData();
        alert('Pelanggan berhasil ditambahkan!');
        this.clearPelangganForm();
        this.refreshPelangganTable();
        this.refreshPelangganSelect();
    },

    deletePelanggan(id) {
        if (confirm('Yakin ingin menghapus pelanggan ini?')) {
            this.pelanggan = this.pelanggan.filter(p => p.id !== id);
            this.saveData();
            this.refreshPelangganTable();
            this.refreshPelangganSelect();
        }
    },

    clearPelangganForm() {
        document.getElementById('namaPelanggan').value = '';
        document.getElementById('alamatPelanggan').value = '';
        document.getElementById('telpPelanggan').value = '';
        document.getElementById('tipePelanggan').value = 'R';
    },

    refreshPelangganTable() {
        const tbody = document.querySelector('#pelangganTable tbody');
        tbody.innerHTML = '';

        this.pelanggan.forEach(p => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${p.id}</td>
                <td>${p.nama}</td>
                <td>${p.alamat}</td>
                <td>${p.telp}</td>
                <td>${p.tipe}</td>
                <td><button class="btn-danger" onclick="app.deletePelanggan(${p.id})">Hapus</button></td>
            `;
            tbody.appendChild(row);
        });
    },

    refreshPelangganSelect() {
        const select = document.getElementById('pelangganSelect');
        const currentValue = select.value;
        select.innerHTML = '<option value="">-- Pilih Pelanggan --</option>';

        this.pelanggan.forEach(p => {
            const option = document.createElement('option');
            option.value = p.id;
            option.textContent = `${p.nama} (${p.tipe})`;
            select.appendChild(option);
        });

        select.value = currentValue;
    },

    // ===== TRANSAKSI =====
    setCurrentDate() {
        const now = new Date();
        const formatted = now.toLocaleDateString('id-ID') + ' ' + now.toLocaleTimeString('id-ID');
        document.getElementById('tglTransaksi').value = formatted;
    },

    generateNoInvoice() {
        const now = new Date();
        const dateStr = now.toISOString().slice(0, 10).replace(/-/g, '');
        const count = this.transaksi.filter(t => t.noInv.startsWith(dateStr)).length + 1;
        return dateStr + String(count).padStart(4, '0');
    },

    updateHarga() {
        const barangId = document.getElementById('barangSelect').value;
        const strata = document.getElementById('strataSelect').value;

        if (!barangId) {
            document.getElementById('hargaDisplay').value = '';
            return;
        }

        const barang = this.barang.find(b => b.id == barangId);
        if (barang) {
            let harga = 0;
            if (strata === 'R') harga = barang.hargaR;
            else if (strata === 'WS') harga = barang.hargaWS;
            else harga = barang.hargaSO;

            document.getElementById('hargaDisplay').value = 'Rp' + harga.toLocaleString('id-ID');
        }
    },

    addItem() {
        const barangId = document.getElementById('barangSelect').value;
        const qty = parseInt(document.getElementById('qtyInput').value) || 1;
        const diskon = parseFloat(document.getElementById('diskonItemInput').value) || 0;

        if (!barangId) {
            alert('Pilih barang terlebih dahulu!');
            return;
        }

        const barang = this.barang.find(b => b.id == barangId);
        const strata = document.getElementById('strataSelect').value;
        let harga = 0;
        if (strata === 'R') harga = barang.hargaR;
        else if (strata === 'WS') harga = barang.hargaWS;
        else harga = barang.hargaSO;

        const subtotal = (qty * harga) - diskon;

        this.currentItems.push({
            barangId,
            nama: barang.nama,
            qty,
            harga,
            diskon,
            subtotal
        });

        this.updateItemsTable();
        document.getElementById('diskonItemInput').value = '0';
        document.getElementById('qtyInput').value = '1';
    },

    deleteItem(idx) {
        this.currentItems.splice(idx, 1);
        this.updateItemsTable();
    },

    updateItemsTable() {
        const tbody = document.querySelector('#itemsTable tbody');
        tbody.innerHTML = '';

        this.currentItems.forEach((item, idx) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${idx + 1}</td>
                <td>${item.nama}</td>
                <td>${item.qty}</td>
                <td>Rp${item.harga.toLocaleString('id-ID')}</td>
                <td>Rp${item.diskon.toLocaleString('id-ID')}</td>
                <td>Rp${item.subtotal.toLocaleString('id-ID')}</td>
                <td><button class="btn-danger" onclick="app.deleteItem(${idx})">Hapus</button></td>
            `;
            tbody.appendChild(row);
        });

        this.updateTotal();
    },

    updateDiskonPercentage() {
        const subtotal = this.currentItems.reduce((sum, item) => sum + item.subtotal, 0);
        const pct = parseFloat(document.getElementById('diskonPctInput').value) || 0;
        const diskon = (subtotal * pct) / 100;

        document.getElementById('diskonTotalInput').value = diskon;
        this.updateTotal();
    },

    updateTotal() {
        const subtotal = this.currentItems.reduce((sum, item) => sum + item.subtotal, 0);
        const diskon = parseFloat(document.getElementById('diskonTotalInput').value) || 0;
        const total = subtotal - diskon;

        document.getElementById('subtotalDisplay').value = 'Rp' + subtotal.toLocaleString('id-ID');
        document.getElementById('totalDisplay').value = 'Rp' + total.toLocaleString('id-ID');
    },

    saveTransaksi() {
        if (this.currentItems.length === 0) {
            alert('Tambahkan item terlebih dahulu!');
            return;
        }

        const pelangganId = document.getElementById('pelangganSelect').value;
        const subtotal = this.currentItems.reduce((sum, item) => sum + item.subtotal, 0);
        const diskon = parseFloat(document.getElementById('diskonTotalInput').value) || 0;
        const total = subtotal - diskon;
        const catatan = document.getElementById('catatanInput').value.trim();

        const transaksi = {
            id: Date.now(),
            noInv: this.generateNoInvoice(),
            tglTransaksi: new Date().toLocaleString('id-ID'),
            pelangganId,
            userId: this.currentUser.id,
            items: JSON.parse(JSON.stringify(this.currentItems)),
            subtotal,
            diskon,
            total,
            catatan
        };

        this.transaksi.push(transaksi);
        this.saveData();
        this.currentTransaksiId = transaksi.id;

        alert('Transaksi berhasil disimpan!');
        this.clearForm();
    },

    clearForm() {
        this.currentItems = [];
        document.getElementById('noInvoice').value = this.generateNoInvoice();
        document.getElementById('pelangganSelect').value = '';
        document.getElementById('barangSelect').value = '';
        document.getElementById('strataSelect').value = 'R';
        document.getElementById('hargaDisplay').value = '';
        document.getElementById('qtyInput').value = '1';
        document.getElementById('diskonItemInput').value = '0';
        document.getElementById('diskonTotalInput').value = '0';
        document.getElementById('diskonPctInput').value = '0';
        document.getElementById('catatanInput').value = '';
        this.updateItemsTable();
        this.setCurrentDate();
    },

    printReceipt() {
        if (!this.currentTransaksiId) {
            alert('Simpan transaksi terlebih dahulu!');
            return;
        }

        const transaksi = this.transaksi.find(t => t.id === this.currentTransaksiId);
        let receipt = '\n=== STRUK PENJUALAN ===\n';
        receipt += `Invoice: ${transaksi.noInv}\n`;
        receipt += `Tanggal: ${transaksi.tglTransaksi}\n\n`;
        receipt += 'DETAIL ITEM\n';
        receipt += '-'.repeat(40) + '\n';

        transaksi.items.forEach(item => {
            receipt += `${item.nama}\n`;
            receipt += `Qty: ${item.qty} x Rp${item.harga.toLocaleString('id-ID')}\n`;
            receipt += `Subtotal: Rp${item.subtotal.toLocaleString('id-ID')}\n\n`;
        });

        receipt += '-'.repeat(40) + '\n';
        receipt += `Total: Rp${transaksi.total.toLocaleString('id-ID')}\n`;
        receipt += '=== TERIMA KASIH ===\n';

        console.log(receipt);
        alert('Struk siap untuk dicetak:\n' + receipt);
        window.print();
    },

    exportPDF() {
        if (!this.currentTransaksiId) {
            alert('Simpan transaksi terlebih dahulu!');
            return;
        }

        const transaksi = this.transaksi.find(t => t.id === this.currentTransaksiId);
        const pelanggan = this.pelanggan.find(p => p.id == transaksi.pelangganId);

        let html = `
            <!DOCTYPE html>
            <html>
            <head>
                <title>Invoice ${transaksi.noInv}</title>
                <style>
                    body { font-family: Arial; margin: 20px; }
                    h1 { color: #7b2cbf; }
                    table { width: 100%; border-collapse: collapse; margin: 20px 0; }
                    th { background-color: #7b2cbf; color: white; padding: 10px; text-align: left; }
                    td { padding: 10px; border-bottom: 1px solid #ddd; }
                    .summary { text-align: right; margin-top: 20px; }
                </style>
            </head>
            <body>
                <h1>INVOICE ${transaksi.noInv}</h1>
                <p><strong>Tanggal:</strong> ${transaksi.tglTransaksi}</p>
                <p><strong>Pelanggan:</strong> ${pelanggan ? pelanggan.nama : 'N/A'}</p>
                
                <table>
                    <thead>
                        <tr>
                            <th>No</th>
                            <th>Barang</th>
                            <th>Qty</th>
                            <th>Harga Satuan</th>
                            <th>Diskon</th>
                            <th>Subtotal</th>
                        </tr>
                    </thead>
                    <tbody>
        `;

        transaksi.items.forEach((item, idx) => {
            html += `
                <tr>
                    <td>${idx + 1}</td>
                    <td>${item.nama}</td>
                    <td>${item.qty}</td>
                    <td>Rp${item.harga.toLocaleString('id-ID')}</td>
                    <td>Rp${item.diskon.toLocaleString('id-ID')}</td>
                    <td>Rp${item.subtotal.toLocaleString('id-ID')}</td>
                </tr>
            `;
        });

        html += `
                    </tbody>
                </table>
                
                <div class="summary">
                    <p><strong>Subtotal:</strong> Rp${transaksi.subtotal.toLocaleString('id-ID')}</p>
                    <p><strong>Diskon:</strong> Rp${transaksi.diskon.toLocaleString('id-ID')}</p>
                    <p style="font-size: 18px;"><strong>Total:</strong> Rp${transaksi.total.toLocaleString('id-ID')}</p>
                </div>
            </body>
            </html>
        `;

        const blob = new Blob([html], { type: 'text/html' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `Invoice_${transaksi.noInv}.html`;
        a.click();
    },

    exportExcel() {
        if (!this.currentTransaksiId) {
            alert('Simpan transaksi terlebih dahulu!');
            return;
        }

        const transaksi = this.transaksi.find(t => t.id === this.currentTransaksiId);
        let csv = 'No,Barang,Qty,Harga Satuan,Diskon,Subtotal\n';

        transaksi.items.forEach((item, idx) => {
            csv += `${idx + 1},${item.nama},${item.qty},${item.harga},${item.diskon},${item.subtotal}\n`;
        });

        csv += '\nSummary\n';
        csv += `Subtotal,${transaksi.subtotal}\n`;
        csv += `Diskon,${transaksi.diskon}\n`;
        csv += `Total,${transaksi.total}\n`;

        const blob = new Blob([csv], { type: 'text/csv' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `Invoice_${transaksi.noInv}.csv`;
        a.click();
    },

    // ===== LAPORAN =====
    refreshLaporan() {
        const tbody = document.querySelector('#laporanTable tbody');
        tbody.innerHTML = '';

        this.transaksi.forEach(t => {
            const pelanggan = this.pelanggan.find(p => p.id == t.pelangganId);
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${t.noInv}</td>
                <td>${t.tglTransaksi}</td>
                <td>${pelanggan ? pelanggan.nama : 'N/A'}</td>
                <td>Rp${t.subtotal.toLocaleString('id-ID')}</td>
                <td>Rp${t.diskon.toLocaleString('id-ID')}</td>
                <td>Rp${t.total.toLocaleString('id-ID')}</td>
                <td><button class="btn-primary" onclick="app.viewDetail(${t.id})">Lihat</button></td>
            `;
            tbody.appendChild(row);
        });
    },

    viewDetail(id) {
        const transaksi = this.transaksi.find(t => t.id === id);
        if (transaksi) {
            let detail = `Invoice: ${transaksi.noInv}\nTanggal: ${transaksi.tglTransaksi}\n\nDetail Item:\n`;
            transaksi.items.forEach(item => {
                detail += `- ${item.nama}: ${item.qty}x Rp${item.harga.toLocaleString('id-ID')} = Rp${item.subtotal.toLocaleString('id-ID')}\n`;
            });
            detail += `\nTotal: Rp${transaksi.total.toLocaleString('id-ID')}`;
            alert(detail);
        }
    },

    exportLaporanExcel() {
        let csv = 'No. Invoice,Tanggal,Pelanggan,Subtotal,Diskon,Total\n';

        this.transaksi.forEach(t => {
            const pelanggan = this.pelanggan.find(p => p.id == t.pelangganId);
            csv += `${t.noInv},${t.tglTransaksi},${pelanggan ? pelanggan.nama : 'N/A'},${t.subtotal},${t.diskon},${t.total}\n`;
        });

        const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'Laporan_Transaksi.csv';
        a.click();
    },

    // ===== HELPER FUNCTIONS =====
    refreshAllSelects() {
        this.refreshBarangSelect();
        this.refreshPelangganSelect();
    },

    refreshAllTables() {
        this.refreshBarangTable();
        this.refreshPelangganTable();
        this.refreshLaporan();
    }
};

// Initialize app when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => app.init());
} else {
    app.init();
}
