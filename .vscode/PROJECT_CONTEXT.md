# Fantasy Insights - Project Context

Purpose: pull multi-season Yahoo Fantasy Football data, compute awards, and publish a static "Wrapped" site.

Primary flow:
1) OAuth (recommended): python scripts/oauth2_bootstrap.py
2) Discover leagues: python scripts/discover_leagues.py
3) Sync data: python scripts/sync_all.py
4) Backfills (as needed):
   - python scripts/backfill_draft_results.py
   - python scripts/backfill_stat_modifiers.py
   - python scripts/backfill_roster_injuries.py
   - python scripts/backfill_player_stats.py
5) Export site data: python scripts/export_site_data.py
6) Generate insights:
   - python scripts/generate_insights.py
   - python scripts/generate_team_insights.py

Single-season options:
- Set season_start/season_end in config/config.toml, then run discover + sync.
- Or: python scripts/sync_all.py --only <league_key>
- Generate only one season: python scripts/generate_insights.py --season 2024

Frontend:
- Static site in site/ (index.html, styles.css, app.js).
- Data consumed from site/data/*.json.
- Team picker switches to team-specific insights and hides League Overview.

Deployment (GitHub Pages):
- Publish site/ to gh-pages with git subtree:
  git subtree push --prefix site origin gh-pages

Security:
- .env and config/oauth_tokens.json are ignored.
- data/raw, data/processed, and SQLite files are ignored.

Docs:
- README.md (setup + pipeline)
- docs/oauth_setup.md (OAuth)
- docs/DEPLOYMENT.md (publishing)
- docs/AGENT_CONTEXT.md (LLM handoff)
