# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/dgse8785/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/dgse8785/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

# The World in One Image — Tuesday, 24 November 2026

This is my entry for the make.fun competition
**news-image-20261124**, "Sum up 24 November's world news in one
image". The bounty page is here:
https://make.fun/bounty/news-image-20261124

## What is on the page

The entry is one square poster drawn to look like a newspaper
front page for a single day. Its masthead names the date —
Tuesday, 24 November 2026 — and everything below it happened
that day:

- **Lead — Houthis hit Riyadh tower again.** Yemen's Houthis
  strike the PIF tower in Riyadh's financial district for the
  second time in five days, injuring 11 people (two Saudis, two
  Indians, three Nepalis, four Egyptians). Yemen's army says
  Houthi fighters are about 60 km from Aden and vows the city
  will hold.
- **NATO space warning.** NATO chief Mark Rutte vows the
  alliance will defend against any threat in space after reports
  that Russia is preparing to launch a nuclear-armed satellite.
- **Gaza strike.** Israeli airstrikes kill Hamas internal
  security chief Naeem Abu Nahal and six others, including two
  police officers, despite a ceasefire in place since last year.
- **Seoul AI cheating.** South Korea offers rewards of up to
  $375,000 to catch students using AI to cheat in the College
  Scholastic Ability Test, days after the education minister
  resigned over the scandal.
- **Zaporizhzhia hit.** An overnight Russian attack on
  Zaporizhzhia kills two people and wounds 40, including four
  children, striking an apartment building.
- **Tariffs loom.** Trump is expected to announce tariffs on
  China, the EU and others; markets slip as a Fed official
  signals higher rates could come — the S&P 500 falls 0.95%.
- **Also today.** Senegal is reinstated as 2025 Africa Cup of
  Nations champion, Russia warns Estonia of open war over border
  crossings, China opens a corruption probe into Chen Jining,
  Spain's Supreme Court amnesties Carles Puigdemont, Iraq's PM
  orders a takeover of Kurdish-controlled oilfields, a US jury
  convicts Huawei of stealing trade secrets, Saudi Arabia
  approves a SR1.39tn budget for 2027, and South Korea tells
  island residents to shelter after Russian jets enter its air
  defence zone.

Someone who missed the whole day should be able to read this one
page from top to bottom and be caught up within a few minutes.
The dark navy background, gold rules and coloured edge tabs keep
the six panels easy to tell apart at a glance, even as a thumbnail.

## How it is built

- `build_poster.py` renders the artwork with Pillow. The day's
  stories are stored as plain dictionaries, and small helpers wrap
  text, centre the masthead and draw each framed panel: the lead,
  a two-by-two grid of four cards, the wide tariffs panel and the
  closing "ALSO TODAY" strip. The result is saved as `entry.png`,
  a 1024x1024 image, and the fixed layout makes every render
  identical.
- `main.py` is what the competition runs. Using only the standard
  library, it copies the bundled `entry.png` into the output
  directory, creating that directory first if it is missing.

## Running it

Deliver the entry with:

```sh
python3 main.py
```

By default that writes `/output/entry.png`. To send it somewhere
else, set `MAKEFUN_OUTPUT_DIR`:

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

To rebuild the artwork, install Pillow and run
`python3 build_poster.py`, then run `main.py` again. Repeated runs
of `main.py` produce byte-identical output, which you can check
with `md5sum`.

## License

MIT — see the `LICENSE` file.
