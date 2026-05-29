#!/usr/bin/env python3
"""
心理理财教练 - 常量、工具函数、Pydantic 数据模型
供各模块共享引用
"""
import re
from typing import Optional

from pydantic import BaseModel, field_validator

# ─── 常量 ───

VALID_POCKETS = ["要命的钱", "保命的钱", "生钱的钱", "悦己的钱"]
VALID_EMOTIONS = ["压力", "焦虑", "愉悦", "无聊", "低落", "日常"]
VALID_BILL_TYPES = ["expense", "income"]
VALID_FREQUENCIES = ["monthly", "weekly"]
VALID_WISHLIST_STATUSES = ["waiting", "cooled", "purchased", "cancelled"]
VALID_SUGGESTION_STATUSES = ["pending", "done", "skipped"]

POCKET_ALIASES = {
    "要命": "要命的钱", "保命": "保命的钱", "生钱": "生钱的钱", "悦己": "悦己的钱",
    "生活": "要命的钱", "应急": "保命的钱", "投资": "生钱的钱", "娱乐": "悦己的钱",
}
EMOTION_ALIASES = {
    "平静": "日常", "中性": "日常", "无感": "日常", "日常无感": "日常",
    "开心": "愉悦", "高兴": "愉悦", "爽": "愉悦", "满足": "愉悦",
    "累": "压力", "疲惫": "压力", "崩溃": "压力",
    "烦": "压力", "心累": "压力", "emo": "低落", "难过": "低落", "丧": "低落",
}


# ─── 工具函数 ───

def normalize_pocket(value: str) -> str:
    """纠正财务包名称"""
    if value in VALID_POCKETS:
        return value
    return POCKET_ALIASES.get(value, value)


def normalize_emotion(value: str) -> str:
    """纠正情绪标签"""
    if value in VALID_EMOTIONS:
        return value
    return EMOTION_ALIASES.get(value, value)


def normalize_amount(value) -> float:
    """清理金额：去除货币符号、逗号等，转为 float"""
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        cleaned = re.sub(r"[￥¥$，,]", "", value.strip())
        try:
            return float(cleaned)
        except ValueError:
            return 0.0
    return 0.0


# ─── Pydantic 数据模型 ───

class BillInput(BaseModel):
    item: str
    amount: float
    type: str = "expense"
    pocket: str = "要命的钱"
    emotion_tag: str = ""
    emotion_sub_tag: str = ""
    emotion_raw: str = ""
    note: str = ""
    splits: Optional[list] = None

    @field_validator("amount", mode="before")
    @classmethod
    def clean_amount(cls, v):
        result = normalize_amount(v)
        if result <= 0:
            raise ValueError(
                f"金额缺失或无效（收到: {v}），请向用户确认消费金额后再记录"
            )
        return result

    @field_validator("type", mode="before")
    @classmethod
    def clean_type(cls, v):
        if v in VALID_BILL_TYPES:
            return v
        if v in ("支出", "花", "消费"):
            return "expense"
        if v in ("收入", "赚"):
            return "income"
        return "expense"

    @field_validator("pocket", mode="before")
    @classmethod
    def clean_pocket(cls, v):
        result = normalize_pocket(v)
        if result not in VALID_POCKETS:
            raise ValueError(
                f"无法识别财务包「{v}」，请向用户确认属于哪一类：{VALID_POCKETS}"
            )
        return result

    @field_validator("emotion_tag", mode="before")
    @classmethod
    def clean_emotion_tag(cls, v):
        if not v:
            return ""
        result = normalize_emotion(v)
        if result not in VALID_EMOTIONS:
            return ""
        return result


class SplitItem(BaseModel):
    item: str
    amount: float
    pocket: str = "要命的钱"
    emotion_tag: str = ""
    emotion_sub_tag: str = ""
    emotion_raw: str = ""

    @field_validator("amount", mode="before")
    @classmethod
    def clean_amount(cls, v):
        result = normalize_amount(v)
        if result <= 0:
            raise ValueError(
                f"拆分项金额缺失或无效（收到: {v}），请向用户确认该部分的金额"
            )
        return result

    @field_validator("pocket", mode="before")
    @classmethod
    def clean_pocket(cls, v):
        result = normalize_pocket(v)
        if result not in VALID_POCKETS:
            raise ValueError(
                f"无法识别拆分项财务包「{v}」，请向用户确认属于哪一类：{VALID_POCKETS}"
            )
        return result

    @field_validator("emotion_tag", mode="before")
    @classmethod
    def clean_emotion_tag(cls, v):
        if not v:
            return ""
        result = normalize_emotion(v)
        return result if result in VALID_EMOTIONS else ""


class MoodInput(BaseModel):
    emotion_tag: str
    emotion_sub_tag: str = ""
    emotion_raw: str = ""
    note: str = ""

    @field_validator("emotion_tag", mode="before")
    @classmethod
    def clean_emotion_tag(cls, v):
        result = normalize_emotion(v)
        if result not in VALID_EMOTIONS:
            raise ValueError(
                f"无法识别情绪「{v}」，请向用户确认当前心情，可选：{VALID_EMOTIONS}"
            )
        return result


class WishlistInput(BaseModel):
    item: str
    amount: float
    pocket: str = "悦己的钱"
    emotion_tag: str = ""
    emotion_raw: str = ""
    note: str = ""

    @field_validator("amount", mode="before")
    @classmethod
    def clean_amount(cls, v):
        return normalize_amount(v)

    @field_validator("pocket", mode="before")
    @classmethod
    def clean_pocket(cls, v):
        return normalize_pocket(v)


class RecurringInput(BaseModel):
    item: str
    amount: float
    type: str = "expense"
    pocket: str = "要命的钱"
    frequency: str = "monthly"
    emotion_tag: str = "日常"
    note: str = ""

    @field_validator("amount", mode="before")
    @classmethod
    def clean_amount(cls, v):
        return normalize_amount(v)

    @field_validator("pocket", mode="before")
    @classmethod
    def clean_pocket(cls, v):
        return normalize_pocket(v)

    @field_validator("frequency", mode="before")
    @classmethod
    def clean_frequency(cls, v):
        if v in VALID_FREQUENCIES:
            return v
        return "monthly"


class BudgetInput(BaseModel):
    pocket: str
    amount: float

    @field_validator("amount", mode="before")
    @classmethod
    def clean_amount(cls, v):
        return normalize_amount(v)

    @field_validator("pocket", mode="before")
    @classmethod
    def clean_pocket(cls, v):
        return normalize_pocket(v)


class DebtInput(BaseModel):
    name: str
    total_amount: float
    interest_rate: float = 0.0
    min_payment: float = 0.0
    due_day: int = 1
    note: str = ""

    @field_validator("total_amount", mode="before")
    @classmethod
    def clean_total(cls, v):
        result = normalize_amount(v)
        if result <= 0:
            raise ValueError("债务总额缺失或无效，请向用户确认欠款总额后再添加")
        return result

    @field_validator("min_payment", mode="before")
    @classmethod
    def clean_min_payment(cls, v):
        return normalize_amount(v)

    @field_validator("due_day", mode="before")
    @classmethod
    def clean_due_day(cls, v):
        v = int(v) if v else 1
        if v < 1 or v > 31:
            return 1
        return v


class DebtPaymentInput(BaseModel):
    debt_id: int
    amount: float
    is_extra: bool = False

    @field_validator("amount", mode="before")
    @classmethod
    def clean_amount(cls, v):
        result = normalize_amount(v)
        if result <= 0:
            raise ValueError("还款金额缺失或无效，请向用户确认本次还款金额")
        return result
