import json
import re
import time
from collections import defaultdict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "site" / "data"
OVERRIDES_PATH = BASE_DIR / "config" / "team_identity_overrides.json"

EVENT_RULES = {
    "soul_crushing_loss": ("min", "margin"),
    "highest_score_loss": ("max", "loser_points"),
    "blowout_victim": ("max", "margin"),
    "peak_week": ("max", "points"),
    "rock_bottom": ("min", "points"),
}


def to_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def normalize_manager_names(raw):
    if not raw:
        return None
    cleaned = str(raw).strip()
    if not cleaned or cleaned.lower() in {"--hidden--", "-- hidden --", "hidden"}:
        return None
    cleaned = re.sub(r"\band\b", ",", cleaned, flags=re.IGNORECASE)
    parts = re.split(r"[,&/]", cleaned)
    names = sorted({p.strip().lower() for p in parts if p.strip()})
    if not names:
        return None
    return "|".join(names)


def load_overrides():
    if not OVERRIDES_PATH.exists():
        return {}
    try:
        return json.loads(OVERRIDES_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def build_team_identity_map():
    leagues_path = OUTPUT_DIR / "leagues.json"
    teams_path = OUTPUT_DIR / "teams.json"
    if not leagues_path.exists() or not teams_path.exists():
        return {}, {}

    leagues = json.loads(leagues_path.read_text(encoding="utf-8"))
    teams = json.loads(teams_path.read_text(encoding="utf-8"))
    league_season = {row["league_key"]: int(row["season"]) for row in leagues if row.get("season")}

    overrides = load_overrides()
    team_overrides = overrides.get("team_overrides", {})

    identity_map = {}
    team_to_identity = {}

    for row in teams:
        team_key = row.get("team_key")
        league_key = row.get("league_key")
        season = league_season.get(league_key, 0)
        manager = row.get("manager_names")
        team_name = row.get("name") or row.get("team_name")

        override = team_overrides.get(team_key)
        identity = None
        display_manager = None
        if isinstance(override, dict):
            identity = override.get("identity")
            display_manager = override.get("display_manager")
        elif isinstance(override, str):
            identity = override

        if not identity:
            identity = normalize_manager_names(manager)

        if not identity:
            identity = f"unknown::{team_key}"

        if not display_manager:
            display_manager = manager if manager and manager.strip() else identity.replace("|", " & ")

        team_to_identity[team_key] = identity
        entry = identity_map.get(identity)
        if not entry:
            identity_map[identity] = {
                "identity": identity,
                "manager_names": display_manager,
                "team_name": team_name,
                "latest_season": season,
                "team_keys": {team_key},
            }
        else:
            entry["team_keys"].add(team_key)
            if season >= entry["latest_season"]:
                entry["latest_season"] = season
                entry["manager_names"] = display_manager
                if team_name:
                    entry["team_name"] = team_name

    return identity_map, team_to_identity


def load_seasons():
    index_path = OUTPUT_DIR / "insights_index.json"
    if not index_path.exists():
        return []
    payload = json.loads(index_path.read_text(encoding="utf-8"))
    seasons = [s for s in payload.get("seasons", []) if s != "all"]
    return sorted(seasons, key=lambda s: int(s))


def add_season(entry, season):
    metric = dict(entry.get("metric", {}))
    metric["season"] = season
    entry = dict(entry)
    entry["metric"] = metric
    entry["_season"] = season
    return entry


def entry_season(entry):
    try:
        return int(entry.get("_season") or 0)
    except ValueError:
        return 0


def score_entry(entry, award_id):
    metric = entry.get("metric", {})
    season = entry_season(entry)

    if award_id == "paper_tiger":
        wins = to_float(metric.get("wins")) or 0
        losses = to_float(metric.get("losses")) or 0
        ties = to_float(metric.get("ties")) or 0
        games = wins + losses + ties
        win_pct = wins / games if games else 0
        avg_points = to_float(metric.get("avg_points")) or 0
        return (win_pct, -avg_points, season)

    if award_id == "league_champion_dna":
        top3 = to_float(metric.get("top3_weeks")) or 0
        avg_points = to_float(metric.get("avg_points")) or 0
        return (top3, avg_points, season)

    if award_id in {"consistent_king"}:
        std_dev = to_float(metric.get("std_dev")) or 0
        return (-std_dev, season)

    if award_id in {"boom_or_bust"}:
        std_dev = to_float(metric.get("std_dev")) or 0
        return (std_dev, season)

    if award_id in {"unluckiest_manager"}:
        return (to_float(metric.get("points_against")) or 0, season)

    if award_id in {"juggernaut"}:
        return (to_float(metric.get("avg_points")) or 0, season)

    if award_id == "schedule_screwed_me":
        return (to_float(metric.get("delta")) or 0, season)

    if award_id == "always_the_bridesmaid":
        avg_margin = to_float(metric.get("avg_margin_loss")) or 0
        return (-avg_margin, season)

    if award_id in {"ride_or_die"}:
        return (-(to_float(metric.get("roster_changes")) or 0), season)

    if award_id in {"fantasy_sicko"}:
        return (to_float(metric.get("roster_changes")) or 0, season)

    if award_id == "waiver_wire_addict":
        return (to_float(metric.get("moves")) or 0, season)

    if award_id == "trade_machine":
        return (to_float(metric.get("trades")) or 0, season)

    if award_id == "draft_loyalist":
        return (to_float(metric.get("percent")) or 0, season)

    if award_id == "commitment_issues":
        return (-(to_float(metric.get("percent")) or 0), season)

    if award_id == "draft_steal":
        return (to_float(metric.get("delta")) or 0, season)

    if award_id == "reached_and_regretted":
        return (-(to_float(metric.get("delta")) or 0), season)

    if award_id == "draft_bust":
        return (-(to_float(metric.get("season_points")) or 0), season)

    if award_id == "late_round_wizardry":
        return (to_float(metric.get("season_points")) or 0, season)

    if award_id == "bench_war_crime":
        return (to_float(metric.get("points")) or 0, season)

    if award_id == "set_and_forget":
        starts = to_float(metric.get("starts")) or 0
        avg_weekly = to_float(metric.get("avg_weekly_score")) or 0
        return (starts, avg_weekly, season)

    if award_id == "overthinker":
        return (to_float(metric.get("games")) or 0, season)

    if award_id == "favorite_player":
        unique = to_float(metric.get("unique_teams")) or 0
        roster = to_float(metric.get("roster_appearances")) or 0
        return (unique, roster, season)

    if award_id == "emotional_support":
        starts = to_float(metric.get("starts")) or 0
        avg_weekly = to_float(metric.get("avg_weekly_score")) or 0
        return (starts, avg_weekly, season)

    if award_id == "why_dont_he_want_me":
        return (to_float(metric.get("bench_points")) or 0, season)

    if award_id == "mid_season_glow_up":
        return (to_float(metric.get("points_diff")) or 0, season)

    if award_id == "late_season_collapse":
        points_diff = to_float(metric.get("points_diff")) or 0
        return (-points_diff, season)

    if award_id == "looked_better_on_paper":
        return (to_float(metric.get("difference")) or 0, season)

    if award_id == "trust_the_process":
        win_pct = to_float(metric.get("first_half_win_pct")) or 0
        return (-win_pct, season)

    if award_id == "well_get_em_next_year":
        return (to_float(metric.get("points_for")) or 0, season)

    if award_id in {"peak_week"}:
        return (to_float(metric.get("points")) or 0, season)

    if award_id in {"rock_bottom"}:
        points = to_float(metric.get("points")) or 0
        return (-points, season)

    return (season,)


def select_best_entry(entries, award_id):
    if award_id in EVENT_RULES:
        mode, key = EVENT_RULES[award_id]
        best = None
        for entry in entries:
            metric = entry.get("metric", {})
            value = to_float(metric.get(key))
            if value is None:
                continue
            if best is None:
                best = entry
                continue
            best_value = to_float(best.get("metric", {}).get(key))
            if best_value is None:
                best = entry
                continue
            if mode == "min" and value < best_value:
                best = entry
            elif mode == "max" and value > best_value:
                best = entry
        return best or entries[0]

    return max(entries, key=lambda entry: score_entry(entry, award_id))


def aggregate_league_insights(seasons):
    all_entries = defaultdict(list)
    missing = []

    for season in seasons:
        path = OUTPUT_DIR / f"insights_{season}.json"
        if not path.exists():
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        for entry in payload.get("insights", []):
            all_entries[entry["id"]].append(add_season(entry, season))

    aggregated = []
    for award_id, entries in all_entries.items():
        best = select_best_entry(entries, award_id)
        if not best:
            continue
        aggregated.append(best)

    return {
        "season": "all",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "insights": aggregated,
        "missing": missing,
    }


def aggregate_team_insights(seasons, identity_map, team_to_identity):
    per_identity = defaultdict(lambda: defaultdict(list))

    for season in seasons:
        path = OUTPUT_DIR / f"insights_{season}_teams.json"
        if not path.exists():
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        for team_entry in payload.get("teams", []):
            team_key = team_entry.get("team_key")
            identity = team_to_identity.get(team_key)
            if not identity:
                continue
            for entry in team_entry.get("insights", []):
                per_identity[identity][entry["id"]].append(add_season(entry, season))

    team_payloads = []
    for identity, awards in per_identity.items():
        meta = identity_map.get(identity, {})
        insights = []
        for award_id, entries in awards.items():
            best = select_best_entry(entries, award_id)
            if not best:
                continue
            best = dict(best)
            best["team"] = {
                "team_key": meta.get("identity", identity),
                "team_name": meta.get("team_name"),
                "manager_names": meta.get("manager_names"),
            }
            insights.append(best)

        team_payloads.append(
            {
                "team_key": f"all::{identity}",
                "team_name": meta.get("team_name"),
                "manager_names": meta.get("manager_names"),
                "insights": insights,
                "missing": [],
            }
        )

    return {
        "season": "all",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "teams": sorted(
            team_payloads,
            key=lambda entry: (entry.get("manager_names") or "", entry.get("team_name") or ""),
        ),
    }


def update_index(seasons):
    index_path = OUTPUT_DIR / "insights_index.json"
    payload = {
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "seasons": ["all"] + seasons,
    }
    index_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {index_path}")


def main():
    seasons = load_seasons()
    if not seasons:
        print("No season insights found. Run generate_insights.py first.")
        return

    identity_map, team_to_identity = build_team_identity_map()
    league_payload = aggregate_league_insights(seasons)
    team_payload = aggregate_team_insights(seasons, identity_map, team_to_identity)

    league_path = OUTPUT_DIR / "insights_all.json"
    league_path.write_text(json.dumps(league_payload, indent=2), encoding="utf-8")
    print(f"Wrote {league_path}")

    team_path = OUTPUT_DIR / "insights_all_teams.json"
    team_path.write_text(json.dumps(team_payload, indent=2), encoding="utf-8")
    print(f"Wrote {team_path}")

    update_index(seasons)


if __name__ == "__main__":
    main()
