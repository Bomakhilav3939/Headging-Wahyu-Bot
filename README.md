# EA Hedging EURUSD (5 Pip Grid)

Strategi hedging otomatis menggunakan MetaApi (MT4) + notifikasi Telegram.

## 📌 Strategi
- Buka BUY + SELL di EURUSD setiap 5 pip
- TP 5 pip masing-masing
- Jika salah satu TP, buka BUY+SELL ulang

## 🚀 Deploy ke Railway
1. Buat project di Railway
2. Tambahkan environment variables (lihat `.env.example`)
3. Deploy dan aktifkan

## 🛠️ File Penting
- `main.py` = logika utama
- `telegram_notifier.py` = notifikasi sinyal
- `requirements.txt` = dependensi Python
- `Procfile` = supaya Railway tahu cara menjalankan bot
