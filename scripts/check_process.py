#!/usr/bin/env python3
"""流程审计（通用版 v1.8）：输入流程 JSON，输出通过/不通过清单。
流程 JSON（占位符，换流程时只填这里，不改脚本；红烧鱼只是测试数据里的例子）:
{
  "product": "dish name",
  "final_state": "dish ready",
  "ingredients": [{"name": "fish", "amount": "1", "initial_state": "raw"}],
  "tools": [{"name": "pan", "hazard": ""}],
  "steps": [{"id": 1, "action": "wash", "uses": ["fish"],
             "requires": ["fish raw"], "produces": ["fish clean"],
             "hazard": "", "safety": ""}],
  "innovation": {"description": "...", "does_not_change": ["step order", "final state", "safety"]}
}
检查: 序号连续、前置条件被前面满足、材料/工具先声明后使用、
成品只在最后一步出现、危险步骤有安全做法、创意点<=1 处且声明未改项。
用法: python3 scripts/check_process.py process.json
"""
import json
import sys

def main():
    p = json.load(open(sys.argv[1], encoding="utf-8"))
    ok = True
    def report(passed, name):
        nonlocal ok
        print(("通过 " if passed else "不通过 ") + name)
        ok = ok and passed

    steps = p.get("steps", [])
    ids = [s.get("id") for s in steps]
    report(ids == list(range(1, len(steps) + 1)), f"步骤序号连续 1..{len(steps)}（实测 {ids}）")
    known = set()
    for ing in p.get("ingredients", []):
        known.add(ing["name"])
        known.add(ing.get("initial_state", ""))
    for tool in p.get("tools", []):
        known.add(tool["name"])
    produced = set(known)
    for s in steps:
        for u in s.get("uses", []):
            report(u in [i["name"] for i in p.get("ingredients", [])] + [t["name"] for t in p.get("tools", [])],
                   f"第 {s['id']} 步用的“{u}”先在清单里出现过")
        for r in s.get("requires", []):
            report(r in produced, f"第 {s['id']} 步前置条件“{r}”被前面满足")
        for pr in s.get("produces", []):
            produced.add(pr)
        if s.get("hazard"):
            report(bool(s.get("safety")), f"第 {s['id']} 步危险“{s['hazard']}”有安全做法")
    final = p.get("final_state", "")
    report(final in produced, f"成品状态“{final}”被步骤做出来")
    # 成品只在最后一步出现：前面的步骤不能产生成品
    early = [s["id"] for s in steps[:-1] if final in s.get("produces", [])]
    report(not early, f"成品不在最后一步之前出现（提前出现在第 {early} 步即不通过）")
    inn = p.get("innovation")
    if inn is not None:
        report(bool(inn.get("does_not_change")), "创意点声明了没改什么")
        report("step order" in str(inn.get("does_not_change", [])) or "顺序" in str(inn.get("does_not_change", [])),
               "创意点声明了不改步骤顺序")
    print("结论：通过" if ok else "结论：不通过，改流程表或改剧本，不生成视频")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
