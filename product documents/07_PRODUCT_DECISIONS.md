# Product Decisions Log

## Data storage
- Keep raw XML snapshots in `data/raw/` for replay and audits.
- Normalize into SQLite (`data/processed/fantasy_insights.sqlite`).

## OAuth
- Prefer OAuth 2.0 for Yahoo; keep OAuth 1.0a as fallback.

## Awards and sections
- Removed: Snatched Victory, Stack Enjoyer, Vulture Victim, Auto Draft Menace, Tinkerer (no longer displayed).
- Added: Always the Bridesmaid, Commitment Issues, Why Don't He Want Me, Man?
- Injury-based award ("Intensive Care Unit") removed from UI for now, data can be revisited later.

## Team-specific insights
- Team picker added.
- Team view hides the League Overview section to focus on manager-specific awards.
- All Seasons picker uses manager identity mapping and shows the latest team name.

## Frontend themes
- Dark theme default with Ember, Glacier, and a Light option.
- Reduced background gradients and removed lens flare effects.

## All seasons aggregation
- Added an "All Seasons" view built from per-season winners.
- Team identity mapping uses manager names with overrides in `config/team_identity_overrides.json`.
- All Seasons insights show a season chip per award.

## Playoffs awards
- Added a dedicated Playoffs section with playoff-only awards.
- Awards use playoff weeks only and remain separate from regular-season awards.

## Deployment
- GitHub Pages with gh-pages branch using git subtree.
- Cloudflare proxy in front of GitHub Pages; cache purges may be needed.
