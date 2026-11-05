#!/usr/bin/env python3
"""人物一致性检查（通用版 v1.6）。
用法: python3 scripts/character_check.py <json>
输入 JSON（占位符，换 IP 时只填这里，不改脚本）:
{
  "characters": [
    {"id": "C1", "dna": "plump round green bean, small green sprout on head, ...",
     "markers": ["green sprout", "white chef hat"]},
  ],
  "shots": [
    {"id": 1, "characters": ["C1"], "prompt": "A plump round green bean, small green sprout on head, ... runs."},
  ]
}
检查:
- 每段提示词必须逐字包含该段出场人物的角色 DNA（一字不改）
- 每段提示词必须提到该人物的每件标志物
任一项不过即不通过，改提示词，不生成视频。
成片帧对照三视图的验收是人工核对（颜色、体型、标志物、比例），见 docs/CHARACTER_CONSISTENCY.md。
"""
import json
import sys

def main():
    with open(sys.argv[1]) as f:
        data = json.load(f)
    chars = {c["id"]: c for c in data.get("characters", [])}
    ok = True
    for shot in data.get("shots", []):
        prompt = shot.get("prompt", "")
        for cid in shot.get("characters", []):
            c = chars.get(cid)
            if not c:
                print(f"不通过 镜 {shot.get('id')} 角色 {cid} 不在锁定表里")
                ok = False
                continue
            if c["dna"] not in prompt:
                print(f"不通过 镜 {shot.get('id')} 角色 {cid} 的 DNA 未逐字出现在提示词里")
                ok = False
            else:
                print(f"通过 镜 {shot.get('id')} 角色 {cid} DNA 逐字复用")
            for m in c.get("markers", []):
                if m.lower() not in prompt.lower():
                    print(f"不通过 镜 {shot.get('id')} 角色 {cid} 标志物“{m}”未在提示词里")
                    ok = False
                else:
                    print(f"通过 镜 {shot.get('id')} 角色 {cid} 标志物“{m}”在提示词里")
    print("结论：通过" if ok else "结论：不通过，改提示词，不生成视频")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
