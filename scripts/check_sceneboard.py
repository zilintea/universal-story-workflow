#!/usr/bin/env python3
"""场景设定板校验（v3.22）：校验 scenes.json 的场景定义是否齐全。

对应上传 shortvideo-pipeline 的 sceneboard.py（missing_hard + cmd_check），
按本技能 v3.21 docs/SCENE_BOARD.md 的七要素改写：
- 硬项（缺一项即不合格，退 1）：锚点物 anchor、三段光 lights（≥3）、
  三机位 angles（≥3）、平面要点 plan（≥3 条）、材质细节 materials（≥4 样）、
  色板 palette、使用痕迹 traces。
- --strict 下还验图：无人版主图 empty_file 与六格设定板 board_file 必须存在；
  登记为 has_people=true 的旧底图直接判不合格（做多镜要先出无人版）。
- 不带 --strict 时缺图只提醒，不阻断单条。

scenes.json 格式（与产线兼容）：
  {"scenes": [{"id": "forest", "name": "森林空地", "anchor": "大红果树",
    "lights": ["清晨", "正午", "黄昏"], "angles": [{"id": 1, "name": "全景"}, ...],
    "plan": ["入口在左", "果树居中", "蚁丘在右"], "materials": ["树皮", "草", "土", "果"],
    "palette": ["#7a9a5a", "#c8402a"], "traces": "草被踩出一条小路",
    "empty_file": "scenes/empty-forest.jpg", "board_file": "scenes/board-forest.jpg"}]}

用法：
  python3 scripts/check_sceneboard.py --scenes canvas/scenes.json [--pack-dir .] [--strict]
退出码：0 通过｜1 不合格｜2 参数或路径错｜3 就绪度不足（登记表里没有场景）。
"""
import json
import sys
from pathlib import Path

MIN_LIGHTS = 3
MIN_ANGLES = 3
MIN_PLAN = 3
MIN_MATERIALS = 4


def missing_hard(s):
    out = []
    if not (s.get("anchor") or "").strip():
        out.append("锚点物")
    if len(s.get("lights") or []) < MIN_LIGHTS:
        out.append(f"光线时段（要 {MIN_LIGHTS} 段）")
    if len(s.get("angles") or []) < MIN_ANGLES:
        out.append(f"机位（要 {MIN_ANGLES} 个）")
    if len([x for x in (s.get("plan") or []) if x]) < MIN_PLAN:
        out.append(f"平面结构要点（至少 {MIN_PLAN} 条）")
    if len(s.get("materials") or []) < MIN_MATERIALS:
        out.append(f"材质细节（要 {MIN_MATERIALS} 样）")
    if not (s.get("palette") or []):
        out.append("色板")
    if not (s.get("traces") or "").strip():
        out.append("使用痕迹")
    return out


def main():
    argv = sys.argv[1:]
    def opt(name, default=None):
        return argv[argv.index(name) + 1] if name in argv else default
    scenes_path = opt("--scenes")
    pack_dir = Path(opt("--pack-dir", "."))
    strict = "--strict" in argv
    if not scenes_path:
        print("用法：check_sceneboard.py --scenes canvas/scenes.json [--pack-dir .] [--strict]")
        return 2
    try:
        reg = json.loads(Path(scenes_path).read_text(encoding="utf-8"))
    except Exception as e:
        print(f"读 {scenes_path} 失败：{e}")
        return 2
    scenes = reg.get("scenes") if isinstance(reg, dict) else reg
    if not scenes:
        print("就绪度不足：场景登记表里没有场景")
        return 3
    hard_fail, soft_gap = [], []
    for s in scenes:
        miss = missing_hard(s)
        if miss:
            hard_fail.append(f"{s.get('id', '?')}（{s.get('name', '')}）：缺 " + "、".join(miss))
        for key, label in (("empty_file", "无人版主图"), ("board_file", "六格设定板")):
            f = s.get(key)
            if f and not (pack_dir / f).exists():
                soft_gap.append(f"{s.get('id', '?')} {label} {f} 不存在")
            elif not f:
                soft_gap.append(f"{s.get('id', '?')} 未登记 {label}（{key}）")
        if s.get("has_people") is True:
            hard_fail.append(f"{s.get('id', '?')}：登记为有人物的旧底图，做多镜要先出无人版（empty_file）")
    if hard_fail:
        print("场景定义不合格：")
        for x in hard_fail:
            print("  - " + x)
        print("补齐方式：在 scenes.json 里给这一场加 anchor / lights / angles / plan / materials / palette / traces，")
        print("或按 docs/SCENE_BOARD.md 出板。")
        return 1
    if strict and soft_gap:
        print("设定板还差这些图（--strict 下算不合格）：")
        for x in soft_gap:
            print("  - " + x)
        return 1
    print(f"场景定义合格：{len(scenes)} 场｜锚点、三段光、三机位、平面、四材质、色板、使用痕迹齐全")
    if soft_gap:
        print(f"还差 {len(soft_gap)} 项（不阻断单条，做多镜前补齐）：")
        for x in soft_gap:
            print("  - " + x)
    return 0


if __name__ == "__main__":
    sys.exit(main())
