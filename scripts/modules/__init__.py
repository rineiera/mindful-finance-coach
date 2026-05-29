"""功能模块包：自动注册所有 COMMANDS"""
from modules.bills import COMMANDS as _bills
from modules.budgets import COMMANDS as _budgets
from modules.moods import COMMANDS as _moods
from modules.wishlist import COMMANDS as _wishlist
from modules.recurring import COMMANDS as _recurring
from modules.debts import COMMANDS as _debts
from modules.suggestions import COMMANDS as _suggestions
from modules.config import COMMANDS as _config
from modules.stats import COMMANDS as _stats
from modules.allocation import COMMANDS as _allocation
from modules.reports import COMMANDS as _reports

ALL_COMMANDS = {}
for _cmd_map in [_bills, _budgets, _moods, _wishlist, _recurring,
                  _debts, _suggestions, _config, _stats, _allocation, _reports]:
    ALL_COMMANDS.update(_cmd_map)
