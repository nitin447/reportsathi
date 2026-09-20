from dataclasses import dataclass


@dataclass
class TrendResult:
    direction: str        # "rising" / "falling" / "stable" / "not_enough_data"
    slope_per_test: float | None
    latest_status: str | None
    watch: bool           # True = normal now, but drifting toward the edge
    message: str


def _slope(xs: list[float], ys: list[float]) -> float:
    n = len(xs)
    mean_x, mean_y = sum(xs) / n, sum(ys) / n
    num = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    den = sum((x - mean_x) ** 2 for x in xs) or 1e-9
    return num / den


def analyze_trend(history: list[dict], test_name: str) -> TrendResult:
    if len(history) < 2:
        return TrendResult("not_enough_data", None, history[-1]["status"] if history else None,
                           False, "Not enough past reports yet to see a trend.")

    ys = [h["value"] for h in history]
    xs = list(range(len(ys)))
    slope = _slope(xs, ys)
    latest = history[-1]
    data_span = max(ys) - min(ys) or 1.0
    rel_slope = slope / data_span

    if abs(rel_slope) < 0.03:
        direction = "stable"
    elif rel_slope > 0:
        direction = "rising"
    else:
        direction = "falling"

    watch = False
    message = f"{test_name} has been {direction} across your last {len(history)} reports."

    low, high = latest["low"], latest["high"]
    range_span = (high - low) if (low is not None and high is not None) else data_span

    if latest["status"] == "normal" and direction != "stable" and (low is not None or high is not None):
        if direction == "rising" and high is not None:
            distance_to_edge = (high - latest["value"]) / range_span
            if distance_to_edge < 0.20:
                watch = True
        if direction == "falling" and low is not None:
            distance_to_edge = (latest["value"] - low) / range_span
            if distance_to_edge < 0.20:
                watch = True
        if watch:
            message = (f"{test_name} is still within the normal range, but it has been steadily "
                       f"{direction} over your last {len(history)} reports and is getting close "
                       f"to the edge of the range. Worth mentioning at your next check-up.")

    return TrendResult(direction, round(slope, 3), latest["status"], watch, message)