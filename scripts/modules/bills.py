"""账单模块：CRUD + 拆分记账"""
from datetime import datetime

from models import BillInput, SplitItem
from modules.store import (
    read_json, write_json, next_id, period_range,
    BILLS_FILE,
)


def add_bill(params: dict) -> dict:
    try:
        validated = BillInput(**params)
    except Exception as e:
        return {"error": f"账单数据校验失败: {str(e)}"}

    params = validated.model_dump()
    bills = read_json(BILLS_FILE)
    splits = params.get("splits")

    if splits:
        results = []
        parent_note = params.get("item", "")
        for split in splits:
            try:
                sv = SplitItem(**split).model_dump()
            except Exception as e:
                return {"error": f"拆分项校验失败: {str(e)}"}
            bill = {
                "id": next_id(bills),
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "item": sv.get("item", ""),
                "amount": sv["amount"],
                "type": params.get("type", "expense"),
                "pocket": sv["pocket"],
                "emotion_tag": sv.get("emotion_tag", ""),
                "emotion_sub_tag": sv.get("emotion_sub_tag", ""),
                "emotion_raw": sv.get("emotion_raw", params.get("emotion_raw", "")),
                "note": f"拆自: {parent_note}",
            }
            bills.append(bill)
            results.append(bill)
        write_json(BILLS_FILE, bills)
        return {"success": True, "split_count": len(results), "bills": results}
    else:
        bill = {
            "id": next_id(bills),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "item": params.get("item", ""),
            "amount": params["amount"],
            "type": params.get("type", "expense"),
            "pocket": params["pocket"],
            "emotion_tag": params.get("emotion_tag", ""),
            "emotion_sub_tag": params.get("emotion_sub_tag", ""),
            "emotion_raw": params.get("emotion_raw", ""),
            "note": params.get("note", ""),
        }
        bills.append(bill)
        write_json(BILLS_FILE, bills)
        return bill


def delete_bill(params: dict) -> dict:
    bill_id = params.get("id")
    bills = read_json(BILLS_FILE)
    target = None
    for b in bills:
        if b["id"] == bill_id:
            target = b
            break
    if not target:
        return {"error": f"未找到 id={bill_id} 的账单"}
    bills = [b for b in bills if b["id"] != bill_id]
    write_json(BILLS_FILE, bills)
    return {"success": True, "deleted": target}


def update_bill(params: dict) -> dict:
    bill_id = params.get("id")
    bills = read_json(BILLS_FILE)
    target = None
    for b in bills:
        if b["id"] == bill_id:
            target = b
            break
    if not target:
        return {"error": f"未找到 id={bill_id} 的账单"}
    updatable_fields = ["item", "amount", "type", "pocket", "emotion_tag",
                        "emotion_sub_tag", "emotion_raw", "note"]
    for field in updatable_fields:
        if field in params and params[field] is not None:
            target[field] = params[field]
    write_json(BILLS_FILE, bills)
    return {"success": True, "updated": target}


def get_bills(params: dict = None) -> list:
    params = params or {}
    start_date = params.get("start_date", "")
    end_date = params.get("end_date", "")
    pocket = params.get("pocket", "")
    bill_type = params.get("type", "")
    limit = params.get("limit", 100)

    bills = read_json(BILLS_FILE)
    result = []
    for b in reversed(bills):
        if start_date and b["created_at"] < start_date:
            continue
        if end_date and b["created_at"] > end_date:
            continue
        if pocket and b["pocket"] != pocket:
            continue
        if bill_type and b["type"] != bill_type:
            continue
        result.append(b)
        if len(result) >= limit:
            break
    return result


def get_bills_by_period(params: dict = None) -> list:
    params = params or {}
    period = params.get("period", "month")
    start, end = period_range(period)
    return get_bills({"start_date": start, "end_date": end, "limit": 1000})


COMMANDS = {
    "add_bill": add_bill,
    "delete_bill": delete_bill,
    "update_bill": update_bill,
    "get_bills": get_bills_by_period,
}
