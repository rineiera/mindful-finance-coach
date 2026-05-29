"""预算模块：设置、查询、使用率"""
from datetime import datetime

from models import BudgetInput
from modules.store import (
    read_json, write_json,
    BUDGETS_FILE, BILLS_FILE,
)
from modules.bills import get_bills


def init_budgets():
    budgets = read_json(BUDGETS_FILE)
    if not budgets:
        default = [
            {"pocket": "要命的钱", "monthly_budget": 0},
            {"pocket": "保命的钱", "monthly_budget": 0},
            {"pocket": "生钱的钱", "monthly_budget": 0},
            {"pocket": "悦己的钱", "monthly_budget": 0},
        ]
        write_json(BUDGETS_FILE, default)


def set_budget(params: dict) -> dict:
    try:
        validated = BudgetInput(**params)
    except Exception as e:
        return {"error": f"预算数据校验失败: {str(e)}"}
    pocket = validated.pocket
    monthly_budget = validated.amount
    budgets = read_json(BUDGETS_FILE)
    found = False
    for b in budgets:
        if b["pocket"] == pocket:
            b["monthly_budget"] = monthly_budget
            found = True
    if not found:
        budgets.append({"pocket": pocket, "monthly_budget": monthly_budget})
    write_json(BUDGETS_FILE, budgets)
    return {"success": True, "message": f"【{pocket}】月度预算设置为 ￥{monthly_budget}"}


def get_budgets(params: dict = None) -> list:
    init_budgets()
    return read_json(BUDGETS_FILE)


def budget_usage(params: dict) -> dict:
    pocket = params.get("pocket", "")
    budgets = read_json(BUDGETS_FILE)
    budget = 0
    for b in budgets:
        if b["pocket"] == pocket:
            budget = b["monthly_budget"]
            break
    now = datetime.now()
    month_start = now.strftime("%Y-%m-01 00:00:00")
    month_end = now.strftime("%Y-%m-%d %H:%M:%S")
    bills = get_bills({"start_date": month_start, "end_date": month_end,
                       "pocket": pocket, "type": "expense"})
    spent = sum(b["amount"] for b in bills)
    return {
        "pocket": pocket,
        "budget": budget,
        "spent": round(spent, 2),
        "remaining": round(budget - spent, 2),
        "usage_rate": round(spent / budget * 100, 1) if budget > 0 else 0,
    }


COMMANDS = {
    "set_budget": set_budget,
    "get_budgets": get_budgets,
    "budget_usage": budget_usage,
}
