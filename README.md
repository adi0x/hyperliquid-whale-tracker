# Hyperliquid Whale Tracker

Live whale position tracker and market analytics for Hyperliquid, the #1 decentralized perpetuals exchange.

## What it does

- **Live market data** — prices, open interest, volume, funding rates for 228+ coins
- **Whale position tracking** — monitors known whale wallets and their open positions
- **Market overview** — $4.2B total OI, $22B+ daily volume

## Key Findings

- One whale is SHORT 17,614 ETH at 25x leverage (entered at $3,115)
- BTC dominates with $1.4B in open interest
- HYPE token has more OI ($823M) than ETH ($790M)

## Live Dashboard

[View Hyperliquid Whale Tracker on Dune](https://dune.com/adu0x/hyperliquid-whale-tracker)

## How to run

1. Clone this repo
2. `pip install requests pandas`
3. `python whale_tracker.py`

No API key needed — Hyperliquid's API is public.

## Tech Stack

Python, Hyperliquid API, Dune Analytics, SQL
