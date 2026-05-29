"""建议追踪模块"""
from datetime import datetime

from modules.store import read_json, write_json, next_id, SUGGESTIONS_FILE


def add_suggestion(params: dict) -> dict:
    suggestions = read_json(SUGGESTIONS_FILE)
    suggestion = {
        "id": next_id(suggestions),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "period_start": params.get("period_start", ""),
        "period_end": params.get("period_end", ""),
        "content": params.get("content", ""),
        "status": "pending",
    }
    suggestions.append(suggestion)
    write_json(SUGGESTIONS_FILE, suggestions)
    return suggestion


def get_pending_suggestions(params: dict = None) -> list:
    suggestions = read_json(SUGGESTIONS_FILE)
    return [s for s in suggestions if s["status"] == "pending"]


def update_suggestion(params: dict) -> dict:
    suggestions = read_json(SUGGESTIONS_FILE)
    for s in suggestions:
        if s["id"] == params.get("id"):
            s["status"] = params.get("status", "pending")
    write_json(SUGGESTIONS_FILE, suggestions)
    return {"success": True}


COMMANDS = {
    "add_suggestion": add_suggestion,
    "pending_suggestions": get_pending_suggestions,
    "update_suggestion": update_suggestion,
}
