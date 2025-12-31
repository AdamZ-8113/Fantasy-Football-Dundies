import argparse
import re
from pathlib import Path

from db import connect_db, init_db, upsert_many
from parse_yahoo_xml import parse_player_stats
from yahoo_client import parse_xml

BASE_DIR = Path(__file__).resolve().parents[1]


def dicts_to_rows(items, columns):
    return [tuple(item.get(col) for col in columns) for item in items]


def iter_raw_responses(conn, season=None, league_key=None):
    query = """
        SELECT season, league_key, endpoint, file_path, body
        FROM raw_responses
        WHERE http_status = 200
          AND endpoint LIKE '%/players;player_keys=%/stats;type=week%'
    """
    params = []
    if season:
        query += " AND season = ?"
        params.append(str(season))
    if league_key:
        query += " AND league_key = ?"
        params.append(league_key)
    return conn.execute(query, params).fetchall()


def extract_week(endpoint):
    match = re.search(r"week=(\d+)", endpoint or "")
    if match:
        return int(match.group(1))
    return None


def load_xml_bytes(file_path, body):
    if file_path:
        path = Path(file_path)
        if path.exists():
            return path.read_bytes()
    if body:
        return body.encode("utf-8", errors="replace")
    return None


def main():
    parser = argparse.ArgumentParser(
        description="Populate player_points totals from stored raw player stats XML."
    )
    parser.add_argument("--season", help="Process only the specified season.")
    parser.add_argument("--only", help="Process only the specified league_key.")
    args = parser.parse_args()

    conn = connect_db()
    init_db(conn)

    total_rows = 0
    rows = iter_raw_responses(conn, season=args.season, league_key=args.only)
    for row in rows:
        endpoint = row[2]
        week = extract_week(endpoint)
        if week is None:
            continue
        xml_bytes = load_xml_bytes(row[3], row[4])
        if not xml_bytes:
            continue
        root = parse_xml(xml_bytes)
        stats_rows, _players = parse_player_stats(root, week)
        points_rows = [r for r in stats_rows if r.get("stat_id") == "player_points"]
        if not points_rows:
            continue
        for point in points_rows:
            point["league_key"] = row[1]
        upsert_many(
            conn,
            "player_stats",
            ("league_key", "player_key", "week", "stat_id", "value"),
            dicts_to_rows(
                points_rows,
                ("league_key", "player_key", "week", "stat_id", "value"),
            ),
        )
        total_rows += len(points_rows)

    print(f"Backfilled player_points rows: {total_rows}")


if __name__ == "__main__":
    main()
