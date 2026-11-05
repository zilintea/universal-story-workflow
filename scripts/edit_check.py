#!/usr/bin/env python3
"""影视剪辑 + 连续性检查：输入分镜 JSON，输出通过/不通过清单。
分镜 JSON 格式：
{"shots": [{"id": 1, "scene": "S1", "characters": ["C1"],
  "items": {"I1": "in S1, intact", "I2": "on C1"},
  "camera_side": "left", "shot_scale": "medium", "angle_change": 0,
  "duration": 10, "transition": "hard cut", "action": "cook soup"}, ...]}
检查：180 度轴线、30 度规则、物品连续、场景连续、时长、转场类型。
用法：python edit_check.py episode.json
"""
import sys, json

ALLOWED_TRANSITIONS = {"hard cut", "match on action", "foreground wipe", "dissolve"}

def check(ep):
    shots = ep.get("shots", [])
    results = []
    for i, s in enumerate(shots):
        results.append((f"镜 {s['id']} 时长 ≥2 秒", s.get("duration", 0) >= 2))
        results.append((f"镜 {s['id']} 转场类型允许", s.get("transition", "hard cut") in ALLOWED_TRANSITIONS))
        if i == 0:
            continue
        p = shots[i - 1]
        same_scene = s.get("scene") == p.get("scene")
        # 180 度：同一场景内机位侧不变
        if same_scene:
            results.append((f"转场 {p['id']}→{s['id']} 180 度轴线（同场景机位侧不变）",
                            s.get("camera_side") == p.get("camera_side")))
        # 30 度：同一主体连续两镜，角度变化 ≥30 或景别变化
        if same_scene:
            ok30 = (s.get("angle_change", 0) >= 30) or (s.get("shot_scale") != p.get("shot_scale"))
            results.append((f"转场 {p['id']}→{s['id']} 30 度规则（角度≥30 或景别变化）", ok30))
        # 物品连续：物品状态/位置不变，或本镜有解释（action 字段含该物品变化时，调用方需在 items 里写新状态并在 notes 里说明）
        for item, state in p.get("items", {}).items():
            new = s.get("items", {}).get(item, state)
            changed = new != state
            explained = s.get("item_change_explained", {}).get(item, False)
            results.append((f"转场 {p['id']}→{s['id']} 物品 {item} 连续（不变或有画面解释）",
                            (not changed) or explained))
        # 场景连续：场景变了，转场必须是 wipe 或 dissolve，不能是硬切
        if not same_scene:
            results.append((f"转场 {p['id']}→{s['id']} 场景切换用遮挡/叠化，不能硬切",
                            s.get("transition") in {"foreground wipe", "dissolve"}))
    # 景别节奏：连续 3 镜不为同一景别
    scales = [s.get("shot_scale") for s in shots]
    for i in range(len(scales) - 2):
        results.append((f"镜 {i+1}-{i+3} 景别不连续 3 镜相同",
                        not (scales[i] == scales[i+1] == scales[i+2])))
    return results

if __name__ == "__main__":
    ep = json.load(open(sys.argv[1], encoding="utf-8"))
    ok = True
    for name, passed in check(ep):
        print(("通过 " if passed else "不通过 ") + name)
        ok = ok and passed
    print("结论：" + ("通过" if ok else "不通过，改分镜/转场，不进视频"))
