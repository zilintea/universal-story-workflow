#!/usr/bin/env python3
"""自我构思：给主题或不给主题，出 3 个点子并初筛。
用法：python conceive.py [主题]  —— 不给主题时用默认主题池。
初筛规则：物品会毁、反转无伏笔、主角不唯一、硬凑全员的点子直接筛掉。
"""
import sys, json

STRUCTURES = [
    ("送错东西", "东西送错了地方/人，结果发现本来就是给所有人的", "画上没有名字"),
    ("找东西", "东西丢了，沿路找，最后在最开始的地方找到", "东西一直在身边"),
    ("帮忙帮倒忙", "第一次帮错了，第二次在朋友提示下帮对了", "第一次的错误方法在结尾被反用"),
]

THEMES = ["送错的信", "坚持", "谢谢", "分享"]

def conceive(theme):
    ideas = []
    for i, (name, desc, foreshadow) in enumerate(STRUCTURES, 1):
        ideas.append({
            "id": i,
            "structure": name,
            "theme_input": theme,
            "protagonist": "待定：按 IP 插件选唯一主角（不超过 1 人）",
            "goal": f"围绕“{theme}”的一个具体小目标（第 1 幕就看懂）",
            "object": "一个受保护的物品（怕什么、最后完好到哪里，见 SKILL.md 物品保护原则）",
            "foreshadow": foreshadow,
            "twist": desc,
            "screen": "通过" if foreshadow else "不通过",
        })
    return ideas

if __name__ == "__main__":
    theme = sys.argv[1] if len(sys.argv) > 1 else THEMES[0]
    print(json.dumps(conceive(theme), ensure_ascii=False, indent=2))
