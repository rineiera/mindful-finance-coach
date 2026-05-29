"""债务管理模块"""
from datetime import datetime

from models import DebtInput, DebtPaymentInput
from modules.store import (
    read_json, write_json, next_id,
    DEBTS_FILE, DEBT_PAYMENTS_FILE,
)


def add_debt(params: dict) -> dict:
    try:
        validated = DebtInput(**params)
    except Exception as e:
        return {"error": f"债务数据校验失败: {str(e)}"}
    debts = read_json(DEBTS_FILE)
    debt = {
        "id": next_id(debts),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "name": validated.name,
        "total_amount": validated.total_amount,
        "remaining": validated.total_amount,
        "interest_rate": validated.interest_rate,
        "min_payment": validated.min_payment,
        "due_day": validated.due_day,
        "note": validated.note,
        "active": True,
    }
    debts.append(debt)
    write_json(DEBTS_FILE, debts)
    return debt


def get_debts(params: dict = None) -> list:
    debts = read_json(DEBTS_FILE)
    return [d for d in debts if d.get("active", True)]


def update_debt(params: dict) -> dict:
    debts = read_json(DEBTS_FILE)
    debt_id = params.get("id")
    target = None
    for d in debts:
        if d["id"] == debt_id:
            target = d
            break
    if not target:
        return {"error": f"未找到 id={debt_id} 的债务"}
    updatable = ["name", "interest_rate", "min_payment", "due_day", "note"]
    for field in updatable:
        if field in params and params[field] is not None:
            target[field] = params[field]
    write_json(DEBTS_FILE, debts)
    return {"success": True, "updated": target}


def delete_debt(params: dict) -> dict:
    debts = read_json(DEBTS_FILE)
    debt_id = params.get("id")
    for d in debts:
        if d["id"] == debt_id:
            d["active"] = False
    write_json(DEBTS_FILE, debts)
    return {"success": True}


def record_debt_payment(params: dict) -> dict:
    try:
        validated = DebtPaymentInput(**params)
    except Exception as e:
        return {"error": f"还款数据校验失败: {str(e)}"}

    debts = read_json(DEBTS_FILE)
    target = None
    for d in debts:
        if d["id"] == validated.debt_id:
            target = d
            break
    if not target:
        return {"error": f"未找到 id={validated.debt_id} 的债务"}

    target["remaining"] = max(0, target["remaining"] - validated.amount)
    paid_off = target["remaining"] == 0
    if paid_off:
        target["active"] = False
    write_json(DEBTS_FILE, debts)

    payments = read_json(DEBT_PAYMENTS_FILE)
    payment = {
        "id": next_id(payments),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "debt_id": validated.debt_id,
        "debt_name": target["name"],
        "amount": validated.amount,
        "is_extra": validated.is_extra,
        "remaining_after": target["remaining"],
    }
    payments.append(payment)
    write_json(DEBT_PAYMENTS_FILE, payments)

    return {
        "success": True,
        "debt_name": target["name"],
        "paid": validated.amount,
        "remaining": target["remaining"],
        "paid_off": paid_off,
    }


def get_debt_payments(params: dict = None) -> list:
    params = params or {}
    debt_id = params.get("debt_id")
    payments = read_json(DEBT_PAYMENTS_FILE)
    if debt_id:
        payments = [p for p in payments if p["debt_id"] == debt_id]
    return list(reversed(payments))


def debt_summary(params: dict = None) -> dict:
    debts = get_debts()
    if not debts:
        return {"has_debt": False}

    total_original = sum(d["total_amount"] for d in debts)
    total_remaining = sum(d["remaining"] for d in debts)
    total_paid = total_original - total_remaining
    monthly_min = sum(d["min_payment"] for d in debts if d["min_payment"] > 0)

    snowball_order = sorted(debts, key=lambda d: d["remaining"])
    avalanche_order = sorted(debts, key=lambda d: d["interest_rate"], reverse=True)

    months_estimate = 0
    if monthly_min > 0:
        months_estimate = int(total_remaining / monthly_min)

    return {
        "has_debt": True,
        "total_debts": len(debts),
        "total_original": round(total_original, 2),
        "total_remaining": round(total_remaining, 2),
        "total_paid": round(total_paid, 2),
        "paid_ratio": round(total_paid / total_original * 100, 1) if total_original > 0 else 0,
        "monthly_min_payment": round(monthly_min, 2),
        "months_estimate": months_estimate,
        "snowball_order": [{"name": d["name"], "remaining": d["remaining"]} for d in snowball_order],
        "avalanche_order": [{"name": d["name"], "remaining": d["remaining"], "rate": d["interest_rate"]} for d in avalanche_order],
        "debts": [{
            "id": d["id"],
            "name": d["name"],
            "total_amount": d["total_amount"],
            "remaining": d["remaining"],
            "interest_rate": d["interest_rate"],
            "min_payment": d["min_payment"],
            "due_day": d["due_day"],
            "paid_ratio": round((d["total_amount"] - d["remaining"]) / d["total_amount"] * 100, 1) if d["total_amount"] > 0 else 0,
        } for d in debts],
    }


COMMANDS = {
    "add_debt": add_debt,
    "get_debts": get_debts,
    "update_debt": update_debt,
    "delete_debt": delete_debt,
    "record_debt_payment": record_debt_payment,
    "get_debt_payments": get_debt_payments,
    "debt_summary": debt_summary,
}
