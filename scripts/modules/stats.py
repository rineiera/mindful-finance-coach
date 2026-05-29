"""统计模块：汇总、环比、情绪分析"""
from modules.store import (
    read_json, previous_period_range,
    BILLS_FILE, MOODS_FILE, BUDGETS_FILE, WISHLIST_FILE, RECURRING_FILE,
)
from modules.bills import get_bills, get_bills_by_period
from modules.moods import get_moods


def get_pocket_summary(params: dict = None) -> list:
    params = params or {}
    period = params.get("period", "month")
    bills = get_bills_by_period({"period": period})
    summary = {}
    for b in bills:
        if b["type"] != "expense":
            continue
        pocket = b["pocket"]
        if pocket not in summary:
            summary[pocket] = {"total": 0, "count": 0, "items": []}
        summary[pocket]["total"] += b["amount"]
        summary[pocket]["count"] += 1
        summary[pocket]["items"].append(b["item"])

    total_expense = sum(s["total"] for s in summary.values())
    result = []
    for pocket, data in summary.items():
        result.append({
            "pocket": pocket,
            "total": round(data["total"], 2),
            "count": data["count"],
            "ratio": round(data["total"] / total_expense * 100, 1) if total_expense > 0 else 0,
        })
    return result


def get_pocket_comparison(params: dict = None) -> list:
    params = params or {}
    period = params.get("period", "month")
    current = get_pocket_summary({"period": period})
    prev_start, prev_end = previous_period_range(period)
    prev_bills = get_bills({"start_date": prev_start, "end_date": prev_end, "type": "expense"})

    prev_summary = {}
    for b in prev_bills:
        pocket = b["pocket"]
        if pocket not in prev_summary:
            prev_summary[pocket] = 0
        prev_summary[pocket] += b["amount"]

    result = []
    for c in current:
        pocket = c["pocket"]
        prev_amount = round(prev_summary.get(pocket, 0), 2)
        change = round(c["total"] - prev_amount, 2)
        change_pct = round(change / prev_amount * 100, 1) if prev_amount > 0 else None
        result.append({
            "pocket": pocket,
            "current": c["total"],
            "previous": prev_amount,
            "change": change,
            "change_pct": f"{change_pct}%" if change_pct is not None else "N/A",
        })
    return result


def get_emotion_summary(params: dict = None) -> list:
    params = params or {}
    period = params.get("period", "month")
    bills = get_bills_by_period({"period": period})
    moods = get_moods({"period": period})

    emotion_map = {}
    for b in bills:
        if not b.get("emotion_tag"):
            continue
        tag = b["emotion_tag"]
        if tag not in emotion_map:
            emotion_map[tag] = {"count": 0, "total_spent": 0, "pockets": {}, "from_mood": 0}
        emotion_map[tag]["count"] += 1
        emotion_map[tag]["total_spent"] += b["amount"]
        pocket = b["pocket"]
        if pocket not in emotion_map[tag]["pockets"]:
            emotion_map[tag]["pockets"][pocket] = 0
        emotion_map[tag]["pockets"][pocket] += b["amount"]

    for m in moods:
        if not m.get("emotion_tag"):
            continue
        tag = m["emotion_tag"]
        if tag not in emotion_map:
            emotion_map[tag] = {"count": 0, "total_spent": 0, "pockets": {}, "from_mood": 0}
        emotion_map[tag]["count"] += 1
        emotion_map[tag]["from_mood"] += 1

    result = []
    for tag, data in emotion_map.items():
        result.append({
            "emotion": tag,
            "count": data["count"],
            "total_spent": round(data["total_spent"], 2),
            "from_mood": data["from_mood"],
            "pockets": {k: round(v, 2) for k, v in data["pockets"].items()},
        })
    result.sort(key=lambda x: x["count"], reverse=True)
    return result


def get_emotion_pocket_correlation(params: dict = None) -> list:
    params = params or {}
    period = params.get("period", "month")
    bills = get_bills_by_period({"period": period})
    data_map = {}
    for b in bills:
        if not b.get("emotion_tag"):
            continue
        key = (b["emotion_tag"], b["pocket"])
        if key not in data_map:
            data_map[key] = {"amounts": [], "items": []}
        data_map[key]["amounts"].append(b["amount"])
        data_map[key]["items"].append(b["item"])

    result = []
    for (emotion, pocket), data in data_map.items():
        avg = sum(data["amounts"]) / len(data["amounts"])
        result.append({
            "emotion": emotion,
            "pocket": pocket,
            "frequency": len(data["amounts"]),
            "total": round(sum(data["amounts"]), 2),
            "avg": round(avg, 2),
            "sample_items": data["items"][:5],
        })
    result.sort(key=lambda x: x["frequency"], reverse=True)
    return result


def get_emotion_roi(params: dict = None) -> list:
    params = params or {}
    period = params.get("period", "month")
    bills = get_bills_by_period({"period": period})
    joy_bills = [b for b in bills
                 if b.get("emotion_tag") == "愉悦"
                 and b["pocket"] == "悦己的钱"
                 and b["type"] == "expense"]
    return [{
        "id": b["id"],
        "item": b["item"],
        "amount": b["amount"],
        "emotion_raw": b.get("emotion_raw", ""),
        "created_at": b["created_at"],
    } for b in joy_bills]


def get_overview(params: dict = None) -> dict:
    bills = read_json(BILLS_FILE)
    moods = read_json(MOODS_FILE)
    budgets = read_json(BUDGETS_FILE)
    wishlist = read_json(WISHLIST_FILE)
    recurring = read_json(RECURRING_FILE)
    has_budget = any(b.get("monthly_budget", 0) > 0 for b in budgets)
    pending_wishes = [w for w in wishlist if w.get("status") == "waiting"]
    cooled_wishes = [w for w in wishlist if w.get("status") == "cooled"]
    active_recurring = [r for r in recurring if r.get("active", True)]
    return {
        "total_bills": len(bills),
        "total_moods": len(moods),
        "has_budget_set": has_budget,
        "is_new_user": len(bills) == 0 and len(moods) == 0,
        "pending_wishes": len(pending_wishes),
        "cooled_wishes": len(cooled_wishes),
        "active_recurring_bills": len(active_recurring),
    }


COMMANDS = {
    "summary": get_pocket_summary,
    "comparison": get_pocket_comparison,
    "emotion_summary": get_emotion_summary,
    "correlation": get_emotion_pocket_correlation,
    "emotion_roi": get_emotion_roi,
    "overview": get_overview,
}
