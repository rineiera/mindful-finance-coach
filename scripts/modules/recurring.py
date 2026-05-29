"""固定账单模块"""
from models import RecurringInput
from modules.store import read_json, write_json, next_id, RECURRING_FILE


def add_recurring(params: dict) -> dict:
    try:
        validated = RecurringInput(**params)
    except Exception as e:
        return {"error": f"固定账单数据校验失败: {str(e)}"}
    recurring = read_json(RECURRING_FILE)
    item = {
        "id": next_id(recurring),
        "item": validated.item,
        "amount": validated.amount,
        "type": validated.type,
        "pocket": validated.pocket,
        "frequency": validated.frequency,
        "emotion_tag": validated.emotion_tag,
        "note": validated.note,
        "active": True,
    }
    recurring.append(item)
    write_json(RECURRING_FILE, recurring)
    return item


def get_recurring(params: dict = None) -> list:
    recurring = read_json(RECURRING_FILE)
    return [r for r in recurring if r.get("active", True)]


def delete_recurring(params: dict) -> dict:
    recurring = read_json(RECURRING_FILE)
    item_id = params.get("id")
    for r in recurring:
        if r["id"] == item_id:
            r["active"] = False
    write_json(RECURRING_FILE, recurring)
    return {"success": True}


COMMANDS = {
    "add_recurring": add_recurring,
    "get_recurring": get_recurring,
    "delete_recurring": delete_recurring,
}
