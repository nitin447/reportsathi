import json
from datetime import datetime, timezone

from src.auth import get_conn
from src.pipeline import AnalysisResult


def init_reports_table():
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL REFERENCES users(id),
            report_type TEXT NOT NULL,
            report_date TEXT,
            saved_at TEXT NOT NULL,
            values_json TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def save_report(user_id: int, result: AnalysisResult):
    values = [
        {"name": c.name, "value_numeric": None, "unit": c.unit, "status": c.status,
         "low": c.low, "high": c.high}
        for c in result.checked_values if c.status != "not_numeric"
    ]
    # keep the raw numeric value too, pulled from the original extracted values
    raw_by_name = {v.name: v.value_numeric for v in result.report.values}
    for v in values:
        v["value_numeric"] = raw_by_name.get(v["name"])

    conn = get_conn()
    conn.execute(
        "INSERT INTO reports (user_id, report_type, report_date, saved_at, values_json) "
        "VALUES (?, ?, ?, ?, ?)",
        (user_id, result.report.report_type.value, result.report.report_date,
         datetime.now(timezone.utc).isoformat(), json.dumps(values)),
    )
    conn.commit()
    conn.close()


def get_history(user_id: int, test_name: str) -> list[dict]:
    """Returns [{date, value, unit, low, high, status}, ...] sorted oldest first."""
    conn = get_conn()
    rows = conn.execute(
        "SELECT report_date, saved_at, values_json FROM reports WHERE user_id = ? ORDER BY saved_at",
        (user_id,),
    ).fetchall()
    conn.close()

    history = []
    for report_date, saved_at, values_json in rows:
        for v in json.loads(values_json):
            if v["name"] == test_name and v["value_numeric"] is not None:
                history.append({
                    "date": report_date or saved_at[:10],
                    "value": v["value_numeric"], "unit": v["unit"],
                    "low": v["low"], "high": v["high"], "status": v["status"],
                })
    return history


def list_tracked_tests(user_id: int) -> list[str]:
    conn = get_conn()
    rows = conn.execute("SELECT values_json FROM reports WHERE user_id = ?", (user_id,)).fetchall()
    conn.close()
    names = set()
    for (values_json,) in rows:
        for v in json.loads(values_json):
            if v["value_numeric"] is not None:
                names.add(v["name"])
    return sorted(names)


def report_count(user_id: int) -> int:
    conn = get_conn()
    n = conn.execute("SELECT COUNT(*) FROM reports WHERE user_id = ?", (user_id,)).fetchone()[0]
    conn.close()
    return n