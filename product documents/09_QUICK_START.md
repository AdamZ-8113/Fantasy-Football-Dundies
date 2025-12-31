# Quick Start (One Page)

## Goal
Pull Yahoo Fantasy data, generate insights, and publish the static site.

## Setup
1) Create venv and install deps:
```
python -m venv .venv
./.venv/Scripts/Activate.ps1
pip install -r requirements.txt
```
2) Copy templates:
```
copy .env.example .env
copy config\config.example.toml config\config.toml
```
3) Fill `.env` with your Yahoo app credentials.

## OAuth
Recommended:
```
python scripts/oauth2_bootstrap.py
```
Fallback:
```
python scripts/oauth_bootstrap.py
```

## Standard data run
```
python scripts/discover_leagues.py
python scripts/sync_all.py
python scripts/backfill_draft_results.py
python scripts/backfill_stat_modifiers.py
python scripts/backfill_roster_injuries.py
python scripts/backfill_player_stats.py
python scripts/backfill_player_points_from_raw.py
python scripts/export_site_data.py
python scripts/export_injury_reports.py
python scripts/generate_insights.py
python scripts/generate_team_insights.py
python scripts/generate_all_seasons_insights.py
```

## Single-season run
Option A: set `season_start` and `season_end` in `config/config.toml`, then run discover + sync.

Option B: target one league key:
```
python scripts/sync_all.py --only <league_key>
python scripts/generate_insights.py --season 2024
python scripts/generate_team_insights.py --season 2024
```

## All Seasons aggregate
```
python scripts/generate_all_seasons_insights.py
```

## Publish
```
git add .
git commit -m "Refresh data"
git push
git subtree push --prefix site origin gh-pages
```

## Verify
- Latest season appears in the picker.
- Team view hides League Overview.
- If behind Cloudflare, purge cache for `index.html` and `app.js`.
