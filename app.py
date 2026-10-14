"""
RxCheck
-------
A drug interaction lookup tool. You enter the names of medications you're
taking, and it shows you the actual FDA-approved label text for each one —
including whether one drug's label specifically mentions another by name
in its interactions/warnings section.

Important design choices, made deliberately for safety:
  - We never compute or invent an interaction "severity" or risk score.
    We only surface real text from FDA-approved drug labels (via the
    openFDA API), clearly cited, so you and your pharmacist/doctor can
    read the actual source.
  - We don't attempt counterfeit detection from a photo or description —
    that's not something that can be done reliably, and false reassurance
    there could cause real harm. Instead, /verify gives NAFDAC's own
    general guidance.
  - This tool is US FDA label data, which won't perfectly match what's
    registered in Nigeria, but drug interaction chemistry/pharmacology
    is the same everywhere — it's a legitimate reference even if the
    specific product registration differs. This is explained on the site.

This is not medical advice. Always confirm with a pharmacist or doctor
before starting, stopping, or combining medications.
"""
from flask import Flask, render_template, request

from fda_client import search_drug_label, find_cross_mentions
from reference_data import VERIFICATION_CHECKLIST, NAFDAC_LINKS

MAX_DRUGS = 5


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_template("index.html", max_drugs=MAX_DRUGS)

    @app.route("/check", methods=["POST"])
    def check():
        raw_names = [request.form.get(f"drug{i}", "").strip() for i in range(1, MAX_DRUGS + 1)]
        drug_names = [n for n in raw_names if n]

        if len(drug_names) < 1:
            return render_template("index.html", max_drugs=MAX_DRUGS, error="Enter at least one drug name.")

        # Look up every drug
        lookups = {}
        for name in drug_names:
            lookups[name] = search_drug_label(name)

        not_found = [name for name, data in lookups.items() if data is None]

        # Build per-drug result cards, including cross-mentions of every other drug
        drug_cards = []
        for name in drug_names:
            data = lookups.get(name)
            if not data or data.get("error"):
                drug_cards.append({"query": name, "found": False, "error": data.get("error") if data else None})
                continue

            cross = []
            for other_name in drug_names:
                if other_name == name:
                    continue
                other_data = lookups.get(other_name)
                mentions = find_cross_mentions(data, other_data)
                if mentions:
                    cross.append({"other_drug": other_name, "excerpts": mentions})

            drug_cards.append({
                "query": name,
                "found": True,
                "display_name": (data.get("brand_names") or data.get("generic_names") or [name])[0],
                "drug_interactions": data.get("drug_interactions", []),
                "warnings": data.get("warnings", []),
                "cross_mentions": cross,
            })

        return render_template(
            "results.html", drug_cards=drug_cards, not_found=not_found,
            drug_count=len(drug_names),
        )

    @app.route("/verify")
    def verify():
        return render_template("verify.html", checklist=VERIFICATION_CHECKLIST, links=NAFDAC_LINKS)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
