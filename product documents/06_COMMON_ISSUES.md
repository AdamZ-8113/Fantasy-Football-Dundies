# Common Issues and Fixes

## OAuth 401 / Forbidden
Likely cause: OAuth 1.0a rejected by Yahoo.
Fix: Use OAuth 2.0 flow:
```
python scripts/oauth2_bootstrap.py
```

Other checks:
- Redirect URI must match app settings exactly.
- Use Client ID (Consumer Key) and Client Secret from the same app.
- App ID is not used.
- System clock must be accurate.
- Scope should be `fspt-r` and Fantasy Sports (Read) must be enabled.

## Tokens missing
If `config/oauth_tokens.json` is missing, API calls will fail.
Re-run OAuth bootstrap.

## 400 errors during sync
Some weeks may be out of range for older seasons.
Re-run with `--skip-existing` and continue if data already present.

## Windows path length errors
Raw XML file names can be long. The project now uses hashed names to avoid path length errors.

## Site not updating
If GitHub Pages is behind Cloudflare:
- purge Cloudflare cache
- verify the raw GH Pages content is updated first

## Older seasons show zero player points
Yahoo sometimes returns zeroed stat breakdowns but includes `player_points`.
Fix:
```
python scripts/backfill_player_points_from_raw.py
python scripts/generate_insights.py
python scripts/generate_team_insights.py
```

## Missing teams in All Seasons picker
All Seasons uses manager identity mapping, so historic team names roll into a single picker entry.
Update `config/team_identity_overrides.json` if a manager name changed or is hidden.

## Custom domain returns 404
Ensure `site/CNAME` exists and matches the live domain, then re-publish `gh-pages`.
