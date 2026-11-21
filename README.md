# THE WORLD TODAY — Saturday, 21 November 2026

[![make.fun](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/rezimx-btc/news-image-20261121-v1/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/rezimx-btc/news-image-20261121-v1/reward.svg)](https://make.fun/bounty/news-image-20261121)

A one-page newspaper front page summing up the world's news of **Saturday, 21 November 2026**, drawn entirely in code (Python 3.13, standard library only — the PNG is encoded by hand with `zlib` + `struct`, and the text uses a 5x7 bitmap font typed inline).

## What is on the page

1. **Russia fires 400+ drones and 110 missiles at Ukraine; 8 killed in Kyiv; 2 missiles and a drone land in Poland** — One Turn, "World news today: AI Stock Rout, Russia Strikes, Genocide Ruling", 21 Nov 2026.
2. **Two Russian missiles and a suspected drone land in south-east Poland; Warsaw calls it a provocation; NATO calls it a grave violation** — One Turn conflict briefing, 21 Nov 2026.
3. **UK and EU sign landmark post-Brexit deal in Brussels: food checks scrapped, carbon markets linked, youth mobility for 100,000 each side** — AP via EuropeSays / CNN, 20–21 Nov 2026.
4. **COP31 climate talks in Antalya run past deadline as nearly 200 nations fail to agree** — One Turn, 21 Nov 2026.
5. **Magnitude 6.8 earthquake centred in Junin, Peru, rattles Lima; no immediate casualties or major damage** — Reuters, 21 Nov 2026.
6. **Israeli strikes kill six in Gaza on Friday; West Bank violence continues** — One Turn conflict briefing, 21 Nov 2026.
7. **South Korea's Supreme Court overturns ex-PM Han Duck-soo's 15-year sentence; retrial ordered** — World News "World in 90 Seconds", 21 Nov 2026.
8. **Suspected gas explosion partly collapses a Tbilisi apartment block; six dead including a child** — World News "World in 90 Seconds", 21 Nov 2026.
9. **Saudi-led coalition intercepts three Houthi missiles aimed at Riyadh after a strike damaged the PIF tower** — World News "World in 90 Seconds" / ApexWire, 21 Nov 2026.
10. **AI sell-off: S&P 500 down 3.7% into correction, Nasdaq down 5.3%, Nikkei down 5.06%, gold down 3.98%, Bitcoin below $58,000** — One Turn markets, 21 Nov 2026.
11. **Also today: Bukele to seek a third term in El Salvador; US court lets Trump end TPS for 600,000 Venezuelans; pancreatic-cancer pill makes tumours undetectable in 1 in 12 patients; Gen Z protests in 25 European countries; Alcaraz unbeaten at the ATP Finals; Trump–Xi–Putin summit ends with a joint declaration** — One Turn / World News, 21 Nov 2026.

## How to run

```sh
MAKEFUN_OUTPUT_DIR=out python3 -S main.py
```

Writes `out/entry.png` (1024x1024, under 1 MiB). Deterministic: two runs produce byte-identical output.
