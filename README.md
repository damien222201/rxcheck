# RxCheck

A drug interaction lookup tool. Enter the names of medications you're taking, and see the actual FDA-approved label text for each — including whether one drug's label specifically mentions another by name in its interactions or warnings section.

**This is not medical advice.** Always confirm with a pharmacist or doctor before starting, stopping, or combining medications.

## Design choices made deliberately for safety

This is the most safety-sensitive project in the series, so it's built differently from a typical "AI does the analysis" tool:

- **No invented severity or risk scores.** RxCheck never computes, guesses, or rates how dangerous an interaction is. It only pulls and displays the actual text from FDA-approved drug labels (via the free, public [openFDA API](https://open.fda.gov/apis/drug/label/)), clearly attributed, so you and your pharmacist can read the real source and make the judgment call.
- **No counterfeit detection from a photo or description.** That's not something that can be done reliably without lab testing, and false reassurance there could cause real harm. Instead, the `/verify` page gives NAFDAC's own general, conservative guidance and links to their official resources — nothing invented.
- **US FDA label data, used as a pharmacological reference.** openFDA only covers US-approved labels, which won't always match what's registered in Nigeria. Drug interaction chemistry is the same everywhere a given active ingredient is used, so this is still a legitimate reference — but the site is upfront that you should confirm specifics for your actual product with a pharmacist.
- **The "not medical advice" disclaimer is a permanent part of the layout**, not a one-time popup — it's visible on every page.

## How it works

1. Enter 1–5 drug names (brand or generic).
2. RxCheck looks each one up against openFDA's drug label database.
3. For each drug found, it shows the full "drug interactions" and "warnings" sections from its official label.
4. If another drug you entered is mentioned by name in one drug's interaction/warnings text, that's flagged separately with the exact excerpt — pure text matching against real label content, nothing inferred.

## Tech stack

Flask + `requests`, no database (this is a stateless lookup tool, not crowdsourced data like the other projects in this series). Deployed on Render's free tier.

## Running locally

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Visit `http://localhost:5000`. No API keys or environment variables needed — openFDA's label API is free and keyless.

## Deploying to Render

Push to GitHub, then create a Web Service from the repo (build command `pip install -r requirements.txt`, start command `gunicorn app:app`) — or use the included `render.yaml` blueprint. No database to set up.

## Project structure

```
app.py              # routes + app factory
fda_client.py        # openFDA lookup + cross-mention text matching
reference_data.py    # NAFDAC verification checklist (static content)
templates/            # index, results, verify pages + shared base layout
static/style.css      # all styling
```

## Known limitations

- **Name matching depends on openFDA's data quality.** Misspelled or very obscure drug names may not resolve. Nigerian brand names that differ from US brand names won't match directly — searching by generic/active-ingredient name works best.
- **Cross-mention detection is text matching, not clinical judgment.** A drug's label might describe a real interaction without using the other drug's exact name (e.g. referring to a drug class instead), which this tool won't catch. It surfaces what's explicitly there — it doesn't infer what isn't.
- **Not exhaustive.** Always tell your pharmacist or doctor everything you're taking, including OTC drugs and supplements — this tool is a starting reference, not a substitute for that conversation.

## License

MIT — see [LICENSE](LICENSE).
