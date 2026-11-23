"""Build seed/framer-full.ndjson from the team's Framer status posts.

Usage: python3 seed/build-framer.py [cache_dir]
  Fetches the three Framer pages (or reads spNN.html from cache_dir if given),
  converts every task, meeting and reflection to the Sanity schema and writes
  seed/framer-full.ndjson. Images are referenced with `_sanityAsset` so
  `sanity dataset import` uploads them.

Only seed ids (task-NNN, meeting-NN-NN) are reused; new docs get task-pNN-xx /
meeting-pNN-xx ids. seed/framer-delete-ids.txt lists the seed ids not reused.
"""
import difflib
import hashlib
import json
import re
import sys
import urllib.request
from urllib.parse import urljoin
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).parent
BASE = "https://cronch.framer.website/senior-project-status/status-post-"
POSTS = ["01", "02", "03"]

MEMBERS = {
    "yi huan": "member-yi-huan", "maria": "member-maria", "yen": "member-yen", "fei": "member-fei",
    "sreeja": "member-sreeja", "ben": "member-ben", "sanjana": "member-sanjana", "reuben": "member-reuben",
}
ALL = list(MEMBERS.values())
DEV = ["member-reuben", "member-sanjana", "member-ben"]
DESIGN = ["member-yen", "member-fei", "member-sreeja", "member-maria", "member-sanjana"]
RESEARCH = ["member-fei", "member-yi-huan", "member-sreeja", "member-ben"]
TEAMS = {"all": ALL, "dev team": DEV, "design team": DESIGN, "research team": RESEARCH,
         "design & research team": DESIGN + [m for m in RESEARCH if m not in DESIGN]}

# Tasks that appear on a Framer post by mistake (post, title) -> skipped
SKIP = {("01", "TestFlight Critical Path")}

SECTIONS = {"Completed Tasks": "closed", "Open Tasks": "open", "New Tasks": "new"}
REFLECTIONS_H1 = "Systems/What Can We Do More Efficiently"

problems = []  # things we could not map, reported at the end
PAGE_URL = BASE  # set per post; relative links ("../") are resolved against it


def href(a):
    h = a.attrs.get("href", "")
    return urljoin(PAGE_URL, h) if h and not h.startswith(("#", "mailto:")) else ""


# ---------------------------------------------------------------- HTML tree
VOID = {"img", "br", "hr", "meta", "link", "input", "source"}


class Node:
    def __init__(self, tag, attrs, parent):
        self.tag, self.attrs, self.parent, self.children = tag, dict(attrs), parent, []


class TreeBuilder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = self.cur = Node("root", {}, None)

    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs, self.cur)
        self.cur.children.append(n)
        if tag not in VOID:
            self.cur = n

    def handle_endtag(self, tag):
        c = self.cur
        while c is not None and c.tag != tag:
            c = c.parent
        if c is not None and c.parent is not None:
            self.cur = c.parent

    def handle_data(self, d):
        self.cur.children.append(d)


def walk(n):
    yield n
    for c in n.children:
        if not isinstance(c, str):
            yield from walk(c)


def text(n):
    if isinstance(n, str):
        return n
    if n.tag in ("script", "style"):
        return ""
    return "".join(text(c) for c in n.children)


def clean(s):
    return re.sub(r"\s+", " ", s.replace("\xa0", " ")).strip()


# ---------------------------------------------------------- Portable Text
def key(*parts):
    return hashlib.sha1("|".join(map(str, parts)).encode()).hexdigest()[:12]


class PT:
    """Accumulates Portable Text blocks."""

    def __init__(self, ns, alt_ctx):
        self.ns, self.alt_ctx, self.blocks, self.n = ns, alt_ctx, [], 0
        self.images = []  # image urls seen (for counting)
        self.skip_images = False

    def k(self):
        self.n += 1
        return key(self.ns, self.n)

    def image(self, url):
        self.images.append(url)
        alt = f"{self.alt_ctx} (image {len(self.images)})"
        return {"_type": "image", "_key": self.k(), "_sanityAsset": f"image@{url}", "alt": alt}

    def spans(self, nodes, marks=(), mark_defs=None):
        out = []
        for c in nodes:
            if isinstance(c, str):
                if c:
                    out.append({"_type": "span", "_key": self.k(), "text": c.replace("\xa0", " "), "marks": list(marks)})
            elif c.tag in ("strong", "b"):
                out += self.spans(c.children, marks + ("strong",), mark_defs)
            elif c.tag in ("em", "i"):
                out += self.spans(c.children, marks + ("em",), mark_defs)
            elif c.tag == "u":
                out += self.spans(c.children, marks + ("underline",), mark_defs)
            elif c.tag == "code":
                out += self.spans(c.children, marks + ("code",), mark_defs)
            elif c.tag == "a" and href(c).startswith("http"):
                mk = self.k()
                mark_defs.append({"_type": "link", "_key": mk, "href": href(c)})
                out += self.spans(c.children, marks + (mk,), mark_defs)
            elif c.tag == "br":
                out.append({"_type": "span", "_key": self.k(), "text": "\n", "marks": list(marks)})
            elif c.tag in ("img", "script", "style"):
                continue
            else:
                out += self.spans(c.children, marks, mark_defs)
        return out

    def block(self, inline_nodes, style="normal", list_item=None, level=None):
        mark_defs = []
        children = self.spans(inline_nodes, (), mark_defs)
        # trim outer whitespace, drop empty spans
        if children:
            children[0]["text"] = children[0]["text"].lstrip()
            children[-1]["text"] = children[-1]["text"].rstrip()
        children = [s for s in children if s["text"]]
        if not children:
            return
        b = {"_type": "block", "_key": self.k(), "style": style, "markDefs": mark_defs, "children": children}
        if list_item:
            b["listItem"], b["level"] = list_item, level
        self.blocks.append(b)

    def add_nodes(self, nodes, list_item=None, level=0):
        """Add block-level nodes. Inside a list, each <p> becomes a list item."""
        for c in nodes:
            if isinstance(c, str):
                if clean(c):
                    self.block([c], list_item=list_item, level=level or None)
                continue
            if c.tag == "img":
                if not self.skip_images:
                    self.blocks.append(self.image(img_url(c)))
            elif c.tag in ("ul", "ol"):
                li_type = "bullet" if c.tag == "ul" else "number"
                for li in c.children:
                    if isinstance(li, str) or li.tag != "li":
                        continue
                    self.add_li(li, li_type, level + 1)
            elif c.tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
                style = "h4" if not list_item else "normal"
                self.block(c.children, style=style, list_item=list_item, level=level or None)
            elif c.tag == "p":
                self.block(c.children, list_item=list_item, level=level or None)
            elif c.tag in ("div", "section", "blockquote", "figure"):
                self.add_nodes(c.children, list_item, level)
            else:  # stray inline at block level
                self.block([c], list_item=list_item, level=level or None)

    def add_li(self, li, li_type, level):
        inline, rest = [], []
        for c in li.children:
            if isinstance(c, str) or c.tag not in ("ul", "ol", "img"):
                if rest:  # text after a nested list: keep order
                    rest.append(c)
                else:
                    inline.append(c)
            else:
                rest.append(c)
        # an <li> usually wraps one <p>; unwrap paragraphs into separate items
        paras = [c for c in inline if not isinstance(c, str) and c.tag in ("p", "h1", "h2", "h3", "h4")]
        if paras:
            for p in inline:
                if isinstance(p, str):
                    if clean(p):
                        self.block([p], list_item=li_type, level=level)
                else:
                    self.block(p.children if p.tag in ("p", "h1", "h2", "h3", "h4") else [p], list_item=li_type, level=level)
        elif any(clean(text(c)) for c in inline):
            self.block(inline, list_item=li_type, level=level)
        for c in rest:
            if isinstance(c, str):
                continue
            if c.tag == "img":
                if not self.skip_images:
                    self.blocks.append(self.image(img_url(c)))
            elif c.tag in ("ul", "ol"):
                self.add_nodes([c], list_item=li_type, level=level)
            else:
                self.add_nodes([c], list_item=li_type, level=level)


def img_url(n):
    return n.attrs.get("src", "").split("?")[0]


# ------------------------------------------------------------- field parsing
LABEL_RE = re.compile(r"^\s*([A-Za-z][A-Za-z &/()]{1,30}?)\s*:\s*(.*)$", re.S)
FIELD_LABELS = {
    "due date": "due", "task time": "time", "description": "description", "deliverable": "deliverable",
    "deliverables": "deliverable", "takeaways": "takeaways", "takeaway": "takeaways",
    "date & duration": "when", "date": "when", "attendees": "attendees", "agenda": "agenda",
    "location": "location", "notes": "notes",
}


def leading_label(p, labels=FIELD_LABELS):
    """If paragraph p starts with a bold 'Label:' we know, return (field, remaining inline nodes)."""
    t = clean(text(p))
    m = LABEL_RE.match(t)
    if not m or m.group(1).lower().strip() not in labels:
        return None
    field = labels[m.group(1).lower().strip()]
    # strip the label text from the inline nodes
    remaining, to_strip = [], len(m.group(1)) + 1  # label + ':'
    stripped = False
    for c in p.children:
        if stripped:
            remaining.append(c)
            continue
        ct = text(c).replace("\xa0", " ")
        idx = ct.find(":")
        if idx == -1:
            continue  # part of the label
        stripped = True
        rest = ct[idx + 1:]
        if isinstance(c, str):
            remaining.append(rest)
        elif rest.strip():
            # label and value inside the same element (rare): keep as text with same wrapper
            remaining.append(rest)
    return field, remaining


def first_para(li):
    for c in li.children:
        if not isinstance(c, str) and c.tag in ("p", "h3", "h4", "h2"):
            return c
    return None


def parse_item(nodes):
    """nodes = block nodes after an h2. Returns dict field -> list of (inline_nodes, block_nodes)."""
    fields, order = {}, []
    loose = []  # block nodes not under a known label (meeting bodies)
    current = None
    for n in nodes:
        if isinstance(n, str):
            if clean(n):
                loose.append((current, n))
            continue
        if n.tag in ("ul", "ol"):
            unlabelled = []
            for li in n.children:
                if isinstance(li, str) or li.tag != "li":
                    continue
                p = first_para(li)
                lab = leading_label(p) if p is not None else None
                if lab:
                    field, inline = lab
                    current = field
                    others = [c for c in li.children if c is not p]
                    fields.setdefault(field, []).append((inline, others))
                    order.append(field)
                else:
                    unlabelled.append(li)
            if unlabelled:
                fake = Node(n.tag, {}, None)
                fake.children = unlabelled
                loose.append((current, fake))
        else:
            p = n if n.tag in ("p", "h3", "h4") else None
            lab = leading_label(p) if p is not None else None
            if lab:
                current = lab[0]
                fields.setdefault(current, []).append((lab[1], []))
            else:
                loose.append((current, n))
    return fields, loose


def to_pt(entries, ns, alt_ctx, pt=None):
    pt = pt or PT(ns, alt_ctx)
    for inline, blocks in entries:
        if any(clean(text(c)) for c in inline):
            pt.block(inline)
        pt.add_nodes(blocks)
    return pt


def links_in(entries):
    out = []
    for inline, blocks in entries:
        for top in inline + blocks:
            if isinstance(top, str):
                continue
            for a in walk(top):
                if a.tag == "a" and href(a).startswith("http"):
                    out.append((clean(text(a)) or href(a), href(a)))
    return out


def non_link_text(entries):
    """Does a deliverable entry contain text beyond its links?"""
    def strip_links(n):
        if isinstance(n, str):
            return n
        if n.tag == "a" or n.tag == "img":
            return ""
        return "".join(strip_links(c) for c in n.children)
    for inline, blocks in entries:
        if clean("".join(strip_links(c) for c in inline + blocks)).strip(" .,-–|"):
            return True
    return False


def images_in(entries):
    out = []
    for inline, blocks in entries:
        for top in inline + blocks:
            if isinstance(top, str):
                continue
            out += [img_url(i) for i in walk(top) if i.tag == "img"]
    return out


# --------------------------------------------------------------- value parsing
def parse_date(s, last=False):
    ms = re.findall(r"(\d{1,2})/(\d{1,2})/(\d{2,4})", s)
    if not ms:
        return None
    mo, d, y = map(int, ms[-1] if last else ms[0])
    y = y + 2000 if y < 100 else y
    return f"{y:04d}-{mo:02d}-{d:02d}"


def parse_hours(s):
    s = s.replace(" .", ".")
    total, found = 0.0, False
    for num, unit in re.findall(r"(\d+(?:\.\d+)?)\s*(hours?|hrs?|mins?|minutes?)?", s):
        v = float(num)
        if unit and unit.startswith("m"):
            v /= 60
        total += v
        found = True
    return round(total, 2) if found else None


def parse_people(s, ctx):
    ids = []
    for part in re.split(r",|&(?! research)| and ", s):
        name = clean(part).lower().replace("👉", "").replace("👈", "").strip()
        if not name:
            continue
        if name in TEAMS:
            ids += [m for m in TEAMS[name] if m not in ids]
        elif name in MEMBERS:
            if MEMBERS[name] not in ids:
                ids.append(MEMBERS[name])
        else:
            yield_guest = clean(part).replace("👉", "").replace("👈", "").strip()
            ids.append(("guest", yield_guest))
    return ids


def owners_from_title(raw, ctx):
    raw = clean(raw)
    if " - " in raw or "- " in raw:
        title, _, who = raw.rpartition("-")
        title, who = clean(title), clean(who)
        low = who.lower()
        if low in TEAMS:
            return title, list(TEAMS[low])
        people = [p for p in parse_people(who, ctx)]
        guests = [p for p in people if isinstance(p, tuple)]
        if guests:
            problems.append(f"{ctx}: unknown owner(s) {[g[1] for g in guests]} in title")
        return title, [p for p in people if not isinstance(p, tuple)]
    return clean(raw), []


def contributions(owners, time_str, ctx):
    teams = dict(TEAMS, all=owners or ALL)
    hours = {}
    if time_str:
        t = clean(time_str)
        per = re.findall(r"([A-Za-z][A-Za-z ]*?)\s*\(([^)]*)\)", t)
        if per:
            for name, h in per:
                n = name.strip().lower()
                v = parse_hours(h + ("" if re.search(r"[a-z]", h) else " hrs"))
                if n in teams:
                    for m in teams[n]:
                        hours[m] = v
                elif n in MEMBERS:
                    hours[MEMBERS[n]] = v
                else:
                    problems.append(f"{ctx}: task time for unknown person '{name}'")
        else:
            v = parse_hours(t)
            if v is not None:  # one shared time: every person on the task spent that time
                for m in owners:
                    hours[m] = v
    out = []
    for m in owners + [h for h in hours if h not in owners]:
        c = {"_type": "contribution", "_key": key(ctx, m), "member": {"_type": "reference", "_ref": m}}
        if hours.get(m) is not None:
            c["hours"] = hours[m]
        out.append(c)
    return out


def guess_category(title, owners):
    t = title.lower()
    if re.search(r"instagram|social media|marketing|caption", t):
        return "marketing"
    if re.search(r"outreach|email|volunteer|interviewee|recruit|distribution", t):
        return "outreach"
    if re.search(r"timeline|template|naming|status post|project management|placeholder data", t):
        return "planning"
    if set(owners) == set(DESIGN) or re.search(r"sketch|wireframe|prototype|palette|illustration|style guide|brand assets", t):
        return "design"
    if re.search(r"research|survey|testing|category|findings|script|analysis|persona|evaluation|walkthrough|validate|review lo-fi", t):
        return "research"
    if owners and all(o in DEV for o in owners):
        return "development"
    if re.search(r"parser|database|github|framer setup|testflight|mobile|log in|login|sign up|lock each|convert", t):
        return "development"
    return "design"


# ------------------------------------------------------------------- main
def load(n, cache):
    if cache:
        return (Path(cache) / f"sp{n}.html").read_text()
    req = urllib.request.Request(BASE + n, headers={"User-Agent": "Mozilla/5.0"})
    return urllib.request.urlopen(req, timeout=60).read().decode()


def norm(s):
    s = s.lower().replace("lo-fi", "low-fidelity").replace("hi-fi", "high-fidelity").replace("’", "'")
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def main():
    cache = sys.argv[1] if len(sys.argv) > 1 else None
    seed = [json.loads(l) for l in (HERE / "seed.ndjson").read_text().splitlines() if l.strip()]
    seed_by_id = {d["_id"]: d for d in seed}
    seed_tasks = [d for d in seed if d["_type"] == "task" and re.fullmatch(r"task-\d{3}", d["_id"])]
    seed_meetings = [d for d in seed if d["_type"] == "meeting" and re.fullmatch(r"meeting-\d{2}-\d{2}", d["_id"])]
    used, out, report = set(), [], {}

    global PAGE_URL
    for n in POSTS:
        PAGE_URL = BASE + n
        post_id = f"statusPost-{n}"
        b = TreeBuilder()
        b.feed(load(n, cache))
        root = b.root
        rep = report.setdefault(post_id, {"tasks": 0, "meetings": 0, "images": 0, "closed": 0, "open": 0, "new": 0})

        # --- post document (start from the seed doc so summary/period stay)
        post = dict(seed_by_id[post_id])
        tm = next((x for x in walk(root) if x.tag == "time" and x.attrs.get("datetime")), None)
        if tm:
            post["publishedAt"] = tm.attrs["datetime"][:10]
        banner = next((x for x in walk(root) if x.attrs.get("data-framer-name") == "Banner"), None)
        hero = next((x for x in walk(banner) if x.tag == "img"), None) if banner else None
        if hero:
            post["heroImage"] = {"_type": "image", "_sanityAsset": f"image@{img_url(hero)}",
                                 "alt": f"Team Cronch photo for Status Post {n}"}
            rep["images"] += 1

        containers = {x.attrs.get("data-framer-name"): x for x in walk(root)
                      if x.attrs.get("data-framer-component-type") == "RichTextContainer"}

        # --- tasks
        seq = 0
        for cname, status in SECTIONS.items():
            c = containers.get(cname)
            if c is None:
                problems.append(f"{post_id}: no '{cname}' section")
                continue
            items = split_h2(c)
            for raw_title, nodes in items:
                seq += 1
                ctx = f"Post {n} task '{clean(raw_title)}'"
                title, owners = owners_from_title(raw_title, ctx)
                if (n, title) in SKIP:
                    problems.append(f"{ctx}: skipped (listed on this Framer post by mistake)")
                    continue
                fields, loose = parse_item(nodes)
                doc_id = match_id(title, post_id, seed_tasks, used, f"task-p{n}-{seq:02d}")
                old = seed_by_id.get(doc_id, {})
                doc = {"_id": doc_id, "_type": "task", "statusPost": {"_type": "reference", "_ref": post_id},
                       "status": status, "title": title,
                       "category": old.get("category") or guess_category(title, owners)}
                contrib = contributions(owners, flat(fields.get("time")), ctx)
                if contrib:
                    doc["contributors"] = contrib
                due = parse_date(flat(fields.get("due")) or "", last=True)  # "10/27 - 10/30" -> end date
                if due:
                    doc["dueDate"] = due
                    if status == "closed":
                        doc["finishedDate"] = due
                elif fields.get("due"):
                    problems.append(f"{ctx}: due date '{flat(fields.get('due'))}' is not a date; left blank")
                alt = title
                desc = to_pt(fields.get("description", []), doc_id + "d", alt)
                for _f, node in loose:
                    desc.add_nodes([node])
                for f in fields:
                    if f not in ("due", "time", "description", "deliverable", "takeaways"):
                        problems.append(f"{ctx}: unexpected field '{f}' added to description")
                        desc.block(["%s: " % f.title()])
                        to_pt(fields[f], doc_id + f, alt, desc)
                deliv = fields.get("deliverable", [])
                links = links_in(deliv)
                if links:
                    doc["deliverables"] = [{"_type": "link", "_key": key(doc_id, i, u), "label": l, "url": u}
                                           for i, (l, u) in enumerate(links)]
                if deliv and non_link_text(deliv):
                    # keep wording that isn't just a link (instructions, "TBD", etc.) in the description
                    desc.block(["Deliverable:"])
                    desc.blocks[-1]["children"][0]["marks"] = ["strong"]
                    desc.skip_images = True  # deliverable screenshots go to the task's images field
                    to_pt(deliv, doc_id + "dv", alt, desc)
                    desc.skip_images = False
                if desc.blocks:
                    doc["description"] = desc.blocks
                take = to_pt(fields.get("takeaways", []), doc_id + "t", alt)
                if take.blocks:
                    doc["takeaways"] = take.blocks
                d_imgs = images_in(deliv)
                if d_imgs:
                    doc["images"] = [{"_type": "image", "_key": key(doc_id, "img", i), "_sanityAsset": f"image@{u}",
                                      "alt": f"{title} (image {i + 1})"} for i, u in enumerate(d_imgs)]
                rep["images"] += len(d_imgs) + len(desc.images) + len(take.images)
                rep["tasks"] += 1
                rep[status] += 1
                out.append(doc)

        # --- meetings + reflections
        c = containers.get("Meeting")
        mseq = 0
        for raw_title, nodes, kind in split_meetings(c):
            if kind == "reflections":
                pt = PT(post_id + "r", "Reflections")
                pt.add_nodes(nodes)
                post["reflections"] = pt.blocks
                rep["images"] += len(pt.images)
                continue
            title = clean(raw_title)
            fields, loose = parse_item(nodes)
            if not fields and out and out[-1]["_type"] == "meeting":
                prev = out[-1]
                pt = PT(prev["_id"] + "x" + title, f"{prev['title']} meeting {prev.get('date', '')}".strip())
                pt.block([title], style="h4")
                pt.add_nodes(nodes)
                prev.setdefault("agenda", []).extend(pt.blocks)
                rep["images"] += len(pt.images)
                problems.append(f"Post {n}: '{title}' has no date/attendees; added as a sub-section of the previous meeting ('{prev['title']}' {prev.get('date')})")
                continue
            mseq += 1
            ctx = f"Post {n} meeting '{title}' #{mseq}"
            when = flat(fields.get("when")) or ""
            date = parse_date(when)
            doc_id = match_meeting(title, date, post_id, seed_meetings, used, f"meeting-p{n}-{mseq:02d}")
            doc = {"_id": doc_id, "_type": "meeting", "statusPost": {"_type": "reference", "_ref": post_id}, "title": title}
            if date:
                doc["date"] = date
            else:
                problems.append(f"{ctx}: no date found ('{when}')")
            dur = clean(when.split("|", 1)[1]) if "|" in when else ""
            if dur:
                doc["duration"] = dur
            if fields.get("location"):
                doc["location"] = flat(fields["location"])
            people = list(parse_people(flat(fields.get("attendees")) or "", ctx))
            att = [p for p in people if not isinstance(p, tuple)]
            guests = [p[1] for p in people if isinstance(p, tuple)]
            if att:
                doc["attendees"] = [{"_type": "reference", "_key": key(doc_id, m), "_ref": m} for m in att]
            if guests:
                doc["guests"] = guests
            agenda = PT(doc_id + "a", f"{title} meeting {date or ''}".strip())
            take = PT(doc_id + "t", f"{title} meeting {date or ''}".strip())
            to_pt(fields.get("agenda", []), "", "", agenda)
            to_pt(fields.get("notes", []), "", "", agenda)
            to_pt(fields.get("takeaways", []), "", "", take)
            for f in fields:
                if f not in ("when", "attendees", "agenda", "takeaways", "location", "notes"):
                    problems.append(f"{ctx}: unexpected field '{f}' added to agenda")
                    to_pt(fields[f], "", "", agenda)
            for field, node in loose:
                (take if field == "takeaways" else agenda).add_nodes([node])
            if agenda.blocks:
                doc["agenda"] = agenda.blocks
            if take.blocks:
                doc["takeaways"] = take.blocks
            rep["images"] += len(agenda.images) + len(take.images)
            rep["meetings"] += 1
            out.append(doc)

        out.insert(0, post)

    # leftover seed ids
    leftover = sorted(d["_id"] for d in seed_tasks + seed_meetings if d["_id"] not in used)
    (HERE / "framer-full.ndjson").write_text("".join(json.dumps(d, ensure_ascii=False) + "\n" for d in out))
    (HERE / "framer-delete-ids.txt").write_text("\n".join(leftover) + "\n")
    print(json.dumps(report, indent=1))
    print("docs:", len(out), "| seed ids reused:", len(used), "| seed ids to delete:", len(leftover))
    print("\n".join("! " + p for p in problems))


def flat(entries):
    if not entries:
        return None
    return clean(" ".join(clean("".join(text(c) for c in i)) + " " + clean("".join(text(b) for b in bl)) for i, bl in entries))


def split_h2(container):
    items, cur = [], None
    for c in container.children:
        if not isinstance(c, str) and c.tag == "h2":
            cur = (text(c), [])
            items.append(cur)
        elif not isinstance(c, str) and c.tag == "h1":
            continue
        elif cur is not None:
            cur[1].append(c)
    return items


def split_meetings(container):
    items, cur = [], None
    for c in container.children:
        if not isinstance(c, str) and c.tag == "h1":
            if clean(text(c)).startswith("Systems"):
                cur = (text(c), [], "reflections")
                items.append(cur)
            else:
                cur = None
            continue
        if not isinstance(c, str) and c.tag == "h2":
            cur = (text(c), [], "meeting")
            items.append(cur)
        elif cur is not None:
            cur[1].append(c)
    return items


def match_id(title, post_id, seed_tasks, used, fallback):
    best, score = None, 0
    for d in seed_tasks:
        if d["statusPost"]["_ref"] != post_id or d["_id"] in used:
            continue
        r = difflib.SequenceMatcher(None, norm(title), norm(d["title"])).ratio()
        if r > score:
            best, score = d, r
    if best and score >= 0.8:
        used.add(best["_id"])
        return best["_id"]
    return fallback


def match_meeting(title, date, post_id, seed_meetings, used, fallback):
    for d in seed_meetings:
        if d["statusPost"]["_ref"] == post_id and d["_id"] not in used and norm(d["title"]) == norm(title) and d.get("date") == date:
            used.add(d["_id"])
            return d["_id"]
    return fallback


if __name__ == "__main__":
    main()
