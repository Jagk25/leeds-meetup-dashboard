# Leeds Live Meetup Dashboard

A live, publicly hosted dashboard showing upcoming events from verified Leeds tech & community Meetup groups — no API key required.

## Deploy to Vercel (Free, ~60 seconds)
1. Unzip this folder and push to a GitHub repo
2. Go to [vercel.com](https://vercel.com) and sign in with GitHub
3. Click **Add New Project** → import your repo
4. Click **Deploy** — done!

## How It Works
- `/api/sync.py` and `/api/events.py` are Python serverless functions on Vercel
- They fetch real `.ics` calendar feeds from Meetup groups server-side (no CORS issues)
- `public/index.html` is the dashboard UI — zero JS dependencies

## Groups Tracked
- Leeds Sharp (.NET)
- Code & Coffee Leeds
- PyData Leeds
- Software Crafters Leeds
- Umbraco Leeds
- EnableTech
- Women in Tech Leeds

## Add More Groups
Edit the `GROUPS` list in `api/sync.py` and `api/events.py`.

## Tech Stack
- Python 3.12 serverless (Vercel)
- `requests` + `icalendar`
- Vanilla HTML/CSS/JS
