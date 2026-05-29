"""收入分配模块"""
from modules.recurring import get_recurring
from modules.debts import get_debts


def income_allocation(params: dict) -> dict:
    income = float(params.get("income", 0))
    if income <= 0:
        return {"error": "收入金额必须大于0"}

    recurring = get_recurring()
    recurring_total = sum(r["amount"] for r in recurring)

    debts = get_debts()
    monthly_debt_payment = sum(d["min_payment"] for d in debts if d["min_payment"] > 0)

    mandatory_total = recurring_total + monthly_debt_payment
    disposable = max(0, income - mandatory_total)

    ratios = params.get("ratios", [0.50, 0.20, 0.15, 0.15])
    pockets = ["要命的钱", "保命的钱", "生钱的钱", "悦己的钱"]
    allocation = {}
    for i, pocket in enumerate(pockets):
        ratio = ratios[i] if i < len(ratios) else 0.15
        allocation[pocket] = round(disposable * ratio, 2)

    return {
        "income": income,
        "layer1_mandatory": {
            "recurring_bills": round(recurring_total, 2),
            "debt_payments": round(monthly_debt_payment, 2),
            "total": round(mandatory_total, 2),
        },
        "disposable_income": round(disposable, 2),
        "layer2_allocation": allocation,
        "note": "可支配收入 = 收入 - 固定账单 - 最低还款" if mandatory_total > 0 else "无刚性扣除，全额可支配",
    }


COMMANDS = {
    "income_allocation": income_allocation,
}
