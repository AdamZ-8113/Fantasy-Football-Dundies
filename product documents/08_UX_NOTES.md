# UX Notes

## Layout
- Hero header with league and season pills on the right.
- Season picker and team picker below hero.
- League Overview section (hidden in team-specific view).
- Awards grouped by category with card layout.
- Playoffs section appears when playoff awards are present.
- Unavailable Awards uses the same header style as other sections (no boxed container).

## Team view
- Team-specific insights should hide the League Overview panel.
- "Team View" badge shows selected team and appears only when a team is selected.
- All Seasons view adds a season chip to each insight.

## Award styling
- Team/manager names should appear as warm badges (chips).
- Player names use neutral badges.
- Metric rows should keep right-aligned values.
- Playoffs cards use wider grid columns and allow badge wrapping.

## Scoring trendline
- Sparkline uses dynamic Y bounds with 10-20 percent padding.
- Tooltip on hover for each week.
- X-axis labels shown for each week.
