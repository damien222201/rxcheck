"""
Static educational content on verifying medication authenticity in Nigeria.

Deliberately general and conservative: we don't claim RxCheck can detect
counterfeits from a description or photo (we can't, reliably), and we
avoid asserting specific technical mechanics (e.g. exact SMS short-codes)
that could go out of date. Instead we point people to NAFDAC's own
official, currently-maintained channels.
"""

VERIFICATION_CHECKLIST = [
    "Buy only from a licensed pharmacy or hospital dispensary — avoid open markets, roadside sellers, or unlicensed online sellers for prescription medication.",
    "Check that the pack has a NAFDAC registration number printed on it. If there's no NAFDAC number at all, treat that as a red flag.",
    "Look for an intact, tamper-evident seal — a broken or missing seal on a sealed product type is a warning sign.",
    "Compare spelling, logo, and packaging quality against a previous pack of the same product if you have one — blurry printing, misspellings, or inconsistent fonts can indicate a fake.",
    "If a product has a scratch-panel or QR-code authentication feature, follow the instructions printed on the pack itself to verify it through the manufacturer's official channel.",
    "If in doubt, ask your pharmacist directly — they deal with this regularly and can often tell you if something looks off.",
    "Report suspected counterfeit or substandard medicine to NAFDAC directly rather than just discarding it, so they can investigate.",
]

NAFDAC_LINKS = {
    "NAFDAC official website": "https://www.nafdac.gov.ng",
    "NAFDAC Green Book (registered products database)": "https://greenbook.nafdac.gov.ng",
}
