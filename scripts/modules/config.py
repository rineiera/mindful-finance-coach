"""配置模块：发薪日等"""
from datetime import datetime

from modules.store import read_config, write_config
from modules.bills import get_bills


def set_config(params: dict) -> dict:
    config = read_config()
    for key, value in params.items():
        config[key] = value
    write_config(config)
    return {"success": True, "config": config}


def get_config(params: dict = None) -> dict:
    return read_config()


def check_payday(params: dict = None) -> dict:
    config = read_config()
    payday = config.get("payday")
    if not payday:
        return {"is_payday": False, "reason": "未设置发薪日"}

    today = datetime.now()
    payday_int = int(payday)
    is_today = (today.day == payday_int)

    month_start = today.strftime("%Y-%m-01 00:00:00")
    month_end = today.strftime("%Y-%m-%d %H:%M:%S")
    income_bills = get_bills({"start_date": month_start, "end_date": month_end, "type": "income"})
    has_income = len(income_bills) > 0
    past_payday = (today.day > payday_int) and not has_income

    return {
        "is_payday": is_today,
        "past_payday_unrecorded": past_payday,
        "payday": payday_int,
        "has_income_this_month": has_income,
    }


COMMANDS = {
    "set_config": set_config,
    "get_config": get_config,
    "check_payday": check_payday,
}
