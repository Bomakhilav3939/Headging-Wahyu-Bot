
import asyncio
import os
from metaapi_cloud_sdk import MetaApi

# Ambil token dan ID akun dari environment variable (isi di Render)
TOKEN = os.getenv('TOKEN')
ACCOUNT_ID = os.getenv('ACCOUNT_ID')

metaapi = MetaApi(TOKEN)

# Parameter strategi
SYMBOL = 'EURUSD'
GRID_PIPS = 0.0005  # 5 pip
TP_PIPS = 0.0005    # 5 pip
LOT_SIZE = 0.01
CHECK_INTERVAL = 10  # detik

open_positions = []

async def get_price(connection):
    price_data = await connection.get_symbol_price(SYMBOL)
    return float(price_data['bid']), float(price_data['ask'])

async def open_trade(connection, order_type, price):
    try:
        result = await connection.create_market_buy_order(SYMBOL, LOT_SIZE) if order_type == 'buy'             else await connection.create_market_sell_order(SYMBOL, LOT_SIZE)
        open_positions.append({'type': order_type, 'entry': price})
        print(f"[ORDER] {order_type.upper()} {SYMBOL} opened at {price}")
    except Exception as e:
        print(f"[ERROR] Gagal kirim order: {e}")

async def main():
    account = await metaapi.metatrader_account_api.get_account(ACCOUNT_ID)
    await account.deploy()
    await account.wait_connected()

    connection = account.get_rpc_connection()
    await connection.connect()

    print("🟢 EA Hedging Grid aktif...")

    # Inisialisasi dengan 1 Buy dan 1 Sell
    bid, ask = await get_price(connection)
    await open_trade(connection, 'buy', ask)
    await open_trade(connection, 'sell', bid)

    while True:
        bid, ask = await get_price(connection)
        price = (bid + ask) / 2

        new_positions = []

        for pos in open_positions:
            entry = pos['entry']
            if pos['type'] == 'buy' and price - entry >= TP_PIPS:
                print(f"[TP] BUY closed at {price} (+{TP_PIPS} pips)")
            elif pos['type'] == 'sell' and entry - price >= TP_PIPS:
                print(f"[TP] SELL closed at {price} (+{TP_PIPS} pips)")
            else:
                new_positions.append(pos)

        open_positions.clear()
        open_positions.extend(new_positions)

        # Buka buy baru jika tidak ada BUY aktif
        if not any(p['type'] == 'buy' for p in open_positions):
            await open_trade(connection, 'buy', ask)

        # Buka sell baru jika tidak ada SELL aktif
        if not any(p['type'] == 'sell' for p in open_positions):
            await open_trade(connection, 'sell', bid)

        await asyncio.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    asyncio.run(main())
