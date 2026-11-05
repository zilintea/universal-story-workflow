#!/usr/bin/env python3
"""逻辑 + 语言审计自查：输入故事 JSON，输出通过/不通过清单。
故事 JSON 格式：{"title": str, "protagonist": str, "theme": str,
  "vocab": [str, ...], "patterns": [str, ...],
  "dialogue": [str, ...], "text": str, "foreshadow": bool, "twist": bool,
  "language": "en" | "ko" | "ja" | "zh" | ...}
用法：python check_story.py story.json [--lang en] [--mode general|teaching]
模式：general（默认，通用版）：只查主角、主题、目标语言、反转伏笔；
  警示点、词汇 ≤5、词汇出现 ≥3 次、句型 ≤2 只在 teaching 模式查。
  （v2.3 修正：v2.2 前默认查警示点，通用故事没警示点就被打回，是教学要求漏进通用流程。）
语言参数：目标语言、句长上限、词数规则一律读 data/languages/<code>.yaml，
脚本里不写死任何一种语言。发音和语音合成不在本技能范围内，用户自行合成或调用语音 API。
"""
import sys, json, re
from pathlib import Path

def load_profile(code):
    # 极简 YAML 读法：只读 code/word_unit/dialogue_max_words/narration_max_words
    prof = {"code": code, "word_unit": "space", "dialogue_max_words": 8, "narration_max_words": 12}
    f = Path(__file__).resolve().parent.parent / "data" / "languages" / f"{code}.yaml"
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            if ":" in line and not line.strip().startswith("#"):
                k, v = line.split(":", 1)
                prof[k.strip()] = v.strip()
        for k in ("dialogue_max_words", "narration_max_words"):
            prof[k] = int(prof[k])
    return prof

def count_words(s, unit):
    if unit == "character":
        return len(s.strip())
    return len(s.split())

def check(story, prof, mode="general"):
    text = story.get("text", "") + " ".join(story.get("dialogue", []))
    low = text.lower()
    results = []
    results.append(("主角唯一（字段非空）", bool(story.get("protagonist"))))
    results.append(("主题一句话（字段非空）", bool(story.get("theme"))))
    results.append(("目标语言已写清（字段 language 非空）", bool(story.get("language"))))
    if mode == "teaching":
        results.append(("词汇 ≤5 个", len(story.get("vocab", [])) <= 5))
        results.append(("句型 ≤2 个", len(story.get("patterns", [])) <= 2))
        results.append((f"对话每句 ≤{prof['dialogue_max_words']} 词（{prof['code']} 档案）",
                        all(count_words(d, prof["word_unit"]) <= prof["dialogue_max_words"] for d in story.get("dialogue", []))))
        results.append(("警示点已写清（字段 warning 非空）", bool(story.get("warning"))))
    for word in story.get("vocab", []) if mode == "teaching" else []:
        if re.search(r'[a-zA-Z]', word):
            n = len(re.findall(r'\b' + re.escape(word.lower()) + r'\b', low))
        else:
            n = text.count(word)
        results.append((f"词汇“{word}”出现 ≥3 次（实测 {n} 次）", n >= 3))
    results.append(("反转有伏笔（字段）", bool(story.get("foreshadow") and story.get("twist"))))
    return results

if __name__ == "__main__":
    lang = "en"
    mode = "general"
    args = sys.argv[1:]
    if "--lang" in args:
        lang = args[args.index("--lang") + 1]
    if "--mode" in args:
        mode = args[args.index("--mode") + 1]
    story = json.load(open(args[0], encoding="utf-8"))
    prof = load_profile(story.get("language", lang))
    print(f"模式：{mode}")
    ok = True
    for name, passed in check(story, prof, mode):
        print(("通过 " if passed else "不通过 ") + name)
        ok = ok and passed
    print("结论：" + ("通过" if ok else "不通过，改骨架，不生成视频"))
