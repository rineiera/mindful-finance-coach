"""心情日记模块"""
from datetime import datetime

from models import MoodInput
from modules.store import read_json, write_json, next_id, period_range, MOODS_FILE


def add_mood(params: dict) -> dict:
    try:
        validated = MoodInput(**params)
    except Exception as e:
        return {"error": f"心情数据校验失败: {str(e)}"}
    moods = read_json(MOODS_FILE)
    mood = {
        "id": next_id(moods),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "emotion_tag": validated.emotion_tag,
        "emotion_sub_tag": validated.emotion_sub_tag,
        "emotion_raw": validated.emotion_raw,
        "note": params.get("note", ""),
    }
    moods.append(mood)
    write_json(MOODS_FILE, moods)
    return mood


def get_moods(params: dict = None) -> list:
    params = params or {}
    period = params.get("period", "month")
    start, end = period_range(period)
    moods = read_json(MOODS_FILE)
    result = []
    for m in reversed(moods):
        if start and m["created_at"] < start:
            continue
        if end and m["created_at"] > end:
            continue
        result.append(m)
        if len(result) >= 1000:
            break
    return result


COMMANDS = {
    "add_mood": add_mood,
    "get_moods": get_moods,
}
