# 🤖 BOT BOKEP LOKAL - V3 (Multifungsi & Stabil)

[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/rabayarantahkiieee/bokep-lokal)

Selamat datang di versi terbaru Bot Bokep Lokal! Bot ini dirancang ulang dari awal untuk menjadi lebih stabil, multifungsi, dan mudah digunakan.

## ✨ Fitur Unggulan

### 🎯 **Fitur Utama**
- **Menu Interaktif Berbasis Tombol**: Pengaturan mudah melalui inline keyboard
- **Welcome Message Kustom**: Atur teks, tombol, dan gambar untuk pesan selamat datang
- **Auto Broadcast**: Kirim pesan berulang secara otomatis ke semua pengguna
- **Manajemen Admin**: Tambah dan hapus admin dengan mudah
- **Database JSON/PostgreSQL**: Semua data (user, settings) disimpan dalam file JSON atau PostgreSQL untuk Heroku

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
   - Masuk ke folder `bokep-lokal` ini melalui terminal atau command prompt.

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

#### **🚀 Create a New App (REKOMENDASI UNTUK BOT)**

##### **⚠️ PENTING: Konfigurasi Database untuk Heroku**

**Bot ini menggunakan file JSON sebagai database. Untuk Heroku, ada beberapa opsi:**

###### **Opsi A: Heroku Postgres (REKOMENDASI - STABIL)**
1. **Install Heroku Postgres Addon:**
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev --app nama-app-anda
   ```

2. **Dapatkan DATABASE_URL:**
   ```bash
   heroku config:get DATABASE_URL --app nama-app-anda
   ```

3. **Set Environment Variable:**
   ```bash
   heroku config:set USE_POSTGRES=true --app nama-app-anda
   heroku config:set DATABASE_URL=your_database_url_here --app nama-app-anda
   ```

###### **Opsi B: Persistent File Storage (GRATIS - DATA BISA HILANG)**
- Bot akan menggunakan file JSON yang disimpan di `/tmp/`
- **Data akan hilang saat restart dyno**
- Cocok untuk testing atau data sementara
- Set environment variable: `USE_POSTGRES=false`

**💡 Rekomendasi: Gunakan Heroku Postgres untuk data yang stabil!**

1. Klik tombol "Deploy to Heroku" di atas
2. **Pilih "Create new app"** (bukan pipeline)
3. Masukkan nama aplikasi Heroku Anda (contoh: `bokep-lokal-bot`)
4. Masukkan Telegram Bot Token Anda di kolom `TOKEN`
5. **Tambahkan database jika perlu** (Postgres recommended)
6. Klik "Deploy app"
7. Tunggu proses deploy selesai (5-10 menit)
8. Bot akan otomatis berjalan 24/7

#### **🔧 New Pipeline (UNTUK PROJECT KOMPLEKS)**
- Pilih ini jika Anda punya staging dan production environment
- Lebih kompleks untuk setup
- Cocok untuk tim development besar
- **TIDAK direkomendasikan** untuk bot sederhana

**💡 Rekomendasi: Gunakan "Create new app" untuk kemudahan dan kecepatan!**

#### **Deploy Manual**
1. **Install Heroku CLI**
   ```bash
   # Download dari: https://devcenter.heroku.com/articles/heroku-cli
   heroku login
   ```

2. **Clone & Setup**
   ```bash
   git clone https://github.com/rabayarantahkiieee/bokep-lokal.git
   cd bokep-lokal
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

## 🔧 Environment Variables & Setup Bot

### **1. Setting Environment Variables di Heroku**

#### **Via Heroku Dashboard:**
1. **Masuk ke Heroku Dashboard** → Pilih aplikasi Anda
2. **Klik tab "Settings"**
3. **Klik "Reveal Config Vars"**
4. **Tambahkan variables berikut:**

| Key | Value | Keterangan |
|-----|-------|------------|
| `TOKEN` | `8067260760:AAF9qWxEtNBFe-b8afJHmVp8tMD9JlkE4LI` | **WAJIB** - Token bot Telegram |
| `ADMIN_IDS` | `6592870669` | **Opsional** - ID admin (pisah dengan koma) |
| `DB_FILE` | `bot_database.json` | **Opsional** - Nama file database |

#### **Via Heroku CLI:**
```bash
# Set TOKEN (WAJIB)
heroku config:set TOKEN=your_telegram_bot_token_here --app nama-app-anda

# Set ADMIN_IDS (Opsional)
heroku config:set ADMIN_IDS=123456789,987654321 --app nama-app-anda

# Cek semua config vars
heroku config --app nama-app-anda
```

### **2. Menjalankan Bot Setelah Deploy**

#### **Cek Status Bot:**
```bash
# Cek apakah worker sedang berjalan
heroku ps --app nama-app-anda

# Jika tidak berjalan, start worker
heroku ps:scale worker=1 --app nama-app-anda

# Restart aplikasi
heroku restart --app nama-app-anda
```

#### **Monitoring Bot:**
```bash
# Lihat logs real-time
heroku logs --tail --app nama-app-anda

# Lihat logs terbaru (100 baris)
heroku logs -n 100 --app nama-app-anda

# Cek status aplikasi
heroku apps:info --app nama-app-anda
```

### **3. Testing Bot Setelah Deploy**

1. **Buka Telegram** dan cari bot Anda
2. **Kirim `/start`** untuk test welcome message
3. **Kirim `/help`** untuk lihat semua command
4. **Kirim `/settings`** untuk akses menu admin (jika Anda admin)

### **4. Troubleshooting Jika Bot Tidak Berjalan**

#### **Bot Tidak Merespon:**
```bash
# Cek logs untuk error
heroku logs --tail --app nama-app-anda

# Restart worker
heroku ps:scale worker=0 --app nama-app-anda
heroku ps:scale worker=1 --app nama-app-anda
```

#### **Error TOKEN:**
```bash
# Pastikan TOKEN sudah benar
heroku config:get TOKEN --app nama-app-anda

# Update TOKEN jika salah
heroku config:set TOKEN=token_baru_anda --app nama-app-anda
```

#### **Database Error:**
```bash
# Cek apakah file database ada
heroku run bash --app nama-app-anda
ls -la bot_database.json
exit
```

### **5. Update Bot (Jika Ada Perubahan Kode)**

#### **Via Git:**
```bash
# Commit perubahan
git add .
git commit -m "Update bot features"

# Push ke Heroku
git push heroku main

# Bot akan otomatis restart
```

#### **Via Heroku Dashboard:**
1. **Masuk Heroku Dashboard** → Pilih aplikasi
2. **Klik tab "Deploy"**
3. **Connect ke GitHub repository**
4. **Enable Automatic Deploys** (opsional)
5. **Klik "Deploy Branch"**

### **6. Backup & Restore Data**

#### **Download Database:**
```bash
# Via Heroku CLI
heroku run bash --app nama-app-anda
cp bot_database.json /tmp/
exit

# Download file
heroku ps:copy /tmp/bot_database.json --app nama-app-anda
```

#### **Upload Database Baru:**
```bash
# Via Heroku Dashboard
# 1. Masuk aplikasi → Resources
# 2. Klik "More" → "Run console"
# 3. Upload file database via browser
```

### **7. Monitoring & Maintenance**

#### **Daily Checks:**
```bash
# Cek uptime
heroku apps:info --app nama-app-anda | grep "Created"

# Cek dyno usage
heroku ps --app nama-app-anda

# Backup database mingguan
heroku run "cp bot_database.json backup_$(date +%Y%m%d).json" --app nama-app-anda
```

#### **Performance Monitoring:**
- **Response Time**: Bot harus merespon dalam 1-2 detik
- **Memory Usage**: Monitor RAM usage di Heroku dashboard
- **Error Rate**: Cek logs untuk error yang berulang

### **8. Cost Management**

#### **Free Tier Limits:**
- **550 jam/bulan** untuk hobby dyno
- **Reset setiap bulan** pada tanggal 1
- **Sleep setelah 30 menit** tidak aktif

#### **Upgrade ke Paid (Jika Perlu):**
```bash
# Upgrade ke hobby dyno (7$/bulan)
heroku ps:resize worker=hobby --app nama-app-anda

# Cek cost saat ini
heroku apps:info --app nama-app-anda | grep "Dyno"
```

### **9. Emergency Stop & Start**

```bash
# Stop bot sementara
heroku ps:scale worker=0 --app nama-app-anda

# Start bot kembali
heroku ps:scale worker=1 --app nama-app-anda

# Force restart
heroku restart --app nama-app-anda
```

### **10. Logs Analysis**

#### **Cek Error Logs:**
```bash
# Filter hanya error
heroku logs --app nama-app-anda | grep "ERROR"

# Cek aktivitas bot
heroku logs --app nama-app-anda | grep "Bot started\|Broadcast\|Welcome"
```

#### **Monitor User Activity:**
```bash
# Cek jumlah user yang aktif
heroku run "python -c \"import json; db=json.load(open('bot_database.json')); print(f'Users: {len(db.get(\"users\", []))}')\"" --app nama-app-anda
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