#!/usr/bin/env python3
"""季检查（通用版 v1.7）：输入季 JSON，输出通过/不通过清单。
季 JSON（占位符，换 IP / 换季时只填这里，不改脚本）:
{
  "season_arc": "from ... to ...",
  "finale_payoff": "payoff text",
  "episodes": [
    {"id": 1, "theme": "...", "new_vocab": ["a","b"], "review_vocab": [],
     "characters": ["C1","C2"], "scenes": ["S1"], "guest_characters": [], "new_scenes": [],
     "foreshadow": "payoff text"},
  ]
}
检查: 主题不重复、每集新词<=5、复习旧词>=2（第1集除外）、
新词在 +1/+3/+7 集复习、季终伏笔在第1集埋下、
客串角色每集<=1、新增场景每集<=1。
用法: python3 scripts/check_season.py season.json
"""
import json
import sys

def main():
    season = json.load(open(sys.argv[1], encoding="utf-8"))
    eps = season.get("episodes", [])
    ok = True
    def report(passed, name):
        nonlocal ok
        print(("通过 " if passed else "不通过 ") + name)
        ok = ok and passed

    themes = [e.get("theme", "") for e in eps]
    report(len(themes) == len(set(themes)), "集主题不重复")
    for e in eps:
        n = len(e.get("new_vocab", []))
        report(n <= 5, f"第 {e['id']} 集新词 ≤5 个（实测 {n} 个）")
        if e["id"] > 1:
            r = len(e.get("review_vocab", []))
            report(r >= 2, f"第 {e['id']} 集复习旧词 ≥2 个（实测 {r} 个）")
        report(len(e.get("guest_characters", [])) <= 1, f"第 {e['id']} 集客串角色 ≤1 个")
        report(len(e.get("new_scenes", [])) <= 1, f"第 {e['id']} 集新增场景 ≤1 个")
    # 词汇复习：新词在 +1/+3/+7 集（季内）至少复习 1 次
    by_id = {e["id"]: e for e in eps}
    for e in eps:
        for w in e.get("new_vocab", []):
            for offset in (1, 3, 7):
                nid = e["id"] + offset
                if nid in by_id:
                    reviewed = w in by_id[nid].get("review_vocab", []) or w in by_id[nid].get("new_vocab", [])
                    report(reviewed, f"词“{w}”在第 {nid} 集复习（+{offset}）")
    # 季终伏笔在第 1 集埋下
    payoff = season.get("finale_payoff", "")
    if payoff and eps:
        report(payoff in str(eps[0].get("foreshadow", "")), "季终 payoff 的伏笔在第 1 集埋下")
    print("结论：通过" if ok else "结论：不通过，改季表或改本集，不生成视频")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
