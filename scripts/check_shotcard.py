#!/usr/bin/env python3
"""镜头卡审计（v1.9）：每镜必填字段，缺一项不进视频。
用法：python3 scripts/check_shotcard.py shots.json
输入：[{"id":1,"scale":"MCU","angle":"EL","camera_side":"left","move":"STATIC",
"comp":"THIRDS","light":"top-left hard 5600K","color":"grey-brown 70%",
"action_start":"...","action_end":"...","env":"...","first":"...","last":"...","emotion":7}]
"""
import json, sys

SCALES = {"EWS","WS","MS-FULL","MS","MCU","CU","ECU","INS"}
ANGLES = {"EL","LOW","HIGH","DUTCH","TOP","AERIAL","OTS","POV"}
MOVES = {"STATIC","PUSH","PULL","PAN","TRACK","FOLLOW","CRANE","ORBIT","WHIP","ZOOM"}
REQUIRED = ["id","scale","angle","camera_side","move","comp","light","color",
            "action_start","action_end","env","first","last","emotion"]

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
    # 连续同景别 ≤2
    for i in range(len(shots)-2):
        if shots[i].get('scale') == shots[i+1].get('scale') == shots[i+2].get('scale'):
            fails.append(f"镜 {shots[i]['id']}-{shots[i+2]['id']} 连续 3 镜同景别")
    for f in fails:
        print("不通过", f)
    print("结论：" + ("不通过，改镜头卡，不进视频" if fails else "通过"))

if __name__ == '__main__':
    main()
