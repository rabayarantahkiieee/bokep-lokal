#!/bin/bash

# Script Deploy Info Freebet Gacor Bot ke Heroku
# Dibuat oleh Kilo Code

echo "🚀 Memulai proses deploy ke Heroku..."

# Cek apakah Heroku CLI terinstall
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI tidak terinstall!"
    echo "📥 Silakan install Heroku CLI terlebih dahulu:"
    echo "   https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# Cek apakah user sudah login ke Heroku
if ! heroku auth:whoami &> /dev/null; then
    echo "❌ Anda belum login ke Heroku CLI!"
    echo "🔐 Silakan login terlebih dahulu:"
    echo "   heroku login"
    exit 1
fi

# Input nama aplikasi Heroku
read -p "📝 Masukkan nama aplikasi Heroku (contoh: info-freebet-bot): " APP_NAME

if [ -z "$APP_NAME" ]; then
    echo "❌ Nama aplikasi tidak boleh kosong!"
    exit 1
fi

# Cek apakah aplikasi sudah ada
if heroku apps:info "$APP_NAME" &> /dev/null; then
    echo "⚠️  Aplikasi '$APP_NAME' sudah ada!"
    read -p "   Apakah Anda ingin menggunakan aplikasi yang sudah ada? (y/n): " USE_EXISTING

    if [[ ! "$USE_EXISTING" =~ ^[Yy]$ ]]; then
        echo "❌ Deploy dibatalkan."
        exit 1
    fi
else
    echo "📦 Membuat aplikasi Heroku baru: $APP_NAME"
    heroku create "$APP_NAME"

    if [ $? -ne 0 ]; then
        echo "❌ Gagal membuat aplikasi Heroku!"
        exit 1
    fi
fi

# Set environment variable untuk TOKEN
read -p "🔑 Masukkan Telegram Bot Token Anda: " BOT_TOKEN

if [ -z "$BOT_TOKEN" ]; then
    echo "❌ Bot Token tidak boleh kosong!"
    exit 1
fi

echo "⚙️  Mengatur environment variables..."
heroku config:set TOKEN="$BOT_TOKEN" --app "$APP_NAME"

# Deploy aplikasi
echo "🚀 Deploy aplikasi ke Heroku..."
git add .
git commit -m "Deploy to Heroku"
git push heroku main

if [ $? -eq 0 ]; then
    echo "✅ Deploy berhasil!"
    echo ""
    echo "🌐 URL Aplikasi: https://$APP_NAME.herokuapp.com"
    echo "🤖 Bot Telegram Anda sudah berjalan di Heroku!"
    echo ""
    echo "📊 Untuk melihat logs:"
    echo "   heroku logs --tail --app $APP_NAME"
    echo ""
    echo "🛑 Untuk menghentikan aplikasi:"
    echo "   heroku ps:scale worker=0 --app $APP_NAME"
    echo ""
    echo "▶️  Untuk menjalankan kembali:"
    echo "   heroku ps:scale worker=1 --app $APP_NAME"
else
    echo "❌ Deploy gagal!"
    echo "🔍 Cek logs untuk detail error:"
    echo "   heroku logs --app $APP_NAME"
    exit 1
fi