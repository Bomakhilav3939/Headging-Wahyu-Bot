import asyncio
import os
from metaapi_cloud_sdk import MetaApi
from telegram_notifier import send_telegram  # notifikasi

TOKEN = os.getenv('TOKEN')
LOGIN = os.getenv('LOGIN')
PASSWORD = os.getenv('PASSWORD')
SERVER = os.getenv('SERVER')

SYMBOL = 'EURUSD'
GRID_PIPS = float(os.getenv('PIP_SIZE', 0.0005))
TP_PIPS = float(os.getenv('TP_PIPS', 0.0005))
LOT_SIZE = float(os.getenv('LOT_SIZE', 0.01))
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', 10))

metaapi = MetaApi(TOKEN)
open_positions = []

async def get_price(connection):
    price_data = await connection.get_symbol_price(SYMBOL)
    return float(price_data['bid']), float(price_data['ask'])

async def open_trade(connection, order_type, price):
    try:
        result = await connection.create_market_buy_order(SYMBOL, LOT_SIZE) if order_type == 'buy' else await connection.create_market_sell_order(SYMBOL, LOT_SIZE)
        open_positions.append({'type': order_type, 'entry': price})
        msg = f"[ORDER] {order_type.upper()} {SYMBOL} opened at {price}"
        print(msg)
        await send_telegram(msg)
    except Exception as e:
        print(f"[ERROR] Gagal kirim order: {e}")

async def main():
    connection = await metaapi.connect(
        account=LOGIN,
        password=PASSWORD,
        server=SERVER,
        type='cloud-g1',
        application='hedging-bot'
    )
    await connection.connect()

    print("🟢 EA Hedging Grid aktif...")
    await send_telegram("🟢 EA Hedging Grid aktif...")

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
                msg = f"[TP] BUY closed at {price} (+{TP_PIPS} pips)"
                print(msg)
                await send_telegram(msg)
            elif pos['type'] == 'sell' and entry - price >= TP_PIPS:
                msg = f"[TP] SELL closed at {price} (+{TP_PIPS} pips)"
                print(msg)
                await send_telegram(msg)
            else:
                new_positions.append(pos)

        open_positions.clear()
        open_positions.extend(new_positions)

        if not any(p['type'] == 'buy' for p in open_positions):
            await open_trade(connection, 'buy', ask)
        if not any(p['type'] == 'sell' for p in open_positions):
            await open_trade(connection, 'sell', bid)

        await asyncio.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    asyncio.run(main())
