import json
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler

import requests
from icalendar import Calendar

GROUPS = [
    ("leeds-sharp", "Leeds Sharp (.NET)"),
    ("code-coffee-leeds", "Code & Coffee Leeds"),
    ("pydata-leeds", "PyData Leeds"),
    ("software-crafters-leeds", "Software Crafters Leeds"),
    ("umbleeds", "Umbraco Leeds"),
    ("enable-tech", "EnableTech"),
    ("empowering-women-with-technology", "Women in Tech Leeds"),
]

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}


def fetch_events():
    all_events = []
    failed = []
    for slug, name in GROUPS:
        url = f"https://www.meetup.com/{slug}/events/ical/"
        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            if r.status_code != 200:
                failed.append(name)
                continue
            cal = Calendar.from_ical(r.content)
            for comp in cal.walk("VEVENT"):
                dtstart = comp.get("dtstart")
                all_events.append({
                    "id": str(comp.get("uid")),
                    "title": str(comp.get("summary")),
                    "start": dtstart.dt.isoformat() if dtstart else None,
                    "location": str(comp.get("location")) if comp.get("location") else f"{name} venue, Leeds",
                    "desc": str(comp.get("description"))[:200] if comp.get("description") else f"Hosted by {name}",
                    "url": str(comp.get("url")),
                    "group": name,
                    "slug": slug,
                })
        except Exception:
            failed.append(name)

    all_events.sort(key=lambda e: e["start"] or "")
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "city": "Leeds",
        "event_count": len(all_events),
        "events": all_events,
        "failed_groups": failed,
    }


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self._respond()

    def do_POST(self):
        self._respond()

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def _respond(self):
        data = fetch_events()
        body = json.dumps(data).encode()
        self.send_response(200)
        self._cors()
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
