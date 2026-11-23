"""Check seed/framer-full.ndjson against the Sanity schema before importing."""
import json
import re
from pathlib import Path

HERE = Path(__file__).parent
docs = [json.loads(l) for l in (HERE / "framer-full.ndjson").read_text().splitlines()]
seed_ids = {json.loads(l)["_id"] for l in (HERE / "seed.ndjson").read_text().splitlines() if l.strip()}
ids = {d["_id"] for d in docs} | seed_ids
errors = []
ALLOWED = {
    "statusPost": {"title", "slug", "publishedAt", "periodStart", "periodEnd", "heroImage", "summary", "reflections"},
    "task": {"statusPost", "status", "title", "category", "contributors", "dueDate", "finishedDate", "estimateHours",
             "description", "deliverables", "takeaways", "images"},
    "meeting": {"statusPost", "title", "date", "duration", "location", "attendees", "guests", "agenda", "takeaways"},
}
CATS = {"design", "research", "development", "marketing", "outreach", "planning"}
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def err(d, msg):
    errors.append(f"{d['_id']}: {msg}")


def ref(d, r, name):
    if not isinstance(r, dict) or r.get("_type") != "reference" and "_ref" not in r:
        err(d, f"{name} is not a reference")
    elif r["_ref"] not in ids:
        err(d, f"{name} points to missing {r['_ref']}")


def image(d, im, name):
    if im.get("_type") != "image" or not str(im.get("_sanityAsset", "")).startswith("image@https://"):
        err(d, f"{name} bad image")


def keys(d, arr, name):
    ks = [x.get("_key") for x in arr]
    if None in ks or len(set(ks)) != len(ks):
        err(d, f"{name} has missing/duplicate _key")


def rich(d, arr, name):
    if not isinstance(arr, list) or not arr:
        err(d, f"{name} empty")
        return
    keys(d, arr, name)
    for b in arr:
        if b["_type"] == "image":
            image(d, b, name)
            continue
        if b["_type"] != "block" or b.get("style") not in ("normal", "h4"):
            err(d, f"{name} bad block {b.get('_type')}/{b.get('style')}")
        if "listItem" in b and (b["listItem"] not in ("bullet", "number") or not isinstance(b.get("level"), int)):
            err(d, f"{name} bad list item")
        keys(d, b["children"], name + ".children")
        mds = {m["_key"] for m in b["markDefs"]}
        for m in b["markDefs"]:
            if m["_type"] != "link" or not m["href"].startswith("http"):
                err(d, f"{name} bad link {m}")
        for s in b["children"]:
            if s["_type"] != "span" or not isinstance(s["text"], str):
                err(d, f"{name} bad span")
            for mk in s["marks"]:
                if mk not in mds and mk not in ("strong", "em", "underline", "code"):
                    err(d, f"{name} unknown mark {mk}")


for d in docs:
    t = d["_type"]
    extra = set(d) - ALLOWED[t] - {"_id", "_type"}
    if extra:
        err(d, f"unknown fields {extra}")
    if not d.get("title"):
        err(d, "missing title")
    if t == "statusPost":
        if not DATE.match(d.get("publishedAt", "")):
            err(d, "publishedAt")
        if "heroImage" in d:
            image(d, d["heroImage"], "heroImage")
        if "reflections" in d:
            rich(d, d["reflections"], "reflections")
        continue
    ref(d, d.get("statusPost"), "statusPost")
    if not re.fullmatch(r"task-\d{3}|task-p\d\d-\d\d|meeting-\d\d-\d\d|meeting-p\d\d-\d\d", d["_id"]):
        err(d, "id outside the allowed seed/new patterns")
    if t == "task":
        if d.get("status") not in ("closed", "open", "new"):
            err(d, "status")
        if d.get("category") not in CATS:
            err(d, "category")
        for f in ("dueDate", "finishedDate"):
            if f in d and not DATE.match(d[f]):
                err(d, f)
        for c in d.get("contributors", []):
            ref(d, c.get("member"), "contributor")
            if "hours" in c and not isinstance(c["hours"], (int, float)):
                err(d, "hours")
        keys(d, d.get("contributors", []), "contributors")
        for l in d.get("deliverables", []):
            if not l.get("label") or not re.match(r"^https?://", l.get("url", "")):
                err(d, f"deliverable {l}")
        keys(d, d.get("deliverables", []), "deliverables")
        for im in d.get("images", []):
            image(d, im, "images")
        keys(d, d.get("images", []), "images")
        for f in ("description", "takeaways"):
            if f in d:
                rich(d, d[f], f)
    else:
        if "date" in d and not DATE.match(d["date"]):
            err(d, "date")
        for a in d.get("attendees", []):
            ref(d, a, "attendee")
        keys(d, d.get("attendees", []), "attendees")
        for f in ("agenda", "takeaways"):
            if f in d:
                rich(d, d[f], f)

dupes = len(docs) - len({d["_id"] for d in docs})
if dupes:
    errors.append(f"{dupes} duplicate _id(s)")
print(f"{len(docs)} docs checked, {len(errors)} problem(s)")
print("\n".join(errors))
