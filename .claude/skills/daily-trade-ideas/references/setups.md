# Trade Setups, Price Levels, and Scoring

A trade idea is only valid if it maps to one of these setups. "It's a good company" is not
a setup. Each setup defines **entry, stop, and target mechanically**, so "the right price"
comes from structure + volatility, not from a guess.

All levels use daily data. `ATR` = ATR(14).

---

## Long setups

### 1. Breakout (momentum)
- **Conditions:** price within 3% of 20-day or 52-week high; price > SMA50 > SMA200;
  RS vs benchmark positive over 20d; base of at least ~3 weeks.
- **Entry:** buy-stop just above the pivot high (pivot + 0.1×ATR). Only valid if volume
  on the breakout day is ≥ 1.5× average — say so in the plan.
- **Stop:** below the breakout pivot low or entry − 1.5×ATR, whichever is tighter but
  still beyond normal noise (never < 1×ATR).
- **Target:** T1 = entry + 2R; T2 = trail under the 10-day SMA.

### 2. Pullback in uptrend (buy the dip)
- **Conditions:** price > SMA50 > SMA200; pulled back to the EMA21 or SMA50 zone; RSI 40–55
  (cooled off, not broken); declining volume on the pullback.
- **Entry:** limit order in the zone (EMA21 ± 0.25×ATR), or buy above the prior day's high
  once it turns up (more confirmation, worse price).
- **Stop:** below the SMA50 or the pullback low, minus 0.5×ATR.
- **Target:** T1 = recent swing high; T2 = 3R.

### 3. Catalyst gap-and-go
- **Conditions:** gap up > 4% on real news (earnings beat + raise, major contract, upgrade
  cluster); relative volume > 2×; gap not filled in first hour (if checking intraday).
- **Entry:** above the first day's high on day 2, or on a hold of the gap's upper half.
- **Stop:** below the gap-day low (or the midpoint of the gap for tighter risk).
- **Target:** 2R, then trail.

### 4. Oversold bounce (counter-trend — lowest priority)
- Only in Risk-On or Neutral regime, only in names still above SMA200.
- **Conditions:** RSI(14) < 30, price ≥ 2.5×ATR below EMA21, at a prior support level.
- **Entry:** above the prior day's high (wait for the turn — don't catch the knife).
- **Stop:** below the low of the selloff. **Target:** EMA21. Half normal size.

## Short / avoid setups (only if config allows shorts)
- **Breakdown:** mirror of the breakout below 20-day low, price < SMA50 < SMA200, RS negative.
- **Failed rally:** bounce into a falling SMA50 on low volume, RSI 50–60, then a down day.
If shorts are disabled, list these as **"Avoid / reduce exposure"** instead.

---

## Position sizing (always show the math)
```
risk_per_share   = entry − stop
dollar_risk      = account_size × risk_pct          (from config.yaml)
shares           = floor(dollar_risk / risk_per_share)
position_value   = shares × entry   → cap at max_position_pct of account
R:R              = (target − entry) / (entry − stop)
```
Regime scaling: Risk-On = 1.0× risk, Neutral = 0.75×, Risk-Off = 0.5× (and longs only in
the strongest sector, if any).

## Idea quality score (0–10) — rank and cut with this
| Factor | Points |
|---|---|
| Regime aligned with trade direction | 0–2 |
| Sector strong (RS vs SPY positive and ETF above SMA50) | 0–2 |
| Clean setup per definitions above | 0–2 |
| Fresh catalyst / news support in last 72h | 0–2 |
| R:R to T1 ≥ 2.0 | 0–1 |
| No earnings or binary event inside planned hold | 0–1 |

Only present ideas scoring **≥ 6**. If nothing qualifies, the right output is "no trade
today" plus a watchlist — saying so is a feature, not a failure.

## Hard rejects
- Average dollar volume < $20M/day (or < $5M for space names, with half size)
- R:R to T1 < 1.5
- Stop distance < 1×ATR (will get shaken out) or > 4×ATR (size becomes trivial)
- Earnings within the planned hold, unless explicitly flagged as an earnings play
- Price already > 3×ATR above the entry trigger (chasing)
