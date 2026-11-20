#!/usr/bin/env python3
"""镜头卡审计（v1.9；v3.7：必填字段 14 → 16，加 moving、move_reason；
v3.10：首尾帧分连续/切换——切换镜的首帧是本镜自己的开场，不是上一镜尾帧的静止复刻；
v3.16：短码表扩到 docs/CAMERA_MOVES.md——机位加 WORM（极低机位仰拍）、WAIST（过腰），
运镜加 RACK（焦点转移）、CRASHZOOM（急推）、DOLLY（滑轨）、HANDHELD（手持）、
SLOWMO（慢动作）、ONETAKE（一镜到底）、STEP（抽帧）。
v3.24：必填字段 16 → 18，加 camera_pos（场景设定板平面图上的机位编号，如“机位 1”，
与设定板对得上，不凭空发明）、anchor（本镜画面里的场景锚点物，如“大荷叶上的绿青蛙”，
与场景设定板定的锚点物一致）。
用法：python3 scripts/check_shotcard.py shots.json
输入：[{"id":1,"scale":"MCU","angle":"EL","camera_side":"left","move":"STATIC",
"camera_pos":"机位 1","anchor":"大荷叶",
"comp":"THIRDS","light":"top-left hard 5600K","color":"grey-brown 70%",
"action_start":"...","action_end":"...","moving":"...","move_reason":"...",
"env":"...","first":"...","last":"...","emotion":7}]
动态画布（v3.2，见 docs/DYNAMIC_CANVAS.md）：格数 G = 实际镜数，不再是 N × 3。
镜头卡可带可选字段 segment（第几段，从 1 开始）；不带时按旧约定推断（每 3 镜一段），旧稿不受影响。
同段重复构图（景别 + 机位 + 环境 + 出场人物完全相同）即不通过，合并为 1 格。
"""
import json, sys

SCALES = {"EWS","WS","MS-FULL","MS","MCU","CU","ECU","INS"}
ANGLES = {"EL","LOW","WORM","HIGH","DUTCH","TOP","AERIAL","OTS","POV","WAIST"}
MOVES = {"STATIC","PUSH","PULL","PAN","TRACK","FOLLOW","CRANE","ORBIT","WHIP","ZOOM",
         "RACK","CRASHZOOM","DOLLY","HANDHELD","SLOWMO","ONETAKE","STEP"}
TEMPOS = {"快","中","慢"}
REQUIRED = ["id","scale","angle","camera_side","move","camera_pos","anchor","comp","light","color",
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
        # 节奏（v3.20）：可选字段，缺字段按 中 计，旧稿不受影响
        if s.get('tempo') is not None and s.get('tempo') not in TEMPOS:
            fails.append(f"镜 {s.get('id')} 节奏 {s.get('tempo')} 不合法，只许 快 / 中 / 慢")
        if s.get('beats') is not None and s.get('beats') not in (1, 2, 3):
            fails.append(f"镜 {s.get('id')} 动作数 beats {s.get('beats')} 不合法，只许 1–3")
        if (s.get('tempo') or '中') == '快' and s.get('move') == 'SLOWMO':
            fails.append(f"镜 {s.get('id')} 节奏是快却用了慢动作 SLOWMO：快慢矛盾，改 tempo 为 慢 或换运镜")
    # 慢动作上限（v3.20）：全片最多 1 次，连续两镜不许都是慢动作
    slowmo = [s.get('id') for s in shots if s.get('move') == 'SLOWMO']
    if len(slowmo) > 1:
        fails.append(f"慢动作 SLOWMO 全片 {len(slowmo)} 次（镜 {slowmo}），最多 1 次：其余冲击点改快动作 + 硬切")
    for a, b in zip(shots, shots[1:]):
        if a.get('move') == 'SLOWMO' and b.get('move') == 'SLOWMO':
            fails.append(f"镜 {a.get('id')}→{b.get('id')} 连续两镜都是慢动作：慢动作不许连用")
    # 首尾帧衔接（v3.10：分连续/切换两种转场）
    # continuous（默认，缺字段即连续）：下一镜 first 必须等于上一镜 last（逐字复用）。
    # cut（切到新主体/新角度/新地点）：下一镜 first 必须是不等于上一镜 last 的本镜开场
    #   （新主体已在动中），且切换必须真实改变 characters / env / scale 三者至少其一，
    #   否则是贴错标签的连续镜。影视逻辑：切到新镜头时，开场是新镜头自己的画面，
    #   不是上一镜尾帧的静止复刻；动作/声音跨切衔接，不靠首帧复刻。
    for a, b in zip(shots, shots[1:]):
        t = b.get('transition') or 'continuous'
        if t not in ('continuous', 'cut'):
            fails.append(f"镜 {b.get('id')} transition {t!r} 不合法，只许 continuous / cut")
            continue
        if t == 'continuous':
            if a.get('last') and b.get('first') and a['last'] != b['first']:
                fails.append(f"镜 {a['id']}→{b['id']} 首尾帧不衔接：尾帧≠下镜首帧")
        else:
            if a.get('last') and b.get('first') and a['last'] == b['first']:
                fails.append(f"镜 {a['id']}→{b['id']} 是切换却用了上一镜尾帧当首帧：切换镜的开场是本镜自己的画面，不是上一镜的静止复刻")
            changed = (a.get('characters') != b.get('characters') or
                       a.get('env') != b.get('env') or
                       a.get('scale') != b.get('scale'))
            if not changed:
                fails.append(f"镜 {a['id']}→{b['id']} 标了切换却没换主体/地点/景别：不是真切换，改回 continuous")
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
