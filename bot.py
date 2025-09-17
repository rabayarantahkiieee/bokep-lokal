#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
BOT INFO FREEBET GACOR - V3 (Multifungsi & Stabil)
Dibuat oleh Kilo Code

Fitur Utama:
- Menu Interaktif Berbasis Tombol
- Pesan Welcome & Tombol yang Bisa Diatur
- Auto Broadcast Pesan Berulang
- Manajemen Admin & User
- Fitur Lengkap (Broadcast, Stats, Info, dll.)
"""

import os
import json
import asyncio
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from telegram.constants import ParseMode
from telegram.error import TelegramError

# --- KONFIGURASI UTAMA ---
TOKEN = "8067260760:AAF9qWxEtNBFe-b8afJHmVp8tMD9JlkE4LI"
ADMIN_IDS = [6592870669]  # Admin utama, bisa ditambah via command

# --- NAMA FILE UNTUK MENYIMPAN DATA ---
DB_FILE = "bot_database.json"

# --- STRUKTUR DATABASE DEFAULT ---
DEFAULT_DB = {
    "users": [],
    "admins": ADMIN_IDS,
    "welcome_message": {
        "text": "SELAMAT DATANG DI SITUS\nPAIZA99 SITUS ONLINE\nTERPERCAYA NO 1 DI INDONESIA\n\nCARI DI GOGLE \"PAIZA99\"\n\n❏ SITUS DENGAN BONUS TANPA BATAS\n❏ AUTO TURUN SCATTER\n❏ SCATER HITAM\n❏ PERKALIAN 1000\n\nLINK DAFTAR\nhttps://tautin.app/L2wKBu0Pdi\nhttps://tautin.app/L2wKBu0Pdi\nhttps://tautin.app/L2wKBu0Pdi\n\n🏴 JIKA BOT EROR LAPORAN KE\n@sssalwaww\n\n═══════════════════\n●Nama : {NAME}\n●Username : {USERNAME}\n●ID : {ID}\n●Tanggal : {DATE}\n═══════════════════",
        "buttons": [
            {"text": "Join Sini Kak", "url": "https://t.me/c/3004478026"},
            {"text": "Join Sini Kak", "url": "https://t.me/c/3004478026"}
        ],
        "photo": None
    },
    "broadcast_message": {
        "text": "Ini adalah pesan broadcast. Atur pesan ini di menu settings.",
        "photo": None,
        "buttons": []
    },
    "auto_broadcast": {
        "enabled": False,
        "message": {
            "text": "Ini adalah pesan auto broadcast. Atur pesan ini di menu settings.",
            "photo": None,
            "buttons": []
        },
        "interval_minutes": 60,
        "last_sent": None
    },
    "bot_info": {
        "start_time": datetime.now().isoformat()
    },
    "custom_commands": {},
    "anti_spam": {
        "enabled": False,
        "max_messages_per_minute": 5,
        "warning_message": "⚠️ Terdeteksi spam! Harap kurangi frekuensi pengiriman pesan.",
        "mute_duration_minutes": 10,
        "banned_words": []
    },
    "user_logs": [],
    "navigation_history": {},
    "group_welcome": {
        "enabled": False,
        "text": "Selamat datang di group! Silakan baca rules group.",
        "photo": None,
        "buttons": []
    },
    "scheduled_messages": []
}

# --- FUNGSI DATABASE (LOAD & SAVE) ---
def load_db():
    """Memuat database dari file JSON."""
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return DEFAULT_DB

def save_db(db):
    """Menyimpan database ke file JSON."""
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(db, f, indent=4)

# --- FUNGSI HELPER ---
def is_admin(user_id: int) -> bool:
    """Mengecek apakah user adalah admin."""
    db = load_db()
    return user_id in db.get("admins", [])

def is_main_admin(user_id: int) -> bool:
    """Mengecek apakah user adalah admin utama."""
    return user_id in ADMIN_IDS

def is_main_admin(user_id: int) -> bool:
    """Mengecek apakah user adalah admin utama."""
    return user_id == ADMIN_IDS[0]  # Admin utama adalah yang pertama dalam list

def replace_placeholders(text: str, user) -> str:
    """Mengganti placeholder dalam teks dengan data user."""
    if not text:
        return text

    from datetime import datetime
    now = datetime.now()

    replacements = {
        "{NAME}": user.first_name or "User",
        "{USERNAME}": f"@{user.username}" if user.username else "No Username",
        "{ID}": str(user.id),
        "{DATE}": now.strftime("%d/%m/%Y"),
        "{TIME}": now.strftime("%H:%M:%S"),
        "{FULLDATE}": now.strftime("%d/%m/%Y %H:%M:%S"),
        "{DAY}": now.strftime("%A"),
        "{MONTH}": now.strftime("%B"),
        "{YEAR}": str(now.year),
    }

    for placeholder, value in replacements.items():
        text = text.replace(placeholder, value)

    return text

def log_user_activity(user, action: str, details: str = ""):
    """Mencatat aktivitas user ke dalam log."""
    from datetime import datetime

    db = load_db()
    if "user_logs" not in db:
        db["user_logs"] = []

    # Cek dan simpan perubahan username
    if user.username:
        if "username_history" not in db:
            db["username_history"] = {}

        user_key = str(user.id)
        if user_key not in db["username_history"]:
            db["username_history"][user_key] = []

        # Cek apakah username berubah
        existing_usernames = [entry['username'] for entry in db["username_history"][user_key]]
        if user.username not in existing_usernames:
            db["username_history"][user_key].append({
                "username": user.username,
                "timestamp": datetime.now().isoformat(),
                "action": action
            })

            # Simpan maksimal 10 history per user
            if len(db["username_history"][user_key]) > 10:
                db["username_history"][user_key] = db["username_history"][user_key][-10:]

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "user_id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "action": action,
        "details": details
    }

    # Simpan maksimal 1000 log terakhir
    db["user_logs"].append(log_entry)
    if len(db["user_logs"]) > 1000:
        db["user_logs"] = db["user_logs"][-1000:]

    save_db(db)

def update_navigation_history(user_id: int, menu_path: str):
    """Update riwayat navigasi user untuk breadcrumb."""
    db = load_db()
    if "navigation_history" not in db:
        db["navigation_history"] = {}

    db["navigation_history"][str(user_id)] = menu_path
    save_db(db)

def get_navigation_history(user_id: int) -> str:
    """Mendapatkan menu terakhir yang diakses user."""
    db = load_db()
    return db.get("navigation_history", {}).get(str(user_id), "main_menu")

async def quick_broadcast_task(context, message_config, users, admin_id):
    """Task untuk quick broadcast."""
    sent_count = 0
    failed_count = 0

    for user_id in users:
        try:
            # Coba dapatkan info user untuk placeholder
            try:
                user = await context.bot.get_chat(user_id)
                class SimpleUser:
                    def __init__(self, chat):
                        self.id = chat.id
                        self.first_name = chat.first_name or chat.title or "User"
                        self.username = chat.username

                simple_user = SimpleUser(user)
                await send_complex_message(context, user_id, message_config, simple_user)
            except:
                await send_complex_message(context, user_id, message_config)

            sent_count += 1
        except Exception as e:
            failed_count += 1
            print(f"Gagal kirim quick broadcast ke {user_id}: {e}")
        await asyncio.sleep(1.5)

    # Kirim laporan ke admin
    try:
        result_text = f"""
📢 *QUICK BROADCAST SELESAI*

✅ Terkirim: `{sent_count}`
❌ Gagal: `{failed_count}`
👥 Total User: `{len(users)}`
        """
        await context.bot.send_message(chat_id=admin_id, text=result_text.strip(), parse_mode=ParseMode.MARKDOWN)
    except:
        pass

async def send_random_reaction(context: ContextTypes.DEFAULT_TYPE, chat_id: int, message_id: int):
    """Mengirim reaction emoticon random ke pesan dengan animasi keren."""
    import random

    # Daftar reaction emoticon yang menarik dengan animasi
    reactions = [
        "🎉", "🎊", "🎈", "🎆", "🎇", "✨", "⭐", "🌟", "💫", "🎯",
        "🎪", "🎨", "🎭", "🔥", "💥", "⚡", "🌈", "🎀", "🎁", "🎂",
        "🍾", "🚀", "💎", "👑", "🏆", "🎖️", "🏅", "🥇", "🥈", "🥉",
        "💯", "🌟", "⭐", "✨", "🎯", "🎪", "🎨", "🎭", "🔥", "💥"
    ]

    # Pilih 3 reaction random untuk efek berurutan
    selected_reactions = random.sample(reactions, 3)

    try:
        # Kirim reaction pertama dengan efek besar
        await context.bot.set_message_reaction(
            chat_id=chat_id,
            message_id=message_id,
            reaction=[{"type": "emoji", "emoji": selected_reactions[0]}],
            is_big=True
        )

        # Tunggu sebentar lalu tambahkan reaction kedua
        await asyncio.sleep(0.5)
        await context.bot.set_message_reaction(
            chat_id=chat_id,
            message_id=message_id,
            reaction=[
                {"type": "emoji", "emoji": selected_reactions[0]},
                {"type": "emoji", "emoji": selected_reactions[1]}
            ],
            is_big=False
        )

        # Tunggu sebentar lalu tambahkan reaction ketiga
        await asyncio.sleep(0.5)
        await context.bot.set_message_reaction(
            chat_id=chat_id,
            message_id=message_id,
            reaction=[
                {"type": "emoji", "emoji": selected_reactions[0]},
                {"type": "emoji", "emoji": selected_reactions[1]},
                {"type": "emoji", "emoji": selected_reactions[2]}
            ],
            is_big=True
        )

    except Exception as e:
        print(f"Gagal mengirim reaction animasi: {e}")
        # Fallback: kirim reaction single jika animasi gagal
        try:
            reaction = random.choice(reactions)
            await context.bot.set_message_reaction(
                chat_id=chat_id,
                message_id=message_id,
                reaction=[{"type": "emoji", "emoji": reaction}],
                is_big=True
            )
        except Exception as e2:
            print(f"Gagal mengirim reaction single: {e2}")
            # Jika reaction gagal, tidak perlu kirim pesan fallback
            pass

# --- AUTO BROADCAST ---
async def send_complex_message(context: ContextTypes.DEFAULT_TYPE, user_id: int, message_config: dict, user=None):
    """Fungsi helper untuk mengirim pesan (teks/foto/tombol)."""
    text = message_config.get("text", "")
    photo = message_config.get("photo")
    buttons = message_config.get("buttons", [])

    # Ganti placeholder jika user disediakan
    if user:
        text = replace_placeholders(text, user)

    keyboard = []
    row = []
    for btn in buttons:
        row.append(InlineKeyboardButton(btn["text"], url=btn["url"]))
        if len(row) >= 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None

    if photo:
        await context.bot.send_photo(chat_id=user_id, photo=photo, caption=text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    elif text:
        await context.bot.send_message(chat_id=user_id, text=text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)


async def auto_broadcast_task(context: ContextTypes.DEFAULT_TYPE):
    """Tugas yang berjalan di background untuk auto broadcast."""
    try:
        db = load_db()
        autobc_config = db.get("auto_broadcast", {})
        if not autobc_config.get("enabled"):
            print("Auto broadcast dinonaktifkan, melewati tugas.")
            return

        message_config = autobc_config.get("message", {})
        users = db.get("users", [])
        if not users:
            print("Tidak ada user terdaftar untuk auto broadcast.")
            return

        if not (message_config.get("text") or message_config.get("photo")):
            print("Pesan auto broadcast belum diatur, melewati tugas.")
            return

        print(f"Memulai auto broadcast ke {len(users)} user...")

        sent_count = 0
        failed_count = 0
        for user_id in users:
            try:
                # Coba dapatkan info user untuk placeholder
                try:
                    user = await context.bot.get_chat(user_id)
                    # Buat user object sederhana
                    class SimpleUser:
                        def __init__(self, chat):
                            self.id = chat.id
                            self.first_name = chat.first_name or chat.title or "User"
                            self.username = chat.username
    
                    simple_user = SimpleUser(user)
                    await send_complex_message(context, user_id, message_config, simple_user)
                except:
                    # Jika gagal dapatkan info user, kirim tanpa placeholder
                    await send_complex_message(context, user_id, message_config)
    
                sent_count += 1
                print(f"Berhasil kirim ke {user_id}")
            except TelegramError as e:
                failed_count += 1
                print(f"Gagal mengirim auto broadcast ke {user_id}: {e}")
            except Exception as e:
                failed_count += 1
                print(f"Error tak terduga saat mengirim ke {user_id}: {e}")
            await asyncio.sleep(1) # Jeda aman 1 detik per pesan

        print(f"Auto Broadcast Selesai: {sent_count} terkirim, {failed_count} gagal.")
        db["auto_broadcast"]["last_sent"] = datetime.now().isoformat()
        save_db(db)

    except Exception as e:
        print(f"Error dalam auto_broadcast_task: {e}")


# --- HANDLER COMMAND ---
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menangani command /start."""
    user = update.effective_user
    db = load_db()

    # Log aktivitas user
    log_user_activity(user, "start_command", "User menggunakan /start")

    # Daftarkan user baru jika belum ada
    if user.id not in db["users"]:
        db["users"].append(user.id)
        save_db(db)
        log_user_activity(user, "new_user", "User baru terdaftar")

    # Kirim pesan welcome
    welcome_config = db.get("welcome_message", {})
    text = welcome_config.get("text", "Selamat datang!")
    buttons = welcome_config.get("buttons", [])
    photo = welcome_config.get("photo")

    # Buat inline keyboard
    keyboard = []
    row = []
    for btn in buttons:
        row.append(InlineKeyboardButton(btn["text"], url=btn["url"]))
        if len(row) == 2: # Maksimal 2 tombol per baris
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
        
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Kirim welcome message
    sent_message = None
    if photo:
        sent_message = await update.message.reply_photo(photo=photo, caption=replace_placeholders(text, user), reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    else:
        sent_message = await update.message.reply_text(replace_placeholders(text, user), reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

    # Kirim reaction animasi random ke pesan welcome yang baru dikirim
    if sent_message:
        await send_random_reaction(context, sent_message.chat_id, sent_message.message_id)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menampilkan daftar command."""
    commands = await context.bot.get_my_commands()
    help_text = "Berikut adalah daftar command yang tersedia:\n\n"
    for cmd in commands:
        help_text += f"/{cmd.command} - {cmd.description}\n"

    await update.message.reply_text(help_text)

async def guide_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menampilkan guide placeholder untuk pesan."""
    guide_text = """
📚 *GUIDE PLACEHOLDER PESAN*

Placeholder berikut bisa digunakan di semua pesan (Welcome, Broadcast, Auto Broadcast):

👤 *User Info:*
• `{NAME}` - Nama depan user
• `{USERNAME}` - Username dengan @
• `{ID}` - ID Telegram user

📅 *Tanggal & Waktu:*
• `{DATE}` - Tanggal (DD/MM/YYYY)
• `{TIME}` - Waktu (HH:MM:SS)
• `{FULLDATE}` - Tanggal & waktu lengkap
• `{DAY}` - Hari (Monday, Tuesday, dll.)
• `{MONTH}` - Bulan (January, February, dll.)
• `{YEAR}` - Tahun

💡 *Contoh Penggunaan:*
```
SELAMAT DATANG {NAME}!
Username: {USERNAME}
ID: {ID}
Tanggal: {DATE}
```

✅ Placeholder akan otomatis diganti dengan data user saat pesan dikirim!
    """
    await update.message.reply_text(guide_text, parse_mode=ParseMode.MARKDOWN)

async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mengirim pesan broadcast ke semua user."""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Anda tidak punya izin untuk command ini.")
        return

    # Pesan diambil dari database, bukan argumen
    db = load_db()
    message_config = db.get("broadcast_message", {})
    users = db.get("users", [])

    if not users:
        await update.message.reply_text("Belum ada user yang terdaftar.")
        return
    
    if not (message_config.get("text") or message_config.get("photo")):
        await update.message.reply_text("Pesan broadcast belum diatur. Silakan atur melalui menu /settings.")
        return

    sent_count = 0
    failed_count = 0
    status_msg = await update.message.reply_text(f"📢 Memulai broadcast ke {len(users)} user...")

    for user_id in users:
        try:
            # Coba dapatkan info user untuk placeholder
            try:
                user = await context.bot.get_chat(user_id)
                # Buat user object sederhana
                class SimpleUser:
                    def __init__(self, chat):
                        self.id = chat.id
                        self.first_name = chat.first_name or chat.title or "User"
                        self.username = chat.username

                simple_user = SimpleUser(user)
                await send_complex_message(context, user_id, message_config, simple_user)
            except:
                # Jika gagal dapatkan info user, kirim tanpa placeholder
                await send_complex_message(context, user_id, message_config)

            sent_count += 1
        except TelegramError as e:
            failed_count += 1
            print(f"Gagal mengirim broadcast ke {user_id}: {e}")
        await asyncio.sleep(1.5) # Jeda aman 1.5 detik

    await status_msg.edit_text(f"Broadcast Selesai!\n✅ Terkirim: {sent_count}\n❌ Gagal: {failed_count}")


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menampilkan statistik bot."""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Anda tidak punya izin untuk command ini.")
        return
        
    db = load_db()
    start_time = datetime.fromisoformat(db.get("bot_info", {}).get("start_time"))
    uptime = datetime.now() - start_time

    stats_text = f"""
📊 **STATISTIK BOT**

- 👥 Total Pengguna: `{len(db.get('users', []))}`
- 👑 Total Admin: `{len(db.get('admins', []))}`
- ⚙️ Auto Broadcast: `{'Aktif' if db.get('auto_broadcast', {}).get('enabled') else 'Mati'}`
- ⏰ Uptime: `{str(uptime).split('.')[0]}`
    """
    await update.message.reply_text(stats_text, parse_mode=ParseMode.MARKDOWN)


async def getid_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mengirim informasi ID user, chat, dan group."""
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    id_text = f"""
🆔 *INFORMASI ID*

- *User ID Anda*: `{user_id}`
- *Chat ID Saat Ini*: `{chat_id}`
    """

    # Jika ada pesan yang di-reply, ambil ID pengirimnya
    if update.message.reply_to_message:
        replied_user = update.message.reply_to_message.from_user
        id_text += f"\n- *User ID (dari Reply)*: `{replied_user.id}`"

    await update.message.reply_text(id_text, parse_mode=ParseMode.MARKDOWN)

async def listusers_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menampilkan daftar semua user yang terdaftar (Admin only)."""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Anda tidak punya izin untuk command ini.")
        return

    db = load_db()
    users = db.get("users", [])

    if not users:
        await update.message.reply_text("Belum ada user yang terdaftar.")
        return

    user_list = "\n".join([f"- `{user_id}`" for user_id in users])
    await update.message.reply_text(f"👥 *DAFTAR USER TERDAFTAR*\n\n{user_list}\n\nTotal: {len(users)} user", parse_mode=ParseMode.MARKDOWN)

async def sangmata_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fitur Sang Mata - Cari user by username untuk semua user."""
    user = update.effective_user
    log_user_activity(user, "sangmata_command", "Menggunakan fitur Sang Mata")

    # Cek apakah ada forward message
    if update.message.forward_from or update.message.forward_from_chat:
        await handle_forward_message(update, context)
        return

    # Jika tidak ada forward, minta username
    await update.message.reply_text(
        "👁️ *SANG MATA - PENCARI USER*\n\n"
        "Kirim username yang ingin dicari (tanpa @):\n\n"
        "Contoh: `john_doe`\n\n"
        "💡 *Tips:* Forward pesan dari user untuk deteksi otomatis!",
        parse_mode=ParseMode.MARKDOWN
    )

    # Set state untuk menunggu input username
    context.user_data['state'] = "awaiting_sangmata_search"

async def handle_forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menangani forward message untuk deteksi user."""
    user = update.effective_user
    log_user_activity(user, "forward_message_detection", "Deteksi user via forward message")

    forward_from = update.message.forward_from
    forward_from_chat = update.message.forward_from_chat

    if forward_from:
        # Forward dari user
        user_id = forward_from.id
        username = forward_from.username
        first_name = forward_from.first_name

        # Cari di database logs
        db = load_db()
        user_logs = db.get("user_logs", [])

        # Cari semua aktivitas user ini
        user_activities = [
            log for log in user_logs
            if log.get('user_id') == user_id
        ]

        # Cari history username changes dari database
        username_history = db.get("username_history", {}).get(str(user_id), [])

        # Buat response
        response = f"👁️ *SANG MATA - DETEKSI USER*\n\n"
        response += f"🆔 *ID:* `{user_id}`\n"
        response += f"👤 *Nama:* {first_name}\n"
        response += f"📝 *Username Saat Ini:* @{username if username else 'Tidak ada'}\n\n"

        if user_activities:
            response += f"📊 *Total Aktivitas:* {len(user_activities)}\n"
            response += f"🕐 *Terakhir Aktif:* {datetime.fromisoformat(user_activities[-1]['timestamp']).strftime('%d/%m/%Y %H:%M')}\n\n"

            # Tampilkan 5 aktivitas terakhir
            response += "📋 *5 AKTIVITAS TERAKHIR:*\n"
            for i, log in enumerate(reversed(user_activities[-5:]), 1):
                timestamp = datetime.fromisoformat(log['timestamp']).strftime("%d/%m %H:%M")
                action = log.get('action', 'N/A')
                response += f"{i}. `{timestamp}` | {action}\n"
        else:
            response += "📊 *Status:* User belum pernah berinteraksi dengan bot\n"

        if username_history:
            response += f"\n🔄 *HISTORY USERNAME CHANGES:*\n"
            for i, change in enumerate(reversed(username_history[-5:]), 1):  # Tampilkan 5 terakhir
                timestamp = datetime.fromisoformat(change['timestamp']).strftime("%d/%m/%Y %H:%M")
                old_username = change['username']
                response += f"{i}. `{timestamp}` | @{old_username}\n"

        await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)

    elif forward_from_chat:
        # Forward dari channel/group
        chat_id = forward_from_chat.id
        chat_title = forward_from_chat.title
        chat_username = forward_from_chat.username
        chat_type = "Channel" if forward_from_chat.type == "channel" else "Group"

        response = f"👁️ *SANG MATA - DETEKSI CHAT*\n\n"
        response += f"🆔 *Chat ID:* `{chat_id}`\n"
        response += f"📌 *Tipe:* {chat_type}\n"
        response += f"📝 *Nama:* {chat_title}\n"
        if chat_username:
            response += f"🔗 *Username:* @{chat_username}\n"

        await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)

    else:
        await update.message.reply_text("❌ Tidak dapat mendeteksi user dari forward message.", parse_mode=ParseMode.MARKDOWN)

# --- FUNGSI SETTINGS (Menu Interaktif) ---
# --- FUNGSI SETTINGS & CALLBACK ---

async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menampilkan menu settings interaktif."""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Anda tidak punya izin untuk command ini.")
        return

    # Cek apakah ada riwayat navigasi
    last_menu = get_navigation_history(update.effective_user.id) if update.effective_user else "main_menu"

    keyboard = [
        [InlineKeyboardButton("📝 Welcome Msg", callback_data="menu_welcome")],
        [InlineKeyboardButton("📢 Manual Broadcast", callback_data="menu_broadcast")],
        [InlineKeyboardButton("🤖 Auto Broadcast", callback_data="menu_autobroadcast")],
        [InlineKeyboardButton("👑 Manajemen Admin", callback_data="menu_admin")],
        [InlineKeyboardButton("💾 Backup & Restore", callback_data="menu_backup")],
        [InlineKeyboardButton("⚡ Custom Commands", callback_data="menu_custom")],
        [InlineKeyboardButton("🛡️ Anti-Spam", callback_data="menu_antispam")],
        [InlineKeyboardButton("👁️ Sang Mata (Logs)", callback_data="menu_sangmata")],
        [InlineKeyboardButton("🚀 Fitur Canggih", callback_data="menu_advanced")],
        [InlineKeyboardButton("📊 Statistik Bot", callback_data="stats")],
    ]

    # Tambahkan tombol kembali ke terakhir jika bukan main_menu
    if last_menu != "main_menu":
        keyboard.append([InlineKeyboardButton("🔙 Kembali ke Terakhir", callback_data=f"back_to_last:{last_menu}")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Tambahkan timestamp untuk menghindari "Message is not modified"
    import time
    timestamp = str(int(time.time()))[-4:]  # 4 digit terakhir timestamp

    settings_text = f"⚙️ *MENU PENGATURAN*\n\nPilih kategori yang ingin Anda atur:\n\n📅 *Last Update: {timestamp}*"

    if update.callback_query:
        try:
            await update.callback_query.edit_message_text(settings_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
        except Exception as e:
            if "not modified" in str(e).lower():
                # Pesan sama, abaikan error
                pass
            else:
                # Error lain, lempar ulang
                raise e
    else:
        await update.message.reply_text(settings_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)


async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menangani semua interaksi dari Inline Keyboard."""
    query = update.callback_query

    # Handle callback query timeout gracefully
    try:
        await query.answer(cache_time=1) # Respon cepat
    except Exception as e:
        print(f"Callback query answer failed: {e}")
        # Continue processing even if answer fails

    callback_data = query.data
    db = load_db()
    
    # Navigasi Utama
    if callback_data == "main_menu":
        update_navigation_history(query.from_user.id, "main_menu")
        await settings_command(update, context)
        return

    if callback_data == "settings":
        update_navigation_history(query.from_user.id, "settings")
        await settings_command(update, context)
        return

    if callback_data.startswith("back_to_last:"):
        last_menu = callback_data.split(":", 1)[1]
        # Redirect ke menu terakhir
        if last_menu == "settings":
            await settings_command(update, context)
        elif last_menu == "menu_welcome":
            await callback_handler(update, context)  # Akan dihandle oleh menu_welcome
        # Tambahkan redirect untuk menu lainnya sesuai kebutuhan
        else:
            await settings_command(update, context)  # Fallback ke main menu
        return

    # --- Sub-menu Dinamis ---
    menus = {
        "welcome": ("📝 Welcome Message", db.get("welcome_message", {})),
        "broadcast": ("📢 Manual Broadcast", db.get("broadcast_message", {})),
        "autobroadcast_msg": ("🤖 Auto Broadcast Message", db.get("auto_broadcast", {}).get("message", {}))
    }

    # Penanganan untuk menu Welcome, Broadcast, AutoBroadcast Message
    for key, (title, config) in menus.items():
        if callback_data == f"menu_{key}":
            # Pastikan config adalah dict
            if isinstance(config, str) or config is None:
                config = {}
            photo_status = "✅ Ada" if config.get("photo") else "❌ Kosong"
            button_count = len(config.get("buttons", []))
            text = f"*{title}*\n\n- *Foto*: {photo_status}\n- *Tombol*: {button_count}\n\nPilih aksi:"
            keyboard = [
                [InlineKeyboardButton("👀 Preview", callback_data=f"preview_{key}")],
                [InlineKeyboardButton("Ubah Teks", callback_data=f"set_text_{key}")],
                [InlineKeyboardButton("Ubah Foto", callback_data=f"set_photo_{key}")],
                [InlineKeyboardButton("Tambah Tombol", callback_data=f"add_button_{key}")],
                [InlineKeyboardButton("Hapus Tombol", callback_data=f"clear_buttons_{key}")],
                [InlineKeyboardButton("⬅️ Kembali", callback_data="main_menu")]
            ]
            await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
            return
        elif callback_data == f"set_text_{key}":
            context.user_data['state'] = f"awaiting_text_{key}"
            await query.edit_message_text("✍️ Silakan kirim *teks baru*.", parse_mode=ParseMode.MARKDOWN)
            return
        elif callback_data == f"set_photo_{key}":
            context.user_data['state'] = f"awaiting_photo_{key}"
            await query.edit_message_text("🖼️ Silakan *kirim foto baru*.", parse_mode=ParseMode.MARKDOWN)
            return
        elif callback_data == f"add_button_{key}":
            context.user_data['state'] = f"awaiting_button_{key}"
            await query.edit_message_text("➕ Silakan kirim data tombol dengan format:\n`Nama Tombol | https://link.com`", parse_mode=ParseMode.MARKDOWN)
            return
        elif callback_data == f"clear_buttons_{key}":
            if key == "autobroadcast_msg":
                if "auto_broadcast" not in db:
                    db["auto_broadcast"] = DEFAULT_DB["auto_broadcast"]
                if "message" not in db["auto_broadcast"]:
                    db["auto_broadcast"]["message"] = DEFAULT_DB["auto_broadcast"]["message"]
                db["auto_broadcast"]["message"]["buttons"] = []
            else:
                message_key = f"{key}_message"
                if message_key not in db:
                    db[message_key] = DEFAULT_DB.get(message_key, {"text": "", "photo": None, "buttons": []})
                db[message_key]["buttons"] = []
            save_db(db)
            await query.edit_message_text("✅ Semua tombol telah dihapus.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Kembali", callback_data=f"menu_{key}")], [InlineKeyboardButton("🏠 Menu Utama", callback_data="main_menu")]]))
            return
        elif callback_data == f"preview_{key}":
            # Preview pesan
            if key == "autobroadcast_msg":
                message_config = db["auto_broadcast"]["message"]
            else:
                message_config = db[f"{key}_message"]

            text = message_config.get("text", "")
            photo = message_config.get("photo")
            buttons = message_config.get("buttons", [])

            # Ganti placeholder untuk preview menggunakan data admin
            admin_user = query.from_user
            text = replace_placeholders(text, admin_user)

            # Buat keyboard untuk preview
            keyboard = []
            row = []
            for btn in buttons:
                row.append(InlineKeyboardButton(btn["text"], url=btn["url"]))
                if len(row) >= 2:
                    keyboard.append(row)
                    row = []
            if row:
                keyboard.append(row)

            reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None

            # Kirim preview ke chat admin
            try:
                if photo:
                    await context.bot.send_photo(chat_id=query.from_user.id, photo=photo, caption=text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
                elif text:
                    await context.bot.send_message(chat_id=query.from_user.id, text=text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
                else:
                    await context.bot.send_message(chat_id=query.from_user.id, text="❌ Tidak ada konten untuk di-preview.")

                await query.edit_message_text("✅ Preview telah dikirim ke chat pribadi Anda.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Kembali", callback_data=f"menu_{key}")], [InlineKeyboardButton("🏠 Menu Utama", callback_data="main_menu")]]))
            except Exception as e:
                await query.edit_message_text(f"❌ Gagal mengirim preview: {str(e)}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Kembali", callback_data=f"menu_{key}")]]))
            return

    # Menu Auto Broadcast (Settings)
    if callback_data == "menu_autobroadcast":
        autobc_config = db.get("auto_broadcast", {})
        status = "🟢 AKTIF" if autobc_config.get("enabled") else "🔴 MATI"
        interval = autobc_config.get("interval_minutes", 60)

        keyboard = [
            [InlineKeyboardButton(f"Status: {status}", callback_data="autobc_toggle")],
            [InlineKeyboardButton("Ubah Pesan", callback_data="menu_autobroadcast_msg")],
            [InlineKeyboardButton(f"Interval: {interval} menit", callback_data="autobc_set_interval")],
            [InlineKeyboardButton("🏠 Menu Utama", callback_data="main_menu")],
            [InlineKeyboardButton("⬅️ Kembali ke Settings", callback_data="settings")]
        ]
        await query.edit_message_text("🤖 *PENGATURAN AUTO BROADCAST*\n\nKelola pengaturan auto broadcast pesan.", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
        return
        
    elif callback_data == "autobc_toggle":
        db["auto_broadcast"]["enabled"] = not db["auto_broadcast"].get("enabled", False)
        save_db(db)
        await callback_handler(update, context) # Refresh menu
        return
        
    elif callback_data == "autobc_set_interval":
        context.user_data['state'] = "awaiting_autobc_interval"
        await query.edit_message_text("⏰ Silakan kirim *interval baru* dalam hitungan menit (contoh: `60`).", parse_mode=ParseMode.MARKDOWN)
        return

    # Menu Admin
    elif callback_data == "menu_admin":
        if not is_main_admin(query.from_user.id):
            await query.edit_message_text("❌ Hanya admin utama yang bisa mengelola admin.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Kembali", callback_data="main_menu")]]))
            return

        admins = db.get("admins", [])
        admin_list = "\n".join([f"- `{admin_id}`" for admin_id in admins])
        keyboard = [
            [InlineKeyboardButton("Tambah Admin", callback_data="admin_add")],
            [InlineKeyboardButton("Hapus Admin", callback_data="admin_del")],
            [InlineKeyboardButton("🏠 Menu Utama", callback_data="main_menu")],
            [InlineKeyboardButton("⬅️ Kembali ke Settings", callback_data="settings")]
        ]
        await query.edit_message_text(f"👑 *MANAJEMEN ADMIN*\n\n*Daftar Admin:*\n{admin_list}\n\n⚠️ *Hanya admin utama yang bisa mengelola admin!*", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
        return
        
    elif callback_data == "admin_add":
        if not is_main_admin(query.from_user.id):
            await query.edit_message_text("❌ Hanya admin utama yang bisa menambah admin.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Kembali", callback_data="menu_admin")]]))
            return
        context.user_data['state'] = "awaiting_admin_add"
        await query.edit_message_text("➕ Silakan kirim *User ID* admin yang baru.", parse_mode=ParseMode.MARKDOWN)
        return

    elif callback_data == "admin_del":
        if not is_main_admin(query.from_user.id):
            await query.edit_message_text("❌ Hanya admin utama yang bisa menghapus admin.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Kembali", callback_data="menu_admin")]]))
            return
        context.user_data['state'] = "awaiting_admin_del"
        await query.edit_message_text("➖ Silakan kirim *User ID* admin yang ingin dihapus.", parse_mode=ParseMode.MARKDOWN)
        return

    # Menu Backup & Restore
    elif callback_data == "menu_backup":
        keyboard = [
            [InlineKeyboardButton("💾 Backup Database", callback_data="backup_db")],
            [InlineKeyboardButton("📁 Restore Database", callback_data="restore_db")],
            [InlineKeyboardButton("📊 Export CSV", callback_data="export_csv")],
            [InlineKeyboardButton("🏠 Menu Utama", callback_data="main_menu")],
            [InlineKeyboardButton("⬅️ Kembali ke Settings", callback_data="settings")]
        ]
        await query.edit_message_text("💾 *BACKUP & RESTORE DATABASE*\n\nKelola backup dan export data bot.", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
        return

    elif callback_data == "backup_db":
        try:
            import json
            from datetime import datetime

            db = load_db()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"backup_{timestamp}.json"

            with open(backup_filename, 'w', encoding='utf-8') as f:
                json.dump(db, f, indent=4, ensure_ascii=False)

            # Kirim file backup ke admin
            with open(backup_filename, 'rb') as f:
                await context.bot.send_document(chat_id=query.from_user.id, document=f, filename=backup_filename, caption="✅ *BACKUP BERHASIL*\n\nFile backup database telah dibuat dan dikirim.")

            # Hapus file lokal setelah dikirim
            import os
            os.remove(backup_filename)

            await query.edit_message_text("✅ Backup berhasil! File telah dikirim ke chat pribadi Anda.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Kembali", callback_data="menu_backup")], [InlineKeyboardButton("🏠 Menu Utama", callback_data="main_menu")]]))
        except Exception as e:
            await query.edit_message_text(f"❌ Gagal membuat backup: {str(e)}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Kembali", callback_data="menu_backup")]]))
        return

    elif callback_data == "restore_db":
        context.user_data['state'] = "awaiting_restore_file"
        await query.edit_message_text("📁 *RESTORE DATABASE*\n\nSilakan kirim file backup (.json) yang ingin direstore.\n\n⚠️ *PERINGATAN:* Data saat ini akan digantikan!", parse_mode=ParseMode.MARKDOWN)
        return

    elif callback_data == "export_csv":
        try:
            import csv
            from io import StringIO

            db = load_db()
            users = db.get("users", [])
            admins = db.get("admins", [])

            # Buat CSV untuk users
            csv_output = StringIO()
            writer = csv.writer(csv_output)
            writer.writerow(['User ID', 'Type'])

            for user_id in users:
                user_type = "Admin" if user_id in admins else "User"
                writer.writerow([user_id, user_type])

            csv_content = csv_output.getvalue()
            csv_output.close()

            # Kirim file CSV
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"users_export_{timestamp}.csv"

            await context.bot.send_document(
                chat_id=query.from_user.id,
                document=csv_content.encode('utf-8'),
                filename=filename,
                caption="📊 *EXPORT DATA USERS*\n\nFile CSV berisi daftar semua users dan admin telah dikirim."
            )

            await query.edit_message_text("✅ Export CSV berhasil! File telah dikirim ke chat pribadi Anda.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Kembali", callback_data="menu_backup")], [InlineKeyboardButton("🏠 Menu Utama", callback_data="main_menu")]]))

        except Exception as e:
            await query.edit_message_text(f"❌ Gagal export CSV: {str(e)}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Kembali", callback_data="menu_backup")]]))
        return

    # Menu Custom Commands
    elif callback_data == "menu_custom":
        custom_cmds = db.get("custom_commands", {})
        cmd_list = "\n".join([f"• `/{cmd}`" for cmd in custom_cmds.keys()]) if custom_cmds else "Belum ada custom command"

        keyboard = [
            [InlineKeyboardButton("➕ Tambah Command", callback_data="custom_add")],
            [InlineKeyboardButton("🗑️ Hapus Command", callback_data="custom_del")],
            [InlineKeyboardButton("📋 List Commands", callback_data="custom_list")],
            [InlineKeyboardButton("🏠 Menu Utama", callback_data="main_menu")],
            [InlineKeyboardButton("⬅️ Kembali ke Settings", callback_data="settings")]
        ]
        await query.edit_message_text(f"⚡ *CUSTOM COMMANDS*\n\n*Commands tersedia:*\n{cmd_list}\n\nKelola command custom untuk response otomatis.", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
        return

    elif callback_data == "custom_add":
        context.user_data['state'] = "awaiting_custom_cmd"
        await query.edit_message_text("⚡ *TAMBAH CUSTOM COMMAND*\n\nKirim dengan format:\n`command_name | pesan response`\n\nContoh:\n`promo | Selamat datang di promo spesial!`", parse_mode=ParseMode.MARKDOWN)
        return

    elif callback_data == "custom_del":
        custom_cmds = db.get("custom_commands", {})
        if not custom_cmds:
            await query.edit_message_text("❌ Tidak ada custom command yang bisa dihapus.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Kembali", callback_data="menu_custom")]]))
            return

        keyboard = []
        for cmd in custom_cmds.keys():
            keyboard.append([InlineKeyboardButton(f"🗑️ /{cmd}", callback_data=f"del_custom_{cmd}")])
        keyboard.append([InlineKeyboardButton("⬅️ Kembali", callback_data="menu_custom")])

        await query.edit_message_text("🗑️ *HAPUS CUSTOM COMMAND*\n\nPilih command yang ingin dihapus:", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
        return

    elif callback_data == "custom_list":
        custom_cmds = db.get("custom_commands", {})
        if not custom_cmds:
            await query.edit_message_text("📋 *LIST CUSTOM COMMANDS*\n\nBelum ada custom command yang dibuat.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Kembali", callback_data="menu_custom")]]))
            return

        cmd_details = ""
        for cmd, response in custom_cmds.items():
            cmd_details += f"• `/{cmd}` → {response[:50]}{'...' if len(response) > 50 else ''}\n"

        await query.edit_message_text(f"📋 *LIST CUSTOM COMMANDS*\n\n{cmd_details}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Kembali", callback_data="menu_custom")]]), parse_mode=ParseMode.MARKDOWN)
        return

    elif callback_data.startswith("del_custom_"):
        cmd_to_delete = callback_data.replace("del_custom_", "")
        if "custom_commands" in db and cmd_to_delete in db["custom_commands"]:
            del db["custom_commands"][cmd_to_delete]
            save_db(db)
            await query.edit_message_text(f"✅ Custom command `/{cmd_to_delete}` berhasil dihapus!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Kembali", callback_data="menu_custom")], [InlineKeyboardButton("🏠 Menu Utama", callback_data="main_menu")]]), parse_mode=ParseMode.MARKDOWN)
        else:
            await query.edit_message_text("❌ Command tidak ditemukan.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Kembali", callback_data="menu_custom")]]))
        return

    # Menu Anti-Spam
    elif callback_data == "menu_antispam":
        antispam_config = db.get("anti_spam", {})
        status = "🟢 AKTIF" if antispam_config.get("enabled") else "🔴 MATI"
        max_msg = antispam_config.get("max_messages_per_minute", 5)

        keyboard = [
            [InlineKeyboardButton(f"Status: {status}", callback_data="antispam_toggle")],
            [InlineKeyboardButton(f"Max Pesan: {max_msg}/menit", callback_data="antispam_set_limit")],
            [InlineKeyboardButton("📝 Kata Terlarang", callback_data="antispam_banned_words")],
            [InlineKeyboardButton("🏠 Menu Utama", callback_data="main_menu")],
            [InlineKeyboardButton("⬅️ Kembali ke Settings", callback_data="settings")]
        ]
        await query.edit_message_text("🛡️ *ANTI-SPAM SYSTEM*\n\nSistem deteksi spam otomatis untuk menjaga kualitas interaksi.", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
        return

    elif callback_data == "antispam_toggle":
        if "anti_spam" not in db:
            db["anti_spam"] = DEFAULT_DB["anti_spam"]
        db["anti_spam"]["enabled"] = not db["anti_spam"].get("enabled", False)
        save_db(db)
        await callback_handler(update, context)  # Refresh menu
        return

    elif callback_data == "antispam_set_limit":
        context.user_data['state'] = "awaiting_spam_limit"
        await query.edit_message_text("🛡️ *SET LIMIT PESAN*\n\nKirim angka untuk maksimal pesan per menit (contoh: `5`)", parse_mode=ParseMode.MARKDOWN)
        return

    elif callback_data == "antispam_banned_words":
        banned_words = db.get("anti_spam", {}).get("banned_words", [])
        words_list = "\n".join([f"• `{word}`" for word in banned_words]) if banned_words else "Belum ada kata terlarang"

        keyboard = [
            [InlineKeyboardButton("➕ Tambah Kata", callback_data="add_banned_word")],
            [InlineKeyboardButton("🗑️ Hapus Kata", callback_data="del_banned_word")],
            [InlineKeyboardButton("⬅️ Kembali", callback_data="menu_antispam")]
        ]
        await query.edit_message_text(f"📝 *KATA TERLARANG*\n\n{words_list}", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
        return

    elif callback_data == "add_banned_word":
        context.user_data['state'] = "awaiting_banned_word"
        await query.edit_message_text("➕ *TAMBAH KATA TERLARANG*\n\nKirim kata yang ingin dilarang (pisah dengan koma untuk multiple):\n`kata1, kata2, kata3`", parse_mode=ParseMode.MARKDOWN)
        return

    elif callback_data == "del_banned_word":
        banned_words = db.get("anti_spam", {}).get("banned_words", [])
        if not banned_words:
            await query.edit_message_text("❌ Tidak ada kata terlarang yang bisa dihapus.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Kembali", callback_data="antispam_banned_words")]]))
            return

        keyboard = []
        for word in banned_words:
            keyboard.append([InlineKeyboardButton(f"🗑️ {word}", callback_data=f"del_word_{word}")])
        keyboard.append([InlineKeyboardButton("⬅️ Kembali", callback_data="antispam_banned_words")])

        await query.edit_message_text("🗑️ *HAPUS KATA TERLARANG*\n\nPilih kata yang ingin dihapus:", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    elif callback_data.startswith("del_word_"):
        word_to_delete = callback_data.replace("del_word_", "")
        if "anti_spam" in db and "banned_words" in db["anti_spam"] and word_to_delete in db["anti_spam"]["banned_words"]:
            db["anti_spam"]["banned_words"].remove(word_to_delete)
            save_db(db)
            await query.edit_message_text(f"✅ Kata `{word_to_delete}` berhasil dihapus dari daftar terlarang!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Kembali", callback_data="antispam_banned_words")], [InlineKeyboardButton("🏠 Menu Utama", callback_data="main_menu")]]), parse_mode=ParseMode.MARKDOWN)
        else:
            await query.edit_message_text("❌ Kata tidak ditemukan.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Kembali", callback_data="antispam_banned_words")]]))
        return

    # Menu Sang Mata (User Logs)
    elif callback_data == "menu_sangmata":
        user_logs = db.get("user_logs", [])
        total_logs = len(user_logs)

        keyboard = [
            [InlineKeyboardButton("🔍 Cari by Username", callback_data="search_user_logs")],
            [InlineKeyboardButton("📋 Lihat Semua Logs", callback_data="view_all_logs")],
            [InlineKeyboardButton("🧹 Hapus Semua Logs", callback_data="clear_all_logs")],
            [InlineKeyboardButton("🏠 Menu Utama", callback_data="main_menu")],
            [InlineKeyboardButton("⬅️ Kembali ke Settings", callback_data="settings")]
        ]

        await query.edit_message_text(f"👁️ *SANG MATA - USER LOGS*\n\n📊 Total Logs: `{total_logs}`\n\nFitur untuk memantau aktivitas user dengan detail.", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
        return

    elif callback_data == "search_user_logs":
        context.user_data['state'] = "awaiting_username_search"
        await query.edit_message_text("🔍 *CARI LOG USER*\n\nKirim username yang ingin dicari (tanpa @):\n\nContoh: `john_doe`", parse_mode=ParseMode.MARKDOWN)
        return

    elif callback_data == "view_all_logs":
        user_logs = db.get("user_logs", [])
        if not user_logs:
            await query.edit_message_text("📋 *USER LOGS*\n\nBelum ada aktivitas user yang tercatat.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Kembali", callback_data="menu_sangmata")]]), parse_mode=ParseMode.MARKDOWN)
            return

        # Ambil 10 log terakhir
        recent_logs = user_logs[-10:]
        log_text = "📋 *10 LOG TERAKHIR*\n\n"

        for i, log in enumerate(reversed(recent_logs), 1):
            from datetime import datetime
            timestamp = datetime.fromisoformat(log['timestamp']).strftime("%d/%m %H:%M")
            username = log.get('username', 'N/A') or 'N/A'
            action = log.get('action', 'N/A')
            log_text += f"{i}. `{timestamp}` | @{username} | {action}\n"

        keyboard = [
            [InlineKeyboardButton("⬅️ Kembali", callback_data="menu_sangmata")],
            [InlineKeyboardButton("🏠 Menu Utama", callback_data="main_menu")]
        ]

        await query.edit_message_text(log_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
        return

    elif callback_data == "clear_all_logs":
        keyboard = [
            [InlineKeyboardButton("✅ Ya, Hapus Semua", callback_data="confirm_clear_logs")],
            [InlineKeyboardButton("❌ Batal", callback_data="menu_sangmata")]
        ]
        await query.edit_message_text("🧹 *HAPUS SEMUA LOGS*\n\n⚠️ Yakin ingin menghapus semua log aktivitas user?\n\nTindakan ini tidak dapat dibatalkan!", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
        return

    elif callback_data == "confirm_clear_logs":
        db["user_logs"] = []
        save_db(db)
        await query.edit_message_text("✅ Semua log aktivitas user telah dihapus!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Kembali", callback_data="menu_sangmata")], [InlineKeyboardButton("🏠 Menu Utama", callback_data="main_menu")]]), parse_mode=ParseMode.MARKDOWN)
        return

    # Menu Fitur Canggih
    elif callback_data == "menu_advanced":
        keyboard = [
            [InlineKeyboardButton("👥 Welcome Group", callback_data="menu_group_welcome")],
            [InlineKeyboardButton("⏰ Scheduled Messages", callback_data="menu_scheduled")],
            [InlineKeyboardButton("🎯 Quick Actions", callback_data="menu_quick_actions")],
            [InlineKeyboardButton("🏠 Menu Utama", callback_data="main_menu")],
            [InlineKeyboardButton("⬅️ Kembali ke Settings", callback_data="settings")]
        ]
        await query.edit_message_text("🚀 *FITUR CANGGIH*\n\nFitur-fitur advanced untuk kemudahan penggunaan.", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
        return

    elif callback_data == "menu_group_welcome":
        group_welcome = db.get("group_welcome", {})
        status = "🟢 AKTIF" if group_welcome.get("enabled") else "🔴 MATI"

        keyboard = [
            [InlineKeyboardButton(f"Status: {status}", callback_data="toggle_group_welcome")],
            [InlineKeyboardButton("✏️ Edit Pesan", callback_data="edit_group_welcome")],
            [InlineKeyboardButton("🖼️ Ubah Foto", callback_data="photo_group_welcome")],
            [InlineKeyboardButton("⬅️ Kembali", callback_data="menu_advanced")],
            [InlineKeyboardButton("🏠 Menu Utama", callback_data="main_menu")]
        ]
        await query.edit_message_text("👥 *WELCOME MESSAGE GROUP*\n\nPesan welcome khusus untuk group chat.", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
        return

    elif callback_data == "toggle_group_welcome":
        if "group_welcome" not in db:
            db["group_welcome"] = DEFAULT_DB["group_welcome"]
        db["group_welcome"]["enabled"] = not db["group_welcome"].get("enabled", False)
        save_db(db)
        await callback_handler(update, context)  # Refresh menu
        return

    elif callback_data == "edit_group_welcome":
        context.user_data['state'] = "awaiting_group_welcome_text"
        await query.edit_message_text("✏️ *EDIT WELCOME GROUP*\n\nKirim pesan welcome baru untuk group:", parse_mode=ParseMode.MARKDOWN)
        return

    elif callback_data == "photo_group_welcome":
        context.user_data['state'] = "awaiting_group_welcome_photo"
        await query.edit_message_text("🖼️ *UBAH FOTO WELCOME GROUP*\n\nKirim foto baru untuk welcome group:", parse_mode=ParseMode.MARKDOWN)
        return

    elif callback_data == "menu_scheduled":
        scheduled_msgs = db.get("scheduled_messages", [])
        keyboard = [
            [InlineKeyboardButton("➕ Tambah Jadwal", callback_data="add_scheduled")],
            [InlineKeyboardButton("📋 List Jadwal", callback_data="list_scheduled")],
            [InlineKeyboardButton("🗑️ Hapus Jadwal", callback_data="del_scheduled")],
            [InlineKeyboardButton("⬅️ Kembali", callback_data="menu_advanced")],
            [InlineKeyboardButton("🏠 Menu Utama", callback_data="main_menu")]
        ]
        await query.edit_message_text(f"⏰ *SCHEDULED MESSAGES*\n\nTotal jadwal: {len(scheduled_msgs)}\n\nKirim pesan otomatis sesuai jadwal.", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
        return

    elif callback_data == "add_scheduled":
        context.user_data['state'] = "awaiting_scheduled_message"
        await query.edit_message_text("⏰ *TAMBAH SCHEDULED MESSAGE*\n\nKirim dengan format:\n`HH:MM | pesan yang ingin dijadwalkan`\n\nContoh:\n`14:30 | Selamat sore! Promo hari ini!`", parse_mode=ParseMode.MARKDOWN)
        return

    elif callback_data == "list_scheduled":
        scheduled_msgs = db.get("scheduled_messages", [])
        if not scheduled_msgs:
            await query.edit_message_text("📋 *SCHEDULED MESSAGES*\n\nBelum ada jadwal pesan yang dibuat.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Kembali", callback_data="menu_scheduled")]]), parse_mode=ParseMode.MARKDOWN)
            return

        msg_text = "📋 *DAFTAR SCHEDULED MESSAGES*\n\n"
        keyboard = []

        for i, msg in enumerate(scheduled_msgs, 1):
            time_str = msg.get('time', 'N/A')
            message_preview = msg.get('message', '')[:50]
            msg_text += f"{i}. ⏰ `{time_str}` | {message_preview}{'...' if len(msg.get('message', '')) > 50 else ''}\n"
            keyboard.append([InlineKeyboardButton(f"🗑️ Hapus #{i}", callback_data=f"del_sched_{i-1}")])

        keyboard.append([InlineKeyboardButton("⬅️ Kembali", callback_data="menu_scheduled")])
        keyboard.append([InlineKeyboardButton("🏠 Menu Utama", callback_data="main_menu")])

        await query.edit_message_text(msg_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
        return

    elif callback_data.startswith("del_sched_"):
        index = int(callback_data.replace("del_sched_", ""))
        scheduled_msgs = db.get("scheduled_messages", [])

        if 0 <= index < len(scheduled_msgs):
            deleted_msg = scheduled_msgs.pop(index)
            db["scheduled_messages"] = scheduled_msgs
            save_db(db)
            await query.edit_message_text(f"✅ Scheduled message berhasil dihapus!\n\n⏰ Waktu: `{deleted_msg.get('time')}`\n📝 Pesan: {deleted_msg.get('message')[:100]}{'...' if len(deleted_msg.get('message', '')) > 100 else ''}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Kembali", callback_data="menu_scheduled")], [InlineKeyboardButton("🏠 Menu Utama", callback_data="main_menu")]]), parse_mode=ParseMode.MARKDOWN)
        else:
            await query.edit_message_text("❌ Scheduled message tidak ditemukan.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Kembali", callback_data="menu_scheduled")]]))
        return

    elif callback_data == "menu_quick_actions":
        keyboard = [
            [InlineKeyboardButton("📢 Broadcast Sekarang", callback_data="quick_broadcast")],
            [InlineKeyboardButton("👥 List User Online", callback_data="quick_online_users")],
            [InlineKeyboardButton("📊 Quick Stats", callback_data="quick_stats")],
            [InlineKeyboardButton("🔄 Restart Bot", callback_data="quick_restart")],
            [InlineKeyboardButton("⬅️ Kembali", callback_data="menu_advanced")],
            [InlineKeyboardButton("🏠 Menu Utama", callback_data="main_menu")]
        ]
        await query.edit_message_text("🎯 *QUICK ACTIONS*\n\nAksi cepat untuk tugas-tugas umum.", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
        return

    elif callback_data == "quick_broadcast":
        # Quick broadcast - gunakan pesan broadcast yang sudah ada
        db = load_db()
        message_config = db.get("broadcast_message", {})
        users = db.get("users", [])

        if not users:
            await query.edit_message_text("❌ Belum ada user terdaftar.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Kembali", callback_data="menu_quick_actions")]]))
            return

        if not (message_config.get("text") or message_config.get("photo")):
            await query.edit_message_text("❌ Pesan broadcast belum diatur.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Kembali", callback_data="menu_quick_actions")]]))
            return

        await query.edit_message_text("📢 *QUICK BROADCAST*\n\nSedang mengirim pesan ke semua user...", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Kembali", callback_data="menu_quick_actions")]]))

        # Jalankan broadcast di background
        import asyncio
        asyncio.create_task(quick_broadcast_task(context, message_config, users, query.from_user.id))
        return

    elif callback_data == "quick_online_users":
        # Quick check online users (semua user dianggap online)
        db = load_db()
        users = db.get("users", [])
        admins = db.get("admins", [])

        online_text = f"👥 *USER ONLINE CHECK*\n\nTotal User: `{len(users)}`\nTotal Admin: `{len(admins)}`\n\n"

        if users:
            online_text += "*Daftar User Online:*\n"
            for i, user_id in enumerate(users[:20], 1):  # Show max 20 users
                user_type = "👑" if user_id in admins else "👤"
                online_text += f"{i}. {user_type} `{user_id}`\n"

            if len(users) > 20:
                online_text += f"\n... dan {len(users) - 20} user lainnya"

        await query.edit_message_text(online_text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Kembali", callback_data="menu_quick_actions")], [InlineKeyboardButton("🏠 Menu Utama", callback_data="main_menu")]]), parse_mode=ParseMode.MARKDOWN)
        return

    elif callback_data == "quick_stats":
        # Quick statistics
        db = load_db()
        users = db.get("users", [])
        admins = db.get("admins", [])
        user_logs = db.get("user_logs", [])

        stats_text = f"""
📊 *QUICK STATISTICS*

👥 Total Users: `{len(users)}`
👑 Total Admins: `{len(admins)}`
📝 Total Logs: `{len(user_logs)}`

⚙️ Auto Broadcast: `{'Aktif' if db.get('auto_broadcast', {}).get('enabled') else 'Mati'}`
🛡️ Anti-Spam: `{'Aktif' if db.get('anti_spam', {}).get('enabled') else 'Mati'}`
👥 Group Welcome: `{'Aktif' if db.get('group_welcome', {}).get('enabled') else 'Mati'}`
        """

        await query.edit_message_text(stats_text.strip(), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Kembali", callback_data="menu_quick_actions")], [InlineKeyboardButton("🏠 Menu Utama", callback_data="main_menu")]]), parse_mode=ParseMode.MARKDOWN)
        return

    elif callback_data == "quick_restart":
        # Quick restart confirmation
        keyboard = [
            [InlineKeyboardButton("✅ Ya, Restart", callback_data="confirm_restart")],
            [InlineKeyboardButton("❌ Batal", callback_data="menu_quick_actions")]
        ]
        await query.edit_message_text("🔄 *RESTART BOT*\n\n⚠️ Yakin ingin restart bot?\n\nBot akan offline sebentar.", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
        return

    elif callback_data == "confirm_restart":
        await query.edit_message_text("🔄 *BOT SEDANG RESTART...*\n\nBot akan kembali online dalam beberapa detik.", parse_mode=ParseMode.MARKDOWN)
        # Note: Actual restart would require external script or supervisor
        return

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menangani pesan teks biasa untuk melanjutkan proses settings."""
    user_id = update.effective_user.id
    state = context.user_data.get('state')
    text_input = update.message.text or ""

    # Anti-Spam Check
    db = load_db()
    antispam_config = db.get("anti_spam", {})
    if antispam_config.get("enabled") and not is_admin(user_id):
        # Track messages per user
        current_time = datetime.now()
        user_key = f"user_{user_id}"

        if user_key not in context.user_data:
            context.user_data[user_key] = []

        # Clean old messages (older than 1 minute)
        context.user_data[user_key] = [
            msg_time for msg_time in context.user_data[user_key]
            if (current_time - msg_time).seconds < 60
        ]

        # Add current message
        context.user_data[user_key].append(current_time)

        # Check message limit
        max_messages = antispam_config.get("max_messages_per_minute", 5)
        if len(context.user_data[user_key]) > max_messages:
            warning_msg = antispam_config.get("warning_message", "⚠️ Terdeteksi spam!")
            await update.message.reply_text(warning_msg)
            return

        # Check banned words
        banned_words = antispam_config.get("banned_words", [])
        message_lower = text_input.lower()
        for word in banned_words:
            if word.lower() in message_lower:
                await update.message.reply_text("❌ Pesan mengandung kata terlarang!")
                return

    # Handle forward message untuk Sang Mata
    if update.message.forward_from or update.message.forward_from_chat:
        await handle_forward_message(update, context)
        return

    if not is_admin(user_id) or not state:
        return

    text_input = update.message.text
    db = load_db()
    
    # Menangani input teks
    if state.startswith("awaiting_text_"):
        key = state.replace("awaiting_text_", "")
        if key == "welcome":
            if "welcome_message" not in db:
                db["welcome_message"] = DEFAULT_DB["welcome_message"]
            db["welcome_message"]["text"] = text_input
        elif key == "broadcast":
            if "broadcast_message" not in db:
                db["broadcast_message"] = DEFAULT_DB["broadcast_message"]
            db["broadcast_message"]["text"] = text_input
        elif key == "autobroadcast_msg":
            if "auto_broadcast" not in db:
                db["auto_broadcast"] = DEFAULT_DB["auto_broadcast"]
            if "message" not in db["auto_broadcast"] or not isinstance(db["auto_broadcast"]["message"], dict):
                db["auto_broadcast"]["message"] = DEFAULT_DB["auto_broadcast"]["message"]
            db["auto_broadcast"]["message"]["text"] = text_input
        await update.message.reply_text("✅ Teks berhasil diubah.")
    
    # Menangani input tombol
    elif state.startswith("awaiting_button_"):
        key = state.replace("awaiting_button_", "")
        parts = text_input.split(" | ")
        if len(parts) != 2:
            await update.message.reply_text("❌ Format salah. Gunakan: `Nama Tombol | https://link.com`", parse_mode=ParseMode.MARKDOWN)
        else:
            button_text, url = parts
            if key == "welcome":
                if "welcome_message" not in db:
                    db["welcome_message"] = DEFAULT_DB["welcome_message"]
                db["welcome_message"]["buttons"].append({"text": button_text, "url": url})
            elif key == "broadcast":
                if "broadcast_message" not in db:
                    db["broadcast_message"] = DEFAULT_DB["broadcast_message"]
                db["broadcast_message"]["buttons"].append({"text": button_text, "url": url})
            elif key == "autobroadcast_msg":
                if "auto_broadcast" not in db:
                    db["auto_broadcast"] = DEFAULT_DB["auto_broadcast"]
                if "message" not in db["auto_broadcast"] or not isinstance(db["auto_broadcast"]["message"], dict):
                    db["auto_broadcast"]["message"] = DEFAULT_DB["auto_broadcast"]["message"]
                db["auto_broadcast"]["message"]["buttons"].append({"text": button_text, "url": url})
            await update.message.reply_text("✅ Tombol baru berhasil ditambahkan.")

    # Menangani input lain-lain
    elif state == "awaiting_autobc_interval":
        try:
            interval = int(text_input)
            if interval <= 0: raise ValueError
            db["auto_broadcast"]["interval_minutes"] = interval
            save_db(db)
            await update.message.reply_text(f"✅ Interval auto broadcast diubah menjadi {interval} menit.")

            # Restart job queue dengan interval baru
            if hasattr(context, 'application') and context.application.job_queue:
                # Hapus job yang ada
                jobs = context.application.job_queue.jobs()
                for job in jobs:
                    if job.name == "auto_broadcast":
                        job.schedule_removal()

                # Tambahkan job baru
                context.application.job_queue.run_repeating(auto_broadcast_task, interval=interval * 60, first=10, name="auto_broadcast")
                await update.message.reply_text("✅ Job queue telah di-restart dengan interval baru.")
            else:
                await update.message.reply_text("⚠️ Job queue tidak tersedia. Restart bot secara manual untuk menerapkan perubahan.")
        except ValueError:
            await update.message.reply_text("❌ Interval harus berupa angka positif.")
    elif state == "awaiting_admin_add":
        if not is_main_admin(user_id):
            await update.message.reply_text("❌ Hanya admin utama yang bisa menambah admin.")
        else:
            try:
                new_admin_id = int(text_input.strip())
                if new_admin_id in db["admins"]:
                    await update.message.reply_text("❌ User tersebut sudah menjadi admin.")
                else:
                    db["admins"].append(new_admin_id)
                    save_db(db)
                    log_user_activity(update.effective_user, "add_admin", f"Menambah admin baru: {new_admin_id}")
                    await update.message.reply_text(f"✅ Admin baru berhasil ditambahkan: `{new_admin_id}`")
            except ValueError:
                await update.message.reply_text("❌ User ID harus berupa angka.")
    elif state == "awaiting_admin_del":
        if not is_main_admin(user_id):
            await update.message.reply_text("❌ Hanya admin utama yang bisa menghapus admin.")
        else:
            try:
                del_admin_id = int(text_input.strip())
                if del_admin_id == ADMIN_IDS[0]:
                    await update.message.reply_text("❌ Tidak bisa menghapus admin utama.")
                elif del_admin_id not in db["admins"]:
                    await update.message.reply_text("❌ User tersebut bukan admin.")
                else:
                    db["admins"].remove(del_admin_id)
                    save_db(db)
                    log_user_activity(update.effective_user, "remove_admin", f"Menghapus admin: {del_admin_id}")
                    await update.message.reply_text(f"✅ Admin berhasil dihapus: `{del_admin_id}`")
            except ValueError:
                await update.message.reply_text("❌ User ID harus berupa angka.")
    elif state == "awaiting_custom_cmd":
        if not is_admin(user_id):
            await update.message.reply_text("❌ Anda tidak punya izin.")
        else:
            parts = text_input.split(" | ", 1)
            if len(parts) != 2:
                await update.message.reply_text("❌ Format salah! Gunakan: `command_name | pesan response`", parse_mode=ParseMode.MARKDOWN)
            else:
                cmd_name, response = parts
                cmd_name = cmd_name.strip().lower()

                if "custom_commands" not in db:
                    db["custom_commands"] = {}

                db["custom_commands"][cmd_name] = response.strip()
                save_db(db)
                await update.message.reply_text(f"✅ Custom command `/{cmd_name}` berhasil ditambahkan!\n\nResponse: {response[:100]}{'...' if len(response) > 100 else ''}", parse_mode=ParseMode.MARKDOWN)
    elif state == "awaiting_spam_limit":
        if not is_admin(user_id):
            await update.message.reply_text("❌ Anda tidak punya izin.")
        else:
            try:
                limit = int(text_input.strip())
                if limit <= 0:
                    raise ValueError
                if "anti_spam" not in db:
                    db["anti_spam"] = DEFAULT_DB["anti_spam"]
                db["anti_spam"]["max_messages_per_minute"] = limit
                save_db(db)
                await update.message.reply_text(f"✅ Limit anti-spam diubah menjadi {limit} pesan per menit.")
            except ValueError:
                await update.message.reply_text("❌ Limit harus berupa angka positif.")
    elif state == "awaiting_banned_word":
        if not is_admin(user_id):
            await update.message.reply_text("❌ Anda tidak punya izin.")
        else:
            words = [word.strip().lower() for word in text_input.split(',')]
            if "anti_spam" not in db:
                db["anti_spam"] = DEFAULT_DB["anti_spam"]
            if "banned_words" not in db["anti_spam"]:
                db["anti_spam"]["banned_words"] = []

            added_words = []
            for word in words:
                if word and word not in db["anti_spam"]["banned_words"]:
                    db["anti_spam"]["banned_words"].append(word)
                    added_words.append(word)

            save_db(db)
            if added_words:
                await update.message.reply_text(f"✅ Kata terlarang berhasil ditambahkan: {', '.join(added_words)}")
            else:
                await update.message.reply_text("ℹ️ Tidak ada kata baru yang ditambahkan (sudah ada atau kosong).")
    elif state == "awaiting_group_welcome_text":
        if not is_admin(user_id):
            await update.message.reply_text("❌ Anda tidak punya izin.")
        else:
            if "group_welcome" not in db:
                db["group_welcome"] = DEFAULT_DB["group_welcome"]
            db["group_welcome"]["text"] = text_input
            save_db(db)
            await update.message.reply_text("✅ Pesan welcome group berhasil diubah!")
    elif state == "awaiting_scheduled_message":
        if not is_admin(user_id):
            await update.message.reply_text("❌ Anda tidak punya izin.")
        else:
            # Format: "HH:MM | pesan"
            parts = text_input.split(" | ", 1)
            if len(parts) != 2:
                await update.message.reply_text("❌ Format salah! Gunakan: `HH:MM | pesan`", parse_mode=ParseMode.MARKDOWN)
            else:
                time_str, message = parts
                try:
                    # Validasi format waktu
                    from datetime import datetime
                    datetime.strptime(time_str, "%H:%M")

                    if "scheduled_messages" not in db:
                        db["scheduled_messages"] = []

                    scheduled_msg = {
                        "time": time_str,
                        "message": message,
                        "created_by": user_id,
                        "created_at": datetime.now().isoformat()
                    }

                    db["scheduled_messages"].append(scheduled_msg)
                    save_db(db)
                    await update.message.reply_text(f"✅ Scheduled message berhasil ditambahkan!\n\n⏰ Waktu: `{time_str}`\n📝 Pesan: {message[:100]}{'...' if len(message) > 100 else ''}", parse_mode=ParseMode.MARKDOWN)
                except ValueError:
                    await update.message.reply_text("❌ Format waktu salah! Gunakan format HH:MM (contoh: 14:30)")
    elif state == "awaiting_username_search":
        if not is_admin(user_id):
            await update.message.reply_text("❌ Anda tidak punya izin.")
        else:
            username_search = text_input.strip().lower()
            user_logs = db.get("user_logs", [])

            # Cari log berdasarkan username
            matching_logs = [
                log for log in user_logs
                if log.get('username', '').lower() == username_search or
                   username_search in log.get('username', '').lower()
            ]

            if not matching_logs:
                await update.message.reply_text(f"🔍 *HASIL PENCARIAN*\n\nTidak ditemukan log untuk username: `{username_search}`", parse_mode=ParseMode.MARKDOWN)
            else:
                log_text = f"🔍 *LOG AKTIVITAS USER*\n\nUsername: `{username_search}`\nTotal: {len(matching_logs)} aktivitas\n\n"

                # Ambil 10 aktivitas terakhir
                recent_logs = matching_logs[-10:]
                for i, log in enumerate(reversed(recent_logs), 1):
                    timestamp = datetime.fromisoformat(log['timestamp']).strftime("%d/%m/%Y %H:%M")
                    action = log.get('action', 'N/A')
                    details = log.get('details', '')
                    log_text += f"{i}. `{timestamp}` | {action}"
                    if details:
                        log_text += f" | {details[:30]}{'...' if len(details) > 30 else ''}"
                    log_text += "\n"

                await update.message.reply_text(log_text, parse_mode=ParseMode.MARKDOWN)
    elif state == "awaiting_sangmata_search":
        username_search = text_input.strip().lower()
        db = load_db()
        user_logs = db.get("user_logs", [])

        # Cari user berdasarkan username di logs
        matching_users = {}
        for log in user_logs:
            log_username = log.get('username', '').lower()
            if log_username == username_search or username_search in log_username:
                user_id = log.get('user_id')
                if user_id not in matching_users:
                    matching_users[user_id] = {
                        'user_id': user_id,
                        'username': log.get('username'),
                        'first_name': log.get('first_name'),
                        'last_seen': log.get('timestamp'),
                        'activity_count': 0
                    }
                matching_users[user_id]['activity_count'] += 1

        if not matching_users:
            await update.message.reply_text(f"🔍 *HASIL PENCARIAN*\n\nTidak ditemukan user dengan username: `{username_search}`", parse_mode=ParseMode.MARKDOWN)
        else:
            response = f"🔍 *SANG MATA - HASIL PENCARIAN*\n\nUsername: `{username_search}`\nDitemukan: {len(matching_users)} user\n\n"

            # Tampilkan hasil pencarian
            for i, (user_id, user_info) in enumerate(matching_users.items(), 1):
                username = user_info['username'] or 'N/A'
                first_name = user_info['first_name'] or 'N/A'
                activity_count = user_info['activity_count']
                last_seen = datetime.fromisoformat(user_info['last_seen']).strftime("%d/%m/%Y %H:%M")

                response += f"{i}. 🆔 `{user_id}`\n"
                response += f"   👤 {first_name}\n"
                response += f"   📝 @{username}\n"
                response += f"   📊 {activity_count} aktivitas\n"
                response += f"   🕐 Terakhir: {last_seen}\n\n"

            await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)

    save_db(db)
    context.user_data['state'] = None

    # Handle custom commands
    if text_input.startswith('/'):
        cmd = text_input[1:].lower().split()[0]  # Ambil command tanpa /
        custom_cmds = db.get("custom_commands", {})

        if cmd in custom_cmds:
            response = custom_cmds[cmd]
            # Ganti placeholder jika ada
            response = replace_placeholders(response, update.effective_user)
            await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)
            return


async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menangani pengiriman foto untuk settings."""
    user_id = update.effective_user.id
    state = context.user_data.get('state')

    if not is_admin(user_id) or not state or not state.startswith("awaiting_photo_"):
        return

    db = load_db()
    key = state.replace("awaiting_photo_", "")
    photo_id = update.message.photo[-1].file_id

    if key == "welcome":
        db["welcome_message"]["photo"] = photo_id
    elif key == "broadcast":
        db["broadcast_message"]["photo"] = photo_id
    elif key == "autobroadcast_msg":
        db["auto_broadcast"]["message"]["photo"] = photo_id

    save_db(db)
    context.user_data['state'] = None

    await update.message.reply_text("✅ Foto berhasil disimpan!")
    return

async def photo_handler_group_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler khusus untuk photo group welcome."""
    user_id = update.effective_user.id
    state = context.user_data.get('state')

    if not is_admin(user_id) or state != "awaiting_group_welcome_photo":
        return

    db = load_db()
    if "group_welcome" not in db:
        db["group_welcome"] = DEFAULT_DB["group_welcome"]

    photo_id = update.message.photo[-1].file_id
    db["group_welcome"]["photo"] = photo_id
    save_db(db)

    context.user_data['state'] = None
    await update.message.reply_text("✅ Foto welcome group berhasil disimpan!")

async def document_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menangani pengiriman file document untuk restore."""
    user_id = update.effective_user.id
    state = context.user_data.get('state')

    if not is_admin(user_id) or state != "awaiting_restore_file":
        return

    try:
        document = update.message.document
        if not document.file_name.endswith('.json'):
            await update.message.reply_text("❌ File harus berformat .json!")
            return

        # Download file
        file = await context.bot.get_file(document.file_id)
        file_content = await file.download_as_bytearray()

        # Parse JSON
        import json
        restored_db = json.loads(file_content.decode('utf-8'))

        # Validasi struktur database
        required_keys = ["users", "admins", "welcome_message", "broadcast_message", "auto_broadcast"]
        if not all(key in restored_db for key in required_keys):
            await update.message.reply_text("❌ File backup tidak valid! Struktur database tidak lengkap.")
            return

        # Backup database saat ini sebelum restore
        current_db = load_db()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"pre_restore_backup_{timestamp}.json"

        with open(backup_filename, 'w', encoding='utf-8') as f:
            json.dump(current_db, f, indent=4, ensure_ascii=False)

        # Lakukan restore
        save_db(restored_db)

        await update.message.reply_text("✅ *RESTORE BERHASIL!*\n\nDatabase telah direstore dari file backup.\n\n⚠️ Backup sebelum restore tersimpan sebagai file lokal.", parse_mode=ParseMode.MARKDOWN)

    except json.JSONDecodeError:
        await update.message.reply_text("❌ File JSON tidak valid!")
    except Exception as e:
        await update.message.reply_text(f"❌ Gagal restore database: {str(e)}")

    context.user_data['state'] = None


# Handler duplikat dihapus, sudah ditangani di photo_handler yang lebih umum


async def set_bot_commands(application: Application):
    """Mengatur daftar command yang muncul di Telegram."""
    commands = [
        BotCommand("start", "▶️ Mulai bot"),
        BotCommand("help", "ℹ️ Lihat bantuan"),
        BotCommand("guide", "📚 Guide placeholder pesan"),
        BotCommand("sangmata", "👁️ Cari user by username"),
        BotCommand("settings", "⚙️ Pengaturan (Admin)"),
        BotCommand("broadcast", "📢 Kirim pesan ke semua user (Admin)"),
        BotCommand("stats", "📊 Lihat statistik bot (Admin)"),
        BotCommand("getid", "🆔 Dapatkan ID user/chat"),
        BotCommand("listusers", "👥 Lihat daftar user (Admin)"),
    ]
    await application.bot.set_my_commands(commands)


# --- MAIN FUNCTION ---
def main():
    """Fungsi utama untuk menjalankan bot."""
    print("Memulai bot...")
    
    # Buat database jika belum ada
    if not os.path.exists(DB_FILE):
        save_db(DEFAULT_DB)

    # Inisialisasi Application
    application = Application.builder().token(TOKEN).build()
    
    # Daftarkan job queue untuk auto broadcast
    job_queue = application.job_queue
    if job_queue:
        db = load_db()
        interval = db.get("auto_broadcast", {}).get("interval_minutes", 60)
        job_queue.run_repeating(auto_broadcast_task, interval=interval * 60, first=10, name="auto_broadcast")
        print(f"Auto broadcast job dijadwalkan setiap {interval} menit.")
    else:
        print("PERINGATAN: JobQueue tidak tersedia. Fitur auto broadcast tidak akan berjalan.")

    # Daftarkan command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("guide", guide_command))
    application.add_handler(CommandHandler("sangmata", sangmata_command))
    application.add_handler(CommandHandler("broadcast", broadcast_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("settings", settings_command))
    application.add_handler(CommandHandler("getid", getid_command))
    application.add_handler(CommandHandler("listusers", listusers_command))

    # Daftarkan handler untuk interaksi menu dan settings
    application.add_handler(CallbackQueryHandler(callback_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    application.add_handler(MessageHandler(filters.PHOTO, photo_handler))
    application.add_handler(MessageHandler(filters.Document.ALL, document_handler))

    # Forward message akan ditangani di message_handler

    # Handler khusus untuk group welcome photo - menggunakan state check
    application.add_handler(MessageHandler(
        filters.PHOTO,
        photo_handler_group_welcome
    ))
    
    # Atur command bot
    application.post_init = set_bot_commands

    # Jalankan bot
    print("Bot sedang berjalan... Tekan Ctrl+C untuk berhenti.")
    application.run_polling()


if __name__ == "__main__":
    main()