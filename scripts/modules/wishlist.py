"""心愿单模块（冷静池）"""
from datetime import datetime, timedelta

from models import WishlistInput
from modules.store import read_json, write_json, next_id, WISHLIST_FILE


def add_wishlist(params: dict) -> dict:
    try:
        validated = WishlistInput(**params)
    except Exception as e:
        return {"error": f"心愿单数据校验失败: {str(e)}"}
    wishlist = read_json(WISHLIST_FILE)
    item = {
        "id": next_id(wishlist),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "item": validated.item,
        "amount": validated.amount,
        "pocket": validated.pocket,
        "emotion_tag": validated.emotion_tag,
        "emotion_raw": validated.emotion_raw,
        "status": "waiting",
        "cool_until": (datetime.now() + timedelta(hours=48)).strftime("%Y-%m-%d %H:%M:%S"),
        "note": params.get("note", ""),
    }
    wishlist.append(item)
    write_json(WISHLIST_FILE, wishlist)
    return item


def get_wishlist(params: dict = None) -> list:
    params = params or {}
    status = params.get("status", "")
    wishlist = read_json(WISHLIST_FILE)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    result = []
    for w in wishlist:
        if w["status"] == "waiting" and w.get("cool_until", "") < now:
            w["status"] = "cooled"
        if status and w["status"] != status:
            continue
        result.append(w)
    write_json(WISHLIST_FILE, wishlist)
    return result


def update_wishlist(params: dict) -> dict:
    wishlist = read_json(WISHLIST_FILE)
    item_id = params.get("id")
    target = None
    for w in wishlist:
        if w["id"] == item_id:
            target = w
            break
    if not target:
        return {"error": f"未找到 id={item_id} 的心愿单条目"}
    if "status" in params:
        target["status"] = params["status"]
    write_json(WISHLIST_FILE, wishlist)
    return {"success": True, "updated": target}


COMMANDS = {
    "add_wishlist": add_wishlist,
    "get_wishlist": get_wishlist,
    "update_wishlist": update_wishlist,
}
