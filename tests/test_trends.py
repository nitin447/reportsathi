from src.trends import analyze_trend


def test_not_enough_data():
    assert analyze_trend([], "X").direction == "not_enough_data"


def test_stable_values():
    h = [{"value": 90, "low": 70, "high": 99, "status": "normal"} for _ in range(3)]
    assert analyze_trend(h, "Glucose").direction == "stable"


def test_rising_but_still_normal_flags_watch():
    h = [{"value": 88, "low": 70, "high": 99, "status": "normal"},
         {"value": 94, "low": 70, "high": 99, "status": "normal"},
         {"value": 97, "low": 70, "high": 99, "status": "normal"}]
    r = analyze_trend(h, "Glucose")
    assert r.direction == "rising"
    assert r.watch is True


def test_rising_far_from_edge_is_not_watch():
    h = [{"value": 20, "low": 0, "high": 100, "status": "normal"},
         {"value": 30, "low": 0, "high": 100, "status": "normal"},
         {"value": 35, "low": 0, "high": 100, "status": "normal"}]
    r = analyze_trend(h, "X")
    assert r.watch is False


def test_falling_toward_low_edge_flags_watch():
    h = [{"value": 15.0, "low": 12.0, "high": 15.5, "status": "normal"},
         {"value": 13.5, "low": 12.0, "high": 15.5, "status": "normal"},
         {"value": 12.4, "low": 12.0, "high": 15.5, "status": "normal"}]
    r = analyze_trend(h, "Hemoglobin")
    assert r.direction == "falling"
    assert r.watch is True