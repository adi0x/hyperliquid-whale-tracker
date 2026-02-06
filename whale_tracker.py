import requests
import pandas as pd
import json

url = "https://api.hyperliquid.xyz/info"

# ============================================================
# 1. MARKET OVERVIEW
# ============================================================
response = requests.post(url, json={"type": "metaAndAssetCtxs"})
data = response.json()

meta = data[0]["universe"]
markets = data[1]

parsed = []
for i, coin_info in enumerate(meta):
    m = markets[i]
    mark_price = float(m["markPx"])
    oi_tokens = float(m["openInterest"])
    prev_price = float(m["prevDayPx"])
    
    record = {
        "coin": coin_info["name"],
        "price": mark_price,
        "oi_usd": round(oi_tokens * mark_price),
        "volume_usd": round(float(m["dayNtlVlm"])),
        "funding_pct": round(float(m["funding"]) * 100, 4),
        "change_24h": round((mark_price - prev_price) / prev_price * 100, 2)
    }
    parsed.append(record)

df = pd.DataFrame(parsed)
df = df.sort_values("oi_usd", ascending=False)

pd.set_option('display.float_format', lambda x: f'{x:,.2f}')

print("=" * 70)
print("HYPERLIQUID WHALE TRACKER - LIVE DATA")
print("=" * 70)

print("\n📊 TOP 15 COINS BY OPEN INTEREST:\n")
top15 = df.head(15).copy()
top15["oi_usd"] = top15["oi_usd"].apply(lambda x: f"${x:,.0f}")
top15["volume_usd"] = top15["volume_usd"].apply(lambda x: f"${x:,.0f}")
top15["price"] = top15["price"].apply(lambda x: f"${x:,.2f}")
top15["change_24h"] = top15["change_24h"].apply(lambda x: f"{x:+.2f}%")
top15["funding_pct"] = top15["funding_pct"].apply(lambda x: f"{x:.4f}%")
print(top15.to_string(index=False))

print(f"\nTotal coins: {len(df)}")
print(f"Total open interest: ${df['oi_usd'].sum():,.0f}")
print(f"Total daily volume: ${df['volume_usd'].sum():,.0f}")

# ============================================================
# 2. WHALE POSITIONS - Check specific known whale wallets
# ============================================================
print("\n" + "=" * 70)
print("🐋 WHALE POSITION TRACKER")
print("=" * 70)

# Known whale wallets on Hyperliquid
whale_wallets = [
    "0x5078c2fbea2b2ad61bc840bc023e35fce56bedb6",  # James Wynn
    "0x20c2d95a3dfdca9e9ad12794d5fa6fad99da44f5",  # Famous ETH short whale
]

for wallet in whale_wallets:
    response = requests.post(url, json={
        "type": "clearinghouseState",
        "user": wallet
    })
    state = response.json()
    
    print(f"\nWallet: {wallet[:10]}...")
    
    if "assetPositions" in state and len(state["assetPositions"]) > 0:
        for pos in state["assetPositions"]:
            p = pos["position"]
            size = float(p["szi"])
            entry_px = float(p["entryPx"])
            mark_px = float(p.get("markPx", 0)) if "markPx" in p else 0
            
            # Calculate position value
            coin_name = p["coin"]
            side = "LONG" if size > 0 else "SHORT"
            
            print(f"  {coin_name}: {side} | Size: {abs(size):,.4f} | Entry: ${entry_px:,.2f} | Leverage: {p.get('leverage', {}).get('value', 'N/A')}x")
    else:
        print("  No open positions")

# ============================================================
# 3. EXPORT TO CSV
# ============================================================
df.to_csv("hyperliquid_market_data.csv", index=False)
print("\n✅ Exported to hyperliquid_market_data.csv")
print("=" * 70)