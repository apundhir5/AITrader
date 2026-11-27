#!/usr/bin/env python3
"""Fetch daily OHLCV and compute trading indicators. Standard library only.

Usage:
  python3 scan.py --config ../config.yaml            # full scan from config
  python3 scan.py --tickers NVDA AMD --benchmark SPY # ad-hoc
Outputs JSON to stdout: regime, sectors, stocks (with indicators), errors.
Data source: Yahoo Finance public chart endpoint (unofficial; may be delayed ~15 min).
"""
import argparse, json, math, sys, time, urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor

UA = {"User-Agent": "Mozilla/5.0"}


def fetch(ticker, rng="1y"):
    url = ("https://query1.finance.yahoo.com/v8/finance/chart/"
           f"{urllib.parse.quote(ticker)}?range={rng}&interval=1d&includePrePost=false")
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=15) as r:
                res = json.load(r)["chart"]["result"][0]
            q = res["indicators"]["quote"][0]
            rows = [(t, o, h, l, c, v) for t, o, h, l, c, v in
                    zip(res["timestamp"], q["open"], q["high"], q["low"], q["close"], q["volume"])
                    if None not in (o, h, l, c)]
            return {"meta": res["meta"], "rows": rows}
        except Exception as e:
            err = e
            time.sleep(1 + attempt)
    raise RuntimeError(f"{ticker}: {err}")


def sma(xs, n):
    return sum(xs[-n:]) / n if len(xs) >= n else None


def ema(xs, n):
    if len(xs) < n:
        return None
    k, e = 2 / (n + 1), sum(xs[:n]) / n
    for x in xs[n:]:
        e = x * k + e * (1 - k)
    return e


def rsi(closes, n=14):
    if len(closes) <= n:
        return None
    gains = [max(closes[i] - closes[i - 1], 0) for i in range(1, len(closes))]
    losses = [max(closes[i - 1] - closes[i], 0) for i in range(1, len(closes))]
    ag, al = sum(gains[:n]) / n, sum(losses[:n]) / n
    for g, l in zip(gains[n:], losses[n:]):
        ag, al = (ag * (n - 1) + g) / n, (al * (n - 1) + l) / n
    return 100.0 if al == 0 else 100 - 100 / (1 + ag / al)


def atr(rows, n=14):
    if len(rows) <= n:
        return None
    trs = [max(rows[i][2] - rows[i][3], abs(rows[i][2] - rows[i - 1][4]), abs(rows[i][3] - rows[i - 1][4]))
           for i in range(1, len(rows))]
    a = sum(trs[:n]) / n
    for t in trs[n:]:
        a = (a * (n - 1) + t) / n
    return a


def pct(a, b):
    return None if a is None or not b else round((a / b - 1) * 100, 2)


def ret(closes, n):
    return pct(closes[-1], closes[-1 - n]) if len(closes) > n else None


def r2(x):
    return None if x is None or (isinstance(x, float) and math.isnan(x)) else round(x, 2)


def analyze(ticker, data, bench_closes=None):
    rows = data["rows"]
    closes = [r[4] for r in rows]
    highs, lows, vols = [r[2] for r in rows], [r[3] for r in rows], [r[5] or 0 for r in rows]
    last = closes[-1]
    a = atr(rows)
    avg_vol50 = sma(vols[:-1], 50)
    out = {
        "ticker": ticker,
        "last_date": time.strftime("%Y-%m-%d", time.gmtime(rows[-1][0])),
        "close": r2(last),
        "chg_1d_pct": ret(closes, 1), "chg_5d_pct": ret(closes, 5), "chg_20d_pct": ret(closes, 20),
        "sma10": r2(sma(closes, 10)), "sma20": r2(sma(closes, 20)), "sma50": r2(sma(closes, 50)),
        "sma200": r2(sma(closes, 200)), "ema21": r2(ema(closes, 21)),
        "rsi14": r2(rsi(closes)), "atr14": r2(a), "atr_pct": r2(a / last * 100) if a else None,
        "high_20d": r2(max(highs[-21:-1])) if len(highs) > 21 else None,
        "low_20d": r2(min(lows[-21:-1])) if len(lows) > 21 else None,
        "high_52w": r2(max(highs)), "low_52w": r2(min(lows)),
        "pct_from_52w_high": pct(last, max(highs)), "pct_from_52w_low": pct(last, min(lows)),
        "rel_volume": r2(vols[-1] / avg_vol50) if avg_vol50 else None,
        "avg_dollar_vol_m": r2(avg_vol50 * last / 1e6) if avg_vol50 else None,
        "prev_high": r2(highs[-2]) if len(highs) > 1 else None,
        "prev_low": r2(lows[-2]) if len(lows) > 1 else None,
    }
    s50, s200 = out["sma50"], out["sma200"]
    out["trend"] = ("up" if s50 and s200 and last > s50 > s200 else
                    "down" if s50 and s200 and last < s50 < s200 else "mixed")
    if bench_closes:
        for n in (20, 60):
            sr, br = ret(closes, n), ret(bench_closes, n)
            out[f"rs_{n}d"] = r2(sr - br) if sr is not None and br is not None else None
    return out


def load_config(path):
    import yaml  # only needed with --config
    with open(path) as f:
        return yaml.safe_load(f)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config")
    ap.add_argument("--tickers", nargs="*", default=[])
    ap.add_argument("--benchmark", default="SPY")
    args = ap.parse_args()

    cfg = load_config(args.config) if args.config else {}
    bench = cfg.get("market", {}).get("benchmark", args.benchmark)
    regime = cfg.get("market", {}).get("regime_tickers", [bench])
    sectors = cfg.get("sectors", {})

    wanted = set(regime) | {bench} | set(args.tickers)
    for s in sectors.values():
        wanted |= {s["etf"], *s.get("macro", []), *s.get("tickers", [])}
    wanted |= {p["ticker"] for p in cfg.get("open_positions") or []}

    data, errors = {}, []
    with ThreadPoolExecutor(max_workers=8) as ex:
        for t, res in zip(wanted, ex.map(lambda t: _safe(fetch, t), wanted)):
            (errors.append(res["error"]) if "error" in res else data.__setitem__(t, res))

    bc = [r[4] for r in data[bench]["rows"]] if bench in data else None
    an = {t: analyze(t, d, bc) for t, d in data.items() if len(d["rows"]) > 30}

    out = {
        "generated_utc": time.strftime("%Y-%m-%d %H:%M", time.gmtime()),
        "benchmark": bench,
        "regime": {t: an.get(t) for t in regime},
        "sectors": {name: {"etf": an.get(s["etf"]),
                           "macro": {m: an.get(m) for m in s.get("macro", [])},
                           "stocks": [an[t] for t in s.get("tickers", []) if t in an]}
                    for name, s in sectors.items()},
        "adhoc": [an[t] for t in args.tickers if t in an],
        "open_positions": [an.get(p["ticker"]) for p in cfg.get("open_positions") or []],
        "errors": errors,
    }
    json.dump(out, sys.stdout, indent=1)


def _safe(fn, t):
    try:
        return fn(t)
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    main()
