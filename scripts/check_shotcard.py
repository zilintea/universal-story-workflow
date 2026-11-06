#!/usr/bin/env python3
"""镜头卡审计（v1.9；v3.7：必填字段 14 → 16，加 moving、move_reason）。
用法：python3 scripts/check_shotcard.py shots.json
输入：[{"id":1,"scale":"MCU","angle":"EL","camera_side":"left","move":"STATIC",
"comp":"THIRDS","light":"top-left hard 5600K","color":"grey-brown 70%",
"action_start":"...","action_end":"...","moving":"...","move_reason":"...",
"env":"...","first":"...","last":"...","emotion":7}]
动态画布（v3.2，见 docs/DYNAMIC_CANVAS.md）：格数 G = 实际镜数，不再是 N × 3。
镜头卡可带可选字段 segment（第几段，从 1 开始）；不带时按旧约定推断（每 3 镜一段），旧稿不受影响。
同段重复构图（景别 + 机位 + 环境 + 出场人物完全相同）即不通过，合并为 1 格。
"""
import json, sys

SCALES = {"EWS","WS","MS-FULL","MS","MCU","CU","ECU","INS"}
ANGLES = {"EL","LOW","HIGH","DUTCH","TOP","AERIAL","OTS","POV"}
MOVES = {"STATIC","PUSH","PULL","PAN","TRACK","FOLLOW","CRANE","ORBIT","WHIP","ZOOM"}
REQUIRED = ["id","scale","angle","camera_side","move","comp","light","color",
            "action_start","action_end","moving","move_reason","env","first","last","emotion"]

def main():
    shots = json.load(open(sys.argv[1], encoding='utf-8'))
    fails = []
    for s in shots:
        for f in REQUIRED:
            if not s.get(f):
                fails.append(f"镜 {s.get('id')} 缺字段 {f}")
        if s.get('scale') not in SCALES:
            fails.append(f"镜 {s.get('id')} 景别 {s.get('scale')} 不在短码表")
        if s.get('angle') not in ANGLES:
            fails.append(f"镜 {s.get('id')} 机位 {s.get('angle')} 不在短码表")
        if s.get('move') not in MOVES:
            fails.append(f"镜 {s.get('id')} 运镜 {s.get('move')} 不在短码表")
    # 首尾帧衔接：下一镜 first 必须等于上一镜 last（逐字复用）
    for a, b in zip(shots, shots[1:]):
        if a.get('last') and b.get('first') and a['last'] != b['first']:
            fails.append(f"镜 {a['id']}→{b['id']} 首尾帧不衔接：尾帧≠下镜首帧")
    # 连续同景别 ≤2（v3.2 修正：只看同一主角。反打轮流换人时，同景别连拍不算单调）
    for i in range(len(shots)-2):
        same_scale = shots[i].get('scale') == shots[i+1].get('scale') == shots[i+2].get('scale')
        same_chars = (shots[i].get('characters') == shots[i+1].get('characters') ==
                      shots[i+2].get('characters'))
        if same_scale and same_chars:
            fails.append(f"镜 {shots[i]['id']}-{shots[i+2]['id']} 连续 3 镜同景别同主角")
    # 动态画布（v3.2）：同段重复构图即不通过（景别 + 机位 + 环境 + 出场人物 + 动作起止完全相同，
    # 即同一个瞬间画了两遍）。正反打不算重复：动作不同，构图就不同。
    def seg(s):
        return s.get('segment') if s.get('segment') is not None else (s.get('id', 1) - 1) // 3 + 1
    from collections import defaultdict
    by_seg = defaultdict(list)
    for s in shots:
        by_seg[seg(s)].append(s)
    for s_no, group in sorted(by_seg.items()):
        seen = {}
        for s in group:
            key = (s.get('scale'), s.get('angle'), s.get('env'),
                   tuple(s.get('characters', [])),
                   s.get('action_start'), s.get('action_end'))
            if key in seen:
                fails.append(f"镜 {s.get('id')} 与镜 {seen[key]} 同段重复构图（景别/机位/环境/人物/动作完全相同），合并为 1 格")
            else:
                seen[key] = s.get('id')
    print(f"格数 G = {len(shots)}（动态评估：按实际镜数）" +
          "".join(f"，第 {k} 段 {len(v)} 格" for k, v in sorted(by_seg.items())))
    for f in fails:
        print("不通过", f)
    print("结论：" + ("不通过，改镜头卡，不进视频" if fails else "通过"))

if __name__ == '__main__':
    main()
