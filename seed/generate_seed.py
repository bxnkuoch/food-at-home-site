import json, sys, uuid
out = open(sys.argv[1], "w")
k = lambda: uuid.uuid4().hex[:12]
def blocks(text):
    if not text: return []
    return [{"_type":"block","_key":k(),"style":"normal","markDefs":[],"children":[{"_type":"span","_key":k(),"text":p,"marks":[]}]} for p in text.split("\n\n")]
def task(title, owners, due, desc="", take="", time=None):
    t={"_type":"task","_key":k(),"title":title,"owners":owners,"dueDate":due}
    if desc: t["description"]=blocks(desc)
    if take: t["takeaways"]=blocks(take)
    if time: t["taskTime"]=time
    return t
def meet(title, date, dur=None, att=None, agenda=""):
    m={"_type":"meeting","_key":k(),"title":title,"date":date}
    if dur: m["duration"]=dur
    if att: m["attendees"]=att
    if agenda: m["agenda"]=blocks(agenda)
    return m
def emit(d): out.write(json.dumps(d)+"\n")
ALL=["All"]
posts=[
 dict(n="01", date="2026-10-14", start="2026-09-07", end="2026-10-14",
  summary="Research, personas, app maps and our tech stack decision (React Native + Expo).",
  closed=[
   task("NUF Analysis",ALL,"2026-09-07","Ranked 15 feature ideas by newness, usefulness and feasibility and narrowed them to 5."),
   task("File Naming & Labeling Reference Manual",["Maria"],"2026-09-24","Naming and labeling conventions across Teams, Figma, Git and Jira."),
   task("Preliminary Book Research",["Fei","Yi Huan","Sreeja"],"2026-09-28","Reviewed 12 articles on food waste, money waste, shared-household conflict and habit motivation."),
   task("Target Audience Research",["Yi Huan"],"2026-09-28","Primary audience: ages 23-34, recent graduates living with roommates. Secondary: ages 18-22."),
   task("Mobile App Research",["Reuben","Ben","Sanjana"],"2026-09-28","Chose React Native with Expo and TestFlight for one iOS/Android codebase."),
   task("Preliminary Research Summary",["Fei"],"2026-09-29"),
   task("User Persona",["Yi Huan"],"2026-09-29"),
   task("Heuristic Evaluation",["Yen","Fei","Sreeja","Yi Huan"],"2026-09-29"),
   task("GitHub Setup",["Reuben"],"2026-10-01"),
   task("Framer Setup",["Sanjana","Ben","Reuben"],"2026-10-01"),
   task("Competitor Analysis",["Sreeja"],"2026-10-01"),
   task("Sitemap",["Maria"],"2026-10-08"),
   task("UX Whiteboard Session",["Maria","Yen"],"2026-10-08"),
   task("App Map",["Yen"],"2026-10-11"),
   task("Journey Map",["Fei"],"2026-10-12"),
   task("User Flow Summary",["Fei"],"2026-10-12"),
   task("Screener Survey Script",["Fei","Yi Huan","Sreeja","Ben"],"2026-10-12"),
   task("Provisional Brand Brief",["Yen","Fei","Sreeja","Maria","Sanjana"],"2026-10-12"),
   task("Revised App Map & Critical Task Identification",ALL,"2026-10-13"),
   task("Status Post Template",["Maria"],"2026-10-14"),
  ],
  open=[task("Task Flow / User Flow",["Yen"],"2026-10-15"),
        task("Mobile conversion: Home",["Ben"],"2026-10-25"),
        task("Mobile conversion: Receipt",["Reuben"],"2026-10-25"),
        task("Mobile conversion: Profile",["Sanjana"],"2026-10-25")],
  new=[task("Screener Survey Data Analysis",["Fei","Yi Huan","Sreeja","Ben"],"2026-10-20"),
       task("Brand Assets",["Yen"],"2026-10-20"),
       task("Low-fi Prototype",["Yen","Sreeja","Fei","Sanjana"],"2026-10-22"),
       task("Inventory and Metrics mobile conversions",["Reuben"],"2026-10-25"),
       task("Brand Identity Testing Script",["Fei","Yi Huan","Sreeja","Ben"],"2026-10-27")],
  meetings=[meet("Meeting with Troy","2026-10-07","30 min",["Yen","Sreeja"]),
            meet("All-Hands","2026-09-24","1.5 hrs"), meet("All-Hands","2026-09-28"),
            meet("All-Hands","2026-10-01"), meet("All-Hands","2026-10-06"),
            meet("All-Hands","2026-10-08"), meet("All-Hands","2026-10-13"),
            meet("Development","2026-10-13")]),
 dict(n="02", date="2026-10-28", start="2026-10-15", end="2026-10-28",
  summary="Critical task flows, wireframes, the lo-fi prototype and our screener survey results.",
  closed=[
   task("Instagram Captions",["Fei"],"2026-10-15"),
   task("Finalize Critical Task Flows",["Yen"],"2026-10-17","Three flows: act on expiring food, add items by scanning a receipt, and build a shopping list from a recipe URL.",time="3.5 hrs"),
   task("Expiration Data Research",["Ben"],"2026-10-20","USDA FoodKeeper is free and covers 650+ foods. Shelf life depends on storage and whether the item is opened.",time="3 hrs"),
   task("Outreach for Lo-Fi Testing",["Fei"],"2026-10-21"),
   task("Volunteer and Interviewee Tracker",["Sreeja"],"2026-10-22"),
   task("Sketches: item details, profile, login/signup",["Maria"],"2026-10-22"),
   task("Wireframes",["Yen"],"2026-10-25",time="9 hrs"),
   task("Mobile conversions: Home, Inventory, Receipt Scanning, Metrics, Profile",["Ben","Reuben","Sanjana"],"2026-10-25"),
   task("Screener Survey Data Analysis",["Fei"],"2026-10-26",time="3 hrs"),
   task("Integrate Interactions & Finalize Lo-Fi Prototype",["Yen"],"2026-10-26",time="5 hrs"),
   task("Internal Walkthrough",ALL,"2026-10-27",time="45 min"),
   task("Lo-Fi Script",["Fei","Yi Huan","Sreeja","Yen"],"2026-10-28"),
  ],
  open=[task("Lo-Fi User Testing",["Fei","Yi Huan","Sreeja","Ben"],"2026-10-30"),
        task("Winter Quarter Timeline",["Maria"],"2026-10-30"),
        task("Social Media Marketing",["Maria","Sreeja","Yi Huan"],"2026-10-30"),
        task("Color Palette Exploration",["Yen"],"2026-10-31"),
        task("Design Multi-User Database Schema",["Reuben"],"2026-11-03")],
  new=[task("Lo-Fi Prototype Findings",[],"2026-11-03"),
       task("Research AI Parsing for Receipt Scans",[],"2026-11-03"),
       task("Build Sign Up and Log In Screens",[],"2026-11-05"),
       task("Build Receipt Parser",[],"2026-11-07"),
       task("Lock Each User's Data (Row Level Security)",[],"2026-11-08"),
       task("Connect Parser to App",[],"2026-11-10")],
  meetings=[meet("All-Hands","2026-10-15"),meet("All-Hands","2026-10-20"),meet("All-Hands","2026-10-22"),
            meet("All-Hands","2026-10-27"),meet("Information Architecture","2026-10-20"),
            meet("Research","2026-10-23"),meet("Development","2026-10-27")]),
 dict(n="03", date="2026-11-11", start="2026-11-01", end="2026-11-11",
  summary="Lo-fi testing results, phone login, AI receipt parsing research and color exploration.",
  closed=[
   task("Low-Fidelity User Testing",["Fei","Yi Huan","Sreeja","Ben"],"2026-11-01"),
   task("Design the Multi-User Database Schema",["Reuben"],"2026-11-03",time="2 hrs"),
   task("Low-Fidelity Prototype Findings",["Fei","Yi Huan","Sreeja","Ben"],"2026-11-03"),
   task("Build the Sign Up and Log In Screens",["Ben"],"2026-11-10","Phone-number login, chosen over email for a lower barrier to entry. No SMS is sent yet.",time="3 hrs"),
   task("Research AI Parsing in Receipt Scans",["Sanjana"],"2026-11-10",time="3.5 hrs"),
   task("Color Exploration",["Yen","Sreeja","Fei","Maria"],"2026-11-08"),
   task("Preference Testing Assets",["Yen"],"2026-11-08"),
   task("Color Preference Survey Script",["Fei","Yi Huan","Sreeja"],"2026-11-11"),
   task("TestFlight Critical Path",["Reuben","Sanjana","Ben"],"2026-11-11"),
   task("Winter Quarter Project Timeline",["Maria","Yi Huan","Reuben"],"2026-11-12"),
  ],
  open=[task("Revise Low-Fidelity Prototype",["Yen","Sreeja","Fei"],"2026-11-14"),
        task("Finalize Character Illustration Style",["Yen","Fei","Sreeja","Sanjana","Maria"],"2026-11-14"),
        task("Color Preference Testing",["Fei","Yi Huan","Sreeja","Ben"],"2026-11-14")],
  new=[task("Connect Parser to App",["Reuben"],"2026-11-12"),
       task("Notification research for native app",["Ben"],"2026-11-13"),
       task("Style Guide",["Yen"],"2026-11-14"),
       task("Color Preference Findings",["Fei"],"2026-11-14"),
       task("Outreach for High-Fi Testing",["Sreeja"],"2026-11-16"),
       task("High-Fidelity Prototype",["Yen","Fei","Sreeja","Maria"],"2026-11-18")],
  meetings=[meet("All-Hands","2026-11-03"),meet("All-Hands","2026-11-05"),meet("All-Hands","2026-11-10"),
            meet("Information Architecture","2026-11-03"),meet("Design","2026-11-08","1.5 hrs")]),
]
TEAM=[("Yi Huan",["Project Manager"]),("Maria",["Project Manager"]),("Yen",["Designer"]),("Fei",["Researcher"]),
      ("Sreeja",["Researcher"]),("Ben",["Developer","Backend & QA"]),("Sanjana",["Developer","AI & Frontend"]),("Reuben",["Developer","GitHub & Supabase"])]
NAMES=[n for n,_ in TEAM]
mid=lambda n:"member-"+n.lower().replace(" ","-")
for i,(n,r) in enumerate(TEAM):
    emit({"_id":mid(n),"_type":"teamMember","name":n,"roles":r,"order":i+1})
def category(title):
    t=title.lower()
    for words,c in [(["github","mobile","testflight","parser","schema","sign up","log in","row level","notification","mobile app research","supabase"],"development"),
                    (["instagram","social","marketing"],"marketing"),(["outreach","volunteer","email"],"outreach"),
                    (["research","survey","testing","findings","persona","audience","analysis","evaluation","script","journey"],"research"),
                    (["timeline","manual","template","sitemap","framer","status"],"planning")]:
        if any(w in t for w in words): return c
    return "design"
def hours(tt):
    if not tt: return None
    import re
    m=re.match(r"([\d.]+)\s*(hr|hrs|h|min)",tt)
    if not m: return None
    v=float(m.group(1)); return round(v/60,2) if m.group(2)=="min" else v
ti=0
for p in posts:
    pid=f"statusPost-{p['n']}"
    emit({"_id":pid,"_type":"statusPost","title":f"Status Post {p['n']}",
       "slug":{"_type":"slug","current":f"status-post-{p['n']}"},"publishedAt":p["date"],
       "periodStart":p["start"],"periodEnd":p["end"],"summary":p["summary"]})
    for status,lst in [("closed",p["closed"]),("open",p["open"]),("new",p["new"])]:
        for t in lst:
            ti+=1
            owners=NAMES if t["owners"]==ALL else t["owners"]
            h=hours(t.get("taskTime"))
            d={"_id":f"task-{ti:03d}","_type":"task","statusPost":{"_type":"reference","_ref":pid},"status":status,
               "title":t["title"],"category":category(t["title"]),"dueDate":t["dueDate"],
               "contributors":[dict({"_type":"contribution","_key":k(),"member":{"_type":"reference","_ref":mid(o)}},**({"hours":h} if h else {})) for o in owners if o in NAMES]}
            if status=="closed": d["finishedDate"]=t["dueDate"]
            for f in ["description","takeaways"]:
                if f in t: d[f]=t[f]
            emit(d)
    for j,m in enumerate(p["meetings"]):
        d={"_id":f"meeting-{p['n']}-{j+1:02d}","_type":"meeting","statusPost":{"_type":"reference","_ref":pid},"title":m["title"],"date":m["date"]}
        if "duration" in m: d["duration"]=m["duration"]
        if "attendees" in m: d["attendees"]=[{"_type":"reference","_ref":mid(a),"_key":k()} for a in m["attendees"] if a in NAMES]
        emit(d)
faqs=[
 ("What is Food at Home?","Food at Home is a mobile app that helps you track the groceries in your kitchen, get reminded before food expires, and see how much you eat versus throw away.",True),
 ("Who is building it?","Team Cronch, a group of eight Drexel students, as our 2026-27 senior design project. Our status posts show what we work on every two weeks.",True),
 ("How do I get the app?","We're in beta on iOS through TestFlight. See the Download page for the invite link.",True),
 ("Can I share an inventory with my roommates?","Yes, that's a core feature we're building: invite roommates to one household with a shared inventory and shopping list.",True),
 ("How are expiration dates estimated?","We use the USDA FoodKeeper data set, which covers 650+ foods and accounts for where you store the item and whether it's been opened. Treat estimates as guidance, not food-safety advice.",True),
 ("What happens to my data?","See our Privacy Policy for what we collect and why.",False),
]
for i,(q,a,h) in enumerate(faqs):
    emit({"_id":f"faq-{i+1}","_type":"faq","question":q,"answer":blocks(a),"showOnHome":h,"order":i+1})
emit({"_id":"siteSettings","_type":"siteSettings","appName":"Food at Home","teamName":"Team Cronch",
 "tagline":"Spend smarter. Waste less.",
 "heroTitle":"Know what's in your kitchen before it goes bad",
 "heroText":"Food at Home helps young adults and shared households track groceries, catch expiring food in time, and build better food habits.",
 "features":[{"_type":"feature","_key":k(),"title":t,"description":d} for t,d in [
   ("Scan your receipt","Snap a grocery receipt and your items land in your inventory."),
   ("Expiration reminders","Shelf-life estimates for 650+ foods, so you use things up in time."),
   ("Chomp & Toss metrics","See what you ate, what you tossed, and where your grocery money went."),
   ("Shared households","Invite roommates and keep one shared inventory and shopping list.")]],
 "downloadNote":"Free beta for iPhone via TestFlight."})
sections=[
 ("Information We Collect","DRAFT, the team must confirm: phone number (for login), the food items, receipts and household details you add, and basic app diagnostics."),
 ("How We Use Your Information","DRAFT: to run the app's features (inventory, expiration reminders, shared households, metrics) and to improve the app."),
 ("Receipt Scanning","DRAFT: receipt images or text are sent to a third-party AI service to read the items. Name the provider and what it retains."),
 ("Where Data Is Stored","DRAFT: data is stored with Supabase, with row-level security so each household only sees its own data."),
 ("Sharing","DRAFT: we don't sell your data. Members of a household you join can see that household's items."),
 ("Deleting Your Data","DRAFT: how a user can delete their account and data."),
 ("Children's Privacy","DRAFT: the app isn't directed at children under 13."),
 ("Changes to This Policy","DRAFT: we'll update the effective date when this policy changes."),
]
emit({"_id":"privacyPolicy","_type":"privacyPolicy","title":"Privacy Policy","effectiveDate":"2026-12-01",
 "intro":blocks("DRAFT. Replace every section with what the app actually does before publishing. This is a student project and this draft is not legal advice."),
 "sections":[{"_type":"policySection","_key":k(),"heading":h,"body":blocks(b)} for h,b in sections]})
