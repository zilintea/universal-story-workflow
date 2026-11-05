#!/usr/bin/env python3
"""文化锚点拼进分段提示词（v2.7）：读故事 JSON 的 culture 字段（五类），
读分段提示词 JSON [{id, prompt}]，每段提示词后逐字拼上文化锚点。
用法：python apply_culture.py story.json segments.json [out.json]
故事 JSON 没有 culture 字段时原样输出，不报错。
文化锚点是项目属性，不是风格属性；见 docs/CULTURE_ANCHORS.md。
"""
import sys, json

KEYS = ("clothing", "food", "props", "landscape", "colors")
LABELS = {"clothing": "clothing", "food": "food", "props": "props",
          "landscape": "landscape", "colors": "colors"}

def apply(story, segments):
    culture = story.get("culture") or {}
    anchors = {k: str(culture.get(k, "")).strip() for k in KEYS}
    if not any(anchors.values()):
        return segments
    suffix = " Culture anchors (verbatim): " + "; ".join(
        f"{LABELS[k]}: {anchors[k]}" for k in KEYS if anchors[k]) + "."
    return [{"id": s.get("id"), "prompt": s.get("prompt", "") + suffix}
            for s in segments]

if __name__ == "__main__":
    story = json.load(open(sys.argv[1], encoding="utf-8"))
    segments = json.load(open(sys.argv[2], encoding="utf-8"))
    out = apply(story, segments)
    if len(sys.argv) > 3:
        json.dump(out, open(sys.argv[3], "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
    print(json.dumps(out, ensure_ascii=False, indent=1))
