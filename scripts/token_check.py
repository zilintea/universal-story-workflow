#!/usr/bin/env python3
"""Token 代理检查：比较散文模板与紧凑模板的字符数（token 代理，非精确 token 数）。
用法：python token_check.py
"""
import os

def chars(path):
    try:
        return len(open(path, encoding="utf-8").read())
    except FileNotFoundError:
        return 0

if __name__ == "__main__":
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    prose = chars(os.path.join(base, "examples", "fire-english-text.md"))
    compact = chars(os.path.join(base, "templates", "compact_story.txt"))
    print(f"散文示例字符数: {prose}")
    print(f"紧凑模板字符数: {compact}")
    if prose:
        print(f"紧凑模板相对散文示例: {compact/prose:.0%}")
        print("注意：紧凑模板不含完整人物描述（锁定表另存），只做一集时不一定更省，集数越多越省。")
