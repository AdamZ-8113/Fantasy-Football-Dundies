# Data Pipeline and Scripts

## Required config
`.env`:
- YAHOO_CONSUMER_KEY
- YAHOO_CONSUMER_SECRET
- YAHOO_OAUTH_REDIRECT_URI
- YAHOO_OAUTH_SCOPE (default: fspt-r)

`config/config.toml`:
- game_key (nfl)
- season_start / season_end
- league_name_hint / league_id_hint
- league_filter_mode

## OAuth
Recommended:
```
python scripts/oauth2_bootstrap.py
```
Fallback:
```
python scripts/oauth_bootstrap.py
```

## Standard run order
1) Discover leagues
```
python scripts/discover_leagues.py
```
2) Sync data
```
python scripts/sync_all.py
```
3) Backfills (run as needed)
```
python scripts/backfill_draft_results.py
python scripts/backfill_stat_modifiers.py
python scripts/backfill_roster_injuries.py
python scripts/backfill_player_stats.py
python scripts/backfill_player_points_from_raw.py
```
4) Export site data
```
python scripts/export_site_data.py
python scripts/export_injury_reports.py
```
5) Generate insights
```
python scripts/generate_insights.py
python scripts/generate_team_insights.py
python scripts/generate_all_seasons_insights.py
```

## Single-season workflows
Option A: edit `config/config.toml` and set:
```
season_start = 2024
season_end = 2024
```
Then run discover + sync.

Option B: sync only a league key:
```
python scripts/sync_all.py --only <league_key>
```

Generate insights for a single season:
```
python scripts/generate_insights.py --season 2024
python scripts/generate_team_insights.py --season 2024
```

Generate all-seasons aggregate view:
```
python scripts/generate_all_seasons_insights.py
```

## Notes
- `backfill_player_points_from_raw.py` populates `player_points` totals from saved XML.
  This is needed for older seasons where stat breakdown values are zero but Yahoo includes
  a `player_points` total.
- All-seasons aggregation uses a stable team identity map. Update
  `config/team_identity_overrides.json` if managers changed display names.

## Helpful flags
- `sync_all.py --skip-existing`: skips leagues with existing data
- `sync_all.py --resume`: continue after last saved league
