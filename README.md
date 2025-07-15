# EA Grid Hedging - MetaAPI + Render

## Strategi
- Pair: EURUSD
- Grid jarak: 5 pip
- Take Profit: 5 pip
- Lot tetap: 0.01
- Buka BUY dan SELL bersamaan, tutup saat TP tercapai

## Cara Jalankan (di Render.com)
1. Upload file ke GitHub repo (main.py + requirements.txt)
2. Buat Web Service di Render.com
3. Build command: `pip install -r requirements.txt`
4. Start command: `python main.py`
5. Tambahkan Environment Variable:
   - `TOKEN`: token dari metaapi.cloud
   - `ACCOUNT_ID`: account ID dari akun MT4 kamu