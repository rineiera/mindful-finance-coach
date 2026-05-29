#!/usr/bin/env python3
"""
心理理财教练 - CLI 入口
调度各功能模块，支持 stdin 传入 JSON 参数
"""
import json
import sys

from modules import ALL_COMMANDS


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <command> [JSON_PARAMS]")
        print(f"Commands: {', '.join(ALL_COMMANDS.keys())}")
        print(f'\nExample: {sys.argv[0]} add_bill \'{{"item":"奶茶","amount":35,"type":"expense","pocket":"悦己的钱"}}\'')
        print(f'         echo \'{{"item":"奶茶","amount":35}}\' | {sys.argv[0]} add_bill')
        sys.exit(1)

    command = sys.argv[1]
    if command not in ALL_COMMANDS:
        print(json.dumps({"error": f"未知命令: {command}", "available": list(ALL_COMMANDS.keys())}, ensure_ascii=False))
        sys.exit(1)

    params = {}
    if not sys.stdin.isatty():
        try:
            params = json.load(sys.stdin)
        except json.JSONDecodeError:
            params = {}
    elif len(sys.argv) > 2:
        try:
            params = json.loads(sys.argv[2])
        except json.JSONDecodeError:
            params = {}

    result = ALL_COMMANDS[command](params)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
