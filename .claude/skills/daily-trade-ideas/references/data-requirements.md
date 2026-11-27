# Data Requirements

What the skill needs, why, where it comes from, and what to do when it's missing.
Ordered by how much each layer changes the final decision.

Rule of thumb an experienced trader uses: **market regime decides whether to trade,
sector strength decides where, the chart decides when and at what price, news decides
whether the move has a reason to continue, and risk rules decide how much.**

---

## Layer 1 — Market regime (decides IF and HOW AGGRESSIVELY)

| Data | Why it matters | Source |
|---|---|---|
| Benchmark index vs 20/50/200-day MA (SPY, QQQ, IWM) | ~70% of stocks follow the market. Longs in a downtrend fail far more often. | `scripts/scan.py` |
| VIX level and 5-day change | VIX > 25 = wider stops, smaller size; VIX spiking = stand aside on new longs | `scan.py` (^VIX) |
| 10Y yield (^TNX) and US dollar (DX-Y.NYB) trend | Rising yields hit long-duration growth (software, space, unprofitable AI) hardest | `scan.py` |
| Economic calendar today/this week (CPI, PCE, FOMC, NFP, GDP) | Event days produce gaps; avoid opening new swing positions right before them | WebSearch |
| Futures pre-market direction | Sets the opening tone | WebSearch |

Output of this layer: a regime label — **Risk-On / Neutral / Risk-Off** — that scales
how many ideas are allowed and position size (see SKILL.md).

## Layer 2 — Sector / theme strength (decides WHERE)

| Data | Why | Source |
|---|---|---|
| Sector ETF performance 1d / 5d / 20d (XLE, SMH, IGV, UFO/ARKX, etc.) | Money rotates by sector; trade the strongest themes, short/avoid the weakest | `scan.py` |
| Sector ETF relative strength vs SPY | Isolates the sector's own move from the market's | `scan.py` |
| Sector ETF vs its 50-day MA | Simple trend filter | `scan.py` |
| Theme-specific drivers (see `sector-playbooks.md`) | e.g. crude oil for energy, hyperscaler capex for AI | WebSearch |

## Layer 3 — Stock technicals (decides WHEN and AT WHAT PRICE)

Computed by `scripts/scan.py` from ~1 year of daily OHLCV:

| Field | Use |
|---|---|
| Last close, % change 1d/5d/20d | Momentum |
| SMA 10/20/50/200, EMA 21 | Trend structure and pullback-entry levels |
| RSI(14) | Overbought/oversold; momentum divergence |
| ATR(14) and ATR% | **Stop placement and position sizing** — the single most important number for "the right price" |
| 52-week high/low, % from each | Breakout candidates near highs; avoid catching knives near lows |
| 20-day high/low (pivot range) | Breakout trigger / support |
| Relative volume (today vs 50-day avg) | Confirms breakouts; >1.5x = institutional participation |
| Relative strength vs benchmark (20d, 60d) | Leaders outperform in both directions |
| Average dollar volume | Liquidity filter — skip anything under ~$20M/day |

**Not available from the script (gaps to know about):** intraday data, options flow,
short interest, institutional ownership. Get short interest / options context via
WebSearch for finalists only.

## Layer 4 — News and catalysts (decides WHY it should move)

| Data | Why | Source |
|---|---|---|
| Company news last 24–72h | Upgrades, guidance, contracts, FDA-style binary events | WebSearch per finalist |
| **Earnings date** | Holding through earnings is a coin flip with a gap. Flag any idea with earnings inside the planned hold. | WebSearch |
| Analyst rating/price-target changes | Short-term catalyst; clustered upgrades matter more than one | WebSearch |
| Sector news (OPEC, policy, launches, chip export rules, contracts) | Moves the whole group | WebSearch |
| Insider buying (Form 4) | Cluster insider buys are a meaningful signal; selling is mostly noise | WebSearch (openinsider, SEC) |
| Ex-dividend, lockup expiry, secondary offering | Mechanical price pressure | WebSearch |

## Layer 5 — Fundamentals snapshot (sanity check, not the trigger)

For swing trades fundamentals are a filter, not a signal. For each finalist, one line:
revenue growth, profitability (or cash runway for space/early AI names), forward P/E or
EV/Sales vs peers, last earnings beat/miss. Source: WebSearch / company IR.

## Layer 6 — Your personal constraints (decides HOW MUCH) — from `config.yaml`

| Setting | Why |
|---|---|
| Account size and risk per trade (% of account) | Converts a stop distance into a share count |
| Max open positions / max per sector | Prevents five correlated AI trades that are really one bet |
| Holding style (day / swing 2–10 days / position weeks) | Changes timeframe of levels and which setups qualify |
| Long-only or long/short; options allowed? | Filters setups |
| Current open positions | Avoids doubling up; lets the skill review existing trades |

## Layer 7 — Feedback loop (makes the skill better over time)

| Data | Why |
|---|---|
| `journal/YYYY-MM-DD.md` from previous runs | Check what triggered, what hit stop/target. Without this you can't tell if the process works. |
| A running scorecard (win rate, avg R, by setup and sector) | Tells you which setups to keep and which to drop |

---

## Fallback rules when data is missing
- Script fails / no network → do the analysis from WebSearch quotes, mark every level as
  "approximate — verify on your chart", and reduce to max 3 ideas.
- No earnings date found → state "earnings date unverified" on the idea.
- Never invent a price, level, or news item. If it wasn't fetched, say so.
