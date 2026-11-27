# Sector Playbooks

For each theme: what actually drives the stocks, what to check every day, and the traps.
Read only the sections for the sectors in today's run.

---

## Energy (oil & gas, refiners, services, utilities/power)
- **ETFs:** XLE (integrated/E&P), XOP (E&P, higher beta), OIH (services), XLU (utilities), URA (uranium)
- **Daily drivers:** WTI and Brent crude (CL=F, BZ=F), natural gas (NG=F), weekly EIA
  inventory report (Wednesday 10:30 ET), OPEC+ headlines, Middle East / Russia supply news,
  refinery crack spreads for refiners (VLO, MPC, PSX).
- **Power/AI crossover:** data-center electricity demand drives utilities, nuclear and
  uranium (CEG, VST, NRG, CCJ, OKLO, SMR). These trade more like AI names than like oil.
- **Traps:** E&Ps track crude almost 1:1 — a "great chart" against a falling crude chart
  usually fails. Check crude's trend before any E&P long.

## AI (semiconductors, infrastructure, AI platforms)
- **ETFs:** SMH, SOXX (semis); BOTZ/AIQ (broad AI)
- **Daily drivers:** NVDA as the bellwether; hyperscaler capex commentary (MSFT, GOOGL,
  AMZN, META, ORCL); TSMC monthly sales (~10th of month); chip export-control news;
  memory pricing (MU); networking/optical (AVGO, ANET, MRVL, CRDO, COHR); power and cooling
  (VRT, ETN).
- **Earnings clustering:** NVDA earnings move the whole complex — flag the date for every
  AI idea.
- **Traps:** extremely crowded and high-beta. Use ATR-based stops (these names move 3–5%/day
  routinely). Avoid chasing after 3+ up days with RSI > 75.

## Software (SaaS, cybersecurity, data)
- **ETFs:** IGV, WCLD (cloud), CIBR/HACK (cyber)
- **Daily drivers:** 10Y yield (rising yields compress multiples), earnings/guidance
  (billings, NRR, RPO), "AI winners vs AI losers" narrative (is AI a tailwind or a
  seat-count threat?), M&A rumors.
- **Leaders to watch for tone:** MSFT, CRM, NOW, PLTR, CRWD, PANW, SNOW, DDOG, NET.
- **Traps:** post-earnings gaps of ±15–25% are common; never hold a software swing through
  earnings unless that's the intended trade.

## Space & Defense-tech
- **ETFs:** UFO, ARKX; ITA (aerospace & defense, for context)
- **Daily drivers:** launch schedules and outcomes, NASA/DoD/Space Force contract awards,
  SpaceX news (valuation and launch cadence lift the group), satellite-broadband news,
  government budget headlines.
- **Names:** RKLB, ASTS, LUNR, PL, RDW, BKSY, SPCE (speculative); LMT, NOC, BA (large-cap context).
- **Traps:** many are small, unprofitable, retail-driven and dilute via share offerings —
  check for recent/announced offerings and cash runway. Liquidity filter matters; position
  size smaller (half normal risk is reasonable).

## Adding a new sector
Add it to `config.yaml` with: sector ETF, 8–20 liquid tickers, and 2–4 daily macro drivers.
Then add a short section here following the same pattern: drivers, leaders, traps.
