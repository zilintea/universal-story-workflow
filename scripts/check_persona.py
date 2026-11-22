#!/usr/bin/env python3
"""角色设定板校验（v3.22）：校验 story.json 的角色定义是否达到 v3.21 辨识度要求。

对应上传 shortvideo-pipeline 的 persona.py（sheet / pcheck），按本技能
v3.21 docs/CHARACTER_DISTINCTIVENESS.md 改写：
- DNA 三段式（硬提醒，不合格退 1）：每个角色的 appearance 须是“体态 → 脸上的记号 →
  面料/服装”三段，逗号/分号切分后至少 3 段，且须含一件服装或面料词；缺一段
  即判 DNA 不全（角色在多镜里会漂）。
- 设定图存在性（硬失败退 1）：story.json 的 character_sheet 指向的文件必须存在；
  五格设定图（正面+背面全身、面部特写、左右侧脸、四细节特写）以该文件为准，
  文件缺失即 v3.1 三视图硬门未过。
- --strict 下还验：character_sheets（多角色各一张）是否齐全；appearance 里
  是否出现品牌风格词（如 Pixar/Disney，提示词禁写品牌名）。

用法：
  python3 scripts/check_persona.py --story story.json [--base-dir .] [--strict]
退出码：0 通过｜1 不合格｜2 参数或路径错｜3 就绪度不足（story.json 里没有角色）。
"""
import json
import re
import sys
from pathlib import Path

FABRIC_WORDS = ["布", "棉", "麻", "丝", "绸", "毛", "皮", "衫", "衣", "袍", "裙",
                "裤", "帽", "巾", "围巾", "鞋", "靴", "甲", "袍", "绒", "纱", "呢",
                "cotton", "cloth", "silk", "wool", "linen", "fabric", "dress", "shirt",
                "skirt", "robe", "apron", "shawl", "coat", "fur", "shorts", "scarf",
                "hat", "shoes", "boots", "sweater", "jacket"]
BRAND_WORDS = ["pixar", "disney", "迪士尼", "皮克斯", "ghibli", "吉卜力", "dreamworks", "梦工厂"]


def split_dna(appearance):
    parts = [p.strip() for p in re.split(r"[，,；;、]", appearance) if p.strip()]
    return parts


def main():
    argv = sys.argv[1:]
    def opt(name, default=None):
        return argv[argv.index(name) + 1] if name in argv else default
    story_path = opt("--story")
    base_dir = Path(opt("--base-dir", "."))
    strict = "--strict" in argv
    if not story_path:
        print("用法：check_persona.py --story story.json [--base-dir .] [--strict]")
        return 2
    try:
        story = json.loads(Path(story_path).read_text(encoding="utf-8"))
    except Exception as e:
        print(f"读 {story_path} 失败：{e}")
        return 2
    chars = story.get("characters") or []
    if not chars:
        print("就绪度不足：story.json 里没有角色")
        return 3
    hard, soft = [], []
    for c in chars:
        name = c.get("name") or c.get("id") or "?"
        ap = (c.get("appearance") or "").strip()
        if not ap:
            hard.append(f"{name}：没有 appearance（外貌描述），DNA 无从校验")
            continue
        parts = split_dna(ap)
        if len(parts) < 3:
            hard.append(f"{name}：DNA 只有 {len(parts)} 段，要“体态 → 记号 → 面料”三段，"
                        f"当前：{ap}")
        elif not any(w in ap for w in FABRIC_WORDS):
            hard.append(f"{name}：DNA 缺面料/服装一段（体态→记号→面料，第三段须写服装面料），"
                        f"当前：{ap}")
        low = ap.lower()
        hit = [w for w in BRAND_WORDS if w in low]
        if hit:
            hard.append(f"{name}：appearance 含品牌风格词 {hit}，提示词禁写品牌名，改描述性写法")
    sheet = (story.get("character_sheet") or "").strip()
    if sheet:
        p = Path(sheet)
        if not p.is_absolute():
            p = base_dir / p
        if not p.exists():
            hard.append(f"角色设定图不存在：{sheet}（v3.1 三视图硬门未过）")
    else:
        hard.append("story.json 缺 character_sheet 字段（v3.1 三视图硬门：无设定图不进故事板）")
    if strict:
        sheets = story.get("character_sheets") or {}
        for c in chars:
            name = c.get("name") or c.get("id") or "?"
            if name not in sheets and len(chars) > 1:
                soft.append(f"{name}：多角色集未在 character_sheets 里单列设定图（--strict 提醒）")
    if hard:
        print("角色设定不合格：")
        for h in hard:
            print("  - " + h)
        return 1
    print(f"角色设定合格：{len(chars)} 个角色｜DNA 三段式齐全｜设定图存在")
    for w in soft:
        print("提醒", w)
    return 0


if __name__ == "__main__":
    sys.exit(main())
