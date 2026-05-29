"""共享存储层：文件读写、ID 生成、路径常量"""
import fcntl
import json
import os
from datetime import datetime, timedelta


def _detect_skill_dir() -> str:
    """自动检测 Skill 根目录，兼容多种 AI 平台安装位置"""
    # 1. 基于本文件位置推导（最可靠：modules/store.py → skill根目录）
    this_dir = os.path.dirname(os.path.abspath(__file__))
    candidate = os.path.dirname(os.path.dirname(this_dir))  # scripts/modules/ → skill根目录
    skill_md = os.path.join(candidate, "SKILL.md")
    if os.path.exists(skill_md):
        return candidate

    # 2. CodeBuddy 默认位置
    codebuddy_path = os.path.expanduser("~/.codebuddy/skills/mindful-finance-coach")
    if os.path.exists(os.path.join(codebuddy_path, "SKILL.md")):
        return codebuddy_path

    # 3. Claude Code 默认位置
    claude_path = os.path.expanduser("~/.claude/skills/mindful-finance-coach")
    if os.path.exists(os.path.join(claude_path, "SKILL.md")):
        return claude_path

    # 4. 回退到基于本文件位置推导（即使 SKILL.md 不存在也可用）
    return candidate


SKILL_DIR = _detect_skill_dir()
DATA_DIR = os.path.join(SKILL_DIR, "data")
OUTPUT_DIR = os.path.join(SKILL_DIR, "output")

BILLS_FILE = os.path.join(DATA_DIR, "bills.json")
BUDGETS_FILE = os.path.join(DATA_DIR, "budgets.json")
SUGGESTIONS_FILE = os.path.join(DATA_DIR, "suggestions.json")
MOODS_FILE = os.path.join(DATA_DIR, "moods.json")
WISHLIST_FILE = os.path.join(DATA_DIR, "wishlist.json")
RECURRING_FILE = os.path.join(DATA_DIR, "recurring.json")
CONFIG_FILE = os.path.join(DATA_DIR, "config.json")
DEBTS_FILE = os.path.join(DATA_DIR, "debts.json")
DEBT_PAYMENTS_FILE = os.path.join(DATA_DIR, "debt_payments.json")


def ensure_dir():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def read_json(path: str) -> list:
    ensure_dir()
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: str, data):
    ensure_dir()
    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        json.dump(data, f, ensure_ascii=False, indent=2)
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)
    os.replace(tmp_path, path)


def next_id(items: list) -> int:
    if not items:
        return 1
    return max(item.get("id", 0) for item in items) + 1


def read_config() -> dict:
    ensure_dir()
    if not os.path.exists(CONFIG_FILE):
        return {}
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def write_config(config: dict):
    ensure_dir()
    tmp_path = CONFIG_FILE + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        json.dump(config, f, ensure_ascii=False, indent=2)
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)
    os.replace(tmp_path, CONFIG_FILE)


def period_range(period: str = "month"):
    """返回 (start_str, end_str)"""
    now = datetime.now()
    if period == "week":
        start = (now - timedelta(days=now.weekday())).strftime("%Y-%m-%d 00:00:00")
    elif period == "month":
        start = now.strftime("%Y-%m-01 00:00:00")
    elif period == "year":
        start = now.strftime("%Y-01-01 00:00:00")
    else:
        start = now.strftime("%Y-%m-01 00:00:00")
    end = now.strftime("%Y-%m-%d %H:%M:%S")
    return start, end


def previous_period_range(period: str = "month"):
    """返回上一个周期的 (start_str, end_str)"""
    now = datetime.now()
    if period == "week":
        this_monday = now - timedelta(days=now.weekday())
        last_monday = this_monday - timedelta(days=7)
        last_sunday = this_monday - timedelta(days=1)
        start = last_monday.strftime("%Y-%m-%d 00:00:00")
        end = last_sunday.strftime("%Y-%m-%d 23:59:59")
    elif period == "month":
        first_of_this_month = now.replace(day=1)
        last_of_prev = first_of_this_month - timedelta(days=1)
        start = last_of_prev.replace(day=1).strftime("%Y-%m-%d 00:00:00")
        end = last_of_prev.strftime("%Y-%m-%d 23:59:59")
    elif period == "year":
        start = f"{now.year - 1}-01-01 00:00:00"
        end = f"{now.year - 1}-12-31 23:59:59"
    else:
        first_of_this_month = now.replace(day=1)
        last_of_prev = first_of_this_month - timedelta(days=1)
        start = last_of_prev.replace(day=1).strftime("%Y-%m-%d 00:00:00")
        end = last_of_prev.strftime("%Y-%m-%d 23:59:59")
    return start, end
