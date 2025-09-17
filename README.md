# 🤖 BOT INFO FREEBET GACOR - V3 (Multifungsi & Stabil)

[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/yourusername/info-freebet-gacor-bot)

Selamat datang di versi terbaru Bot Info Freebet Gacor! Bot ini dirancang ulang dari awal untuk menjadi lebih stabil, multifungsi, dan mudah digunakan.

## ✨ Fitur Unggulan

### 🎯 **Fitur Utama**
- **Menu Interaktif Berbasis Tombol**: Pengaturan mudah melalui inline keyboard
- **Welcome Message Kustom**: Atur teks, tombol, dan gambar untuk pesan selamat datang
- **Auto Broadcast**: Kirim pesan berulang secara otomatis ke semua pengguna
- **Manajemen Admin**: Tambah dan hapus admin dengan mudah
- **Database JSON**: Semua data (user, settings) disimpan dalam satu file `bot_database.json`

### 🚀 **Fitur Canggih**
- **Preview System**: Preview semua jenis pesan sebelum dikirim
- **Placeholder Otomatis**: Support `{NAME}`, `{USERNAME}`, `{ID}`, `{DATE}`, dll.
- **Backup & Restore**: Export/import database lengkap
- **Custom Commands**: Response otomatis untuk command kustom
- **Scheduled Messages**: Pesan terjadwal berdasarkan waktu
- **Anti-Spam System**: Deteksi spam otomatis
- **Sang Mata**: Track log user by username
- **Export CSV**: Export data user ke format CSV
- **Breadcrumb Navigation**: Navigasi kembali ke menu terakhir
- **Reaction Animation**: Animasi emoji random di /start

### 🔧 **Fitur Developer**
- **Struktur Kode Bersih**: Lebih mudah dipahami dan dikembangkan
- **Command List Dinamis**: Daftar command otomatis muncul di Telegram
- **Error Handling**: Penanganan error yang komprehensif
- **Logging System**: Sistem logging aktivitas user

## 🚀 Cara Setup Cepat

### **Opsi 1: Jalankan Lokal**

1. **Pastikan Python Terinstall**
   - Download dan install Python 3.11+ dari [python.org](https://python.org).
   - Pastikan Anda mencentang "Add Python to PATH" saat instalasi.

2. **Buka Terminal**
   - Masuk ke folder `info_freebet_gacor` ini melalui terminal atau command prompt.

3. **Install Dependencies**
   - Jalankan command berikut untuk menginstall library yang dibutuhkan:
     ```bash
     pip install -r requirements.txt
     ```

4. **Jalankan Bot**
   - Setelah instalasi selesai, jalankan bot dengan command:
     ```bash
     python bot.py
     ```

5. **Selesai!**
   - Bot Anda sekarang sudah online dan siap digunakan. Cari nama bot Anda di Telegram dan kirim `/start`.

### **Opsi 2: Deploy ke Heroku (24/7 Online)**

#### **Deploy Otomatis (One-Click)**
1. Klik tombol "Deploy to Heroku" di atas
2. Masukkan nama aplikasi Heroku Anda
3. Masukkan Telegram Bot Token Anda
4. Klik "Deploy app"
5. Tunggu proses deploy selesai (5-10 menit)
6. Bot Anda sudah online 24/7!

#### **Deploy Manual**
1. **Install Heroku CLI**
   ```bash
   # Download dari: https://devcenter.heroku.com/articles/heroku-cli
   heroku login
   ```

2. **Clone & Setup**
   ```bash
   git clone https://github.com/yourusername/info-freebet-gacor-bot.git
   cd info-freebet-gacor-bot
   heroku create nama-app-anda
   ```

3. **Set Environment Variables**
   ```bash
   heroku config:set TOKEN=your_telegram_bot_token_here
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

5. **Scale Worker**
   ```bash
   heroku ps:scale worker=1
   ```

#### **Script Deploy Cepat**
Gunakan script `deploy.sh` untuk deployment otomatis:
```bash
chmod +x deploy.sh
./deploy.sh
```

### **Opsi 3: Deploy ke Platform Lain**

Bot ini juga kompatibel dengan:
- **Railway**: Import dari GitHub repository
- **Render**: Connect GitHub repository
- **Vercel**: Deploy sebagai serverless function
- **DigitalOcean App Platform**: Import dari GitHub

## ⚙️ Konfigurasi Awal
Bot ini dirancang untuk bekerja `out-of-the-box` dengan konfigurasi default yang sudah disiapkan.

- **Token Bot**: `8067260760:AAF9qWxEtNBFe-b8afJHmVp8tMD9JlkE4LI`
- **Admin Utama**: `6592870669`
- **Pesan Welcome**: Sudah diatur sesuai contoh gambar.
- **Tombol Welcome**: Sudah diatur sesuai contoh gambar.

Anda bisa mengubah semua ini nanti melalui command settings yang akan datang.

## 📋 Daftar Command

### 👥 **Untuk Semua User:**
- `/start` - ▶️ Mulai bot dengan welcome message
- `/help` - ℹ️ Lihat daftar command
- `/guide` - 📚 Guide placeholder pesan
- `/getid` - 🆔 Dapatkan ID user/chat

### 👑 **Untuk Admin:**
- `/settings` - ⚙️ Menu pengaturan utama
- `/broadcast` - 📢 Kirim pesan ke semua user
- `/stats` - 📊 Lihat statistik bot
- `/listusers` - 👥 Lihat daftar user
- `/sangmata` - 👁️ Cari user by username

### 🎯 **Placeholder yang Tersedia:**
- `{NAME}` - Nama depan user
- `{USERNAME}` - Username dengan @
- `{ID}` - ID Telegram user
- `{DATE}` - Tanggal (DD/MM/YYYY)
- `{TIME}` - Waktu (HH:MM:SS)
- `{FULLDATE}` - Tanggal & waktu lengkap
- `{DAY}` - Hari (Monday, Tuesday, dll.)
- `{MONTH}` - Bulan (January, February, dll.)
- `{YEAR}` - Tahun


## 🛠️ Pengembangan Selanjutnya (Roadmap)
Versi saat ini adalah fondasi yang stabil. Fitur-fitur berikut akan ditambahkan melalui **menu interaktif berbasis tombol** pada command `/settings`:

- **Manajemen Welcome Message**:
  - `Setel Teks Welcome`: Ubah teks pesan selamat datang.
  - `Setel Foto Welcome`: Ganti atau hapus foto.
  - `Tambah/Hapus Tombol`: Kelola tombol inline di bawah pesan welcome.

- **Manajemen Auto Broadcast**:
  - `Aktifkan/Nonaktifkan`: Menyalakan atau mematikan auto broadcast.
  - `Setel Pesan`: Mengubah isi pesan yang dikirim otomatis.
  - `Setel Interval`: Mengatur jeda waktu pengiriman (dalam menit).

- **Manajemen Admin**:
  - `Tambah Admin`: Menambah user ID sebagai admin baru.
  - `Hapus Admin`: Menghapus admin.
  - `Lihat Admin`: Menampilkan daftar semua admin.

## 📁 Struktur File

### **File Utama:**
- `bot.py` - File utama yang berisi semua logika bot
- `requirements.txt` - Daftar library Python yang dibutuhkan
- `Procfile` - Konfigurasi worker untuk Heroku
- `runtime.txt` - Versi Python untuk Heroku
- `app.json` - Konfigurasi aplikasi Heroku

### **File Konfigurasi:**
- `.gitignore` - File yang diabaikan Git
- `.env.example` - Template environment variables
- `deploy.sh` - Script deploy otomatis ke Heroku

### **File Dokumentasi:**
- `README.md` - Panduan lengkap (file ini)
- `CONTRIBUTING.md` - Panduan berkontribusi
- `LICENSE` - Lisensi MIT

### **File Data:**
- `bot_database.json` - **File paling penting!** Semua data user, admin, dan pengaturan disimpan di sini. **Backup file ini secara berkala!**

## 🆘 Troubleshooting

### **Error Umum:**
- **NetworkError**: Masalah koneksi internet atau token bot tidak valid
- **Chat not found**: Bot belum ditambahkan ke grup atau tidak memiliki izin
- **Bot tidak merespon**: Cek terminal untuk error dan pastikan token benar
- **Command admin tidak bisa diakses**: Pastikan User ID Anda terdaftar sebagai admin

### **Masalah Heroku:**
- **App crash**: Cek logs dengan `heroku logs --tail --app nama-app`
- **Worker tidak berjalan**: Jalankan `heroku ps:scale worker=1 --app nama-app`
- **Environment variable**: Pastikan TOKEN sudah di-set dengan benar

### **Tips Debug:**
```bash
# Cek logs Heroku
heroku logs --tail --app nama-app-anda

# Restart aplikasi
heroku restart --app nama-app-anda

# Cek status aplikasi
heroku ps --app nama-app-anda
```

## 🔧 Environment Variables

Untuk production, set environment variables berikut:

```bash
# Wajib
TOKEN=your_telegram_bot_token_here

# Opsional
ADMIN_IDS=123456789,987654321
DB_FILE=bot_database.json
```

## 📊 Monitoring & Maintenance

### **Logs & Monitoring:**
- Semua aktivitas user otomatis dicatat
- Gunakan `/sangmata` untuk mencari user by username
- Export data ke CSV untuk analisis lebih lanjut

### **Backup Routine:**
- Backup `bot_database.json` secara berkala
- Gunakan fitur backup built-in di menu settings
- Simpan backup di tempat yang aman

### **Performance:**
- Bot menggunakan async/await untuk performa optimal
- Job queue untuk auto broadcast yang efisien
- Anti-spam system untuk mencegah abuse

## 🤝 Kontribusi

Kami sangat terbuka untuk kontribusi! Lihat [CONTRIBUTING.md](CONTRIBUTING.md) untuk panduan berkontribusi.

### **Cara Berkontribusi:**
1. Fork repository ini
2. Buat branch baru (`git checkout -b feature/nama-fitur`)
3. Commit perubahan (`git commit -m 'feat: tambah fitur baru'`)
4. Push ke branch (`git push origin feature/nama-fitur`)
5. Buat Pull Request

## 📄 Lisensi

Proyek ini menggunakan lisensi MIT - lihat file [LICENSE](LICENSE) untuk detail lebih lanjut.

## 🆘 Dukungan

Jika Anda mengalami masalah atau memiliki pertanyaan:

- **GitHub Issues**: Buat issue di repository ini
- **Telegram**: Hubungi maintainer
- **Email**: Via GitHub profile

## 🎯 Roadmap

### **Fitur Mendatang:**
- [ ] Web dashboard untuk management
- [ ] Multi-language support
- [ ] Advanced analytics
- [ ] Plugin system
- [ ] API endpoints
- [ ] Mobile app companion

### **Improvements:**
- [ ] Performance optimization
- [ ] Better error handling
- [ ] More customization options
- [ ] Integration dengan platform lain

---

## 📞 Kontak

**Developer**: Kilo Code
**GitHub**: [yourusername](https://github.com/yourusername)
**Telegram**: [@yourusername]

---

**⭐ Jika proyek ini bermanfaat, jangan lupa untuk memberikan star!**

Dibuat dengan ❤️ oleh **Kilo Code**.