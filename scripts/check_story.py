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
语言锁定（v2.8）：目标语言 = 用户那句话的语言，不默认英语；
  --lang 不给时读故事 JSON 的 language 字段，再没有时按 zh 走。
  查语言一致性：zh 的对话/旁白不得含拉丁字母单词；en 的不得含 CJK 字符；
  ko 须含韩文，ja 须含假名。见 docs/LANGUAGE_LOCK.md。
语言参数：目标语言、句长上限、词数规则一律读 data/languages/<code>.yaml，
脚本里不写死任何一种语言。发音和语音合成不在本技能范围内，用户自行合成或调用语音 API。
文化锚点（v2.7）：故事 JSON 可带可选字段 culture（五类：clothing/food/props/landscape/colors），
存在时查五类齐全、每类非空、不含空词（“中国元素”“西方元素”“东方元素”“中国风”单独出现即不通过）；
不存在时跳过，通用故事不受影响。见 docs/CULTURE_ANCHORS.md。
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

EMPTY_WORDS = ("中国元素", "西方元素", "东方元素", "中国风", "西式", "中式")

def check_culture(story):
    culture = story.get("culture")
    if not culture:
        return []  # 通用故事跳过
    results = []
    for key in ("clothing", "food", "props", "landscape", "colors"):
        v = str(culture.get(key, "")).strip()
        results.append((f"文化锚点 {key} 已写具体物", bool(v) and v not in EMPTY_WORDS))
    return results

def check_language(story, code):
    """语言一致性（v2.8）：对话 + 旁白必须与目标语言一致。"""
    text = story.get("text", "") + " ".join(story.get("dialogue", []))
    if code == "zh":
        latin = re.findall(r"[A-Za-z]+", text)
        return [("语言一致性：zh 对话/旁白无拉丁字母单词", not latin)]
    if code == "en":
        cjk = re.findall(r"[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]", text)
        return [("语言一致性：en 对话/旁白无 CJK 字符", not cjk)]
    if code == "ko":
        return [("语言一致性：ko 对话/旁白含韩文", bool(re.search(r"[\uac00-\ud7af]", text)))]
    if code == "ja":
        return [("语言一致性：ja 对话/旁白含假名", bool(re.search(r"[\u3040-\u30ff]", text)))]
    return []

def check(story, prof, mode="general"):
    text = story.get("text", "") + " ".join(story.get("dialogue", []))
    low = text.lower()
    results = []
    results.append(("主角唯一（字段非空）", bool(story.get("protagonist"))))
    results.append(("主题一句话（字段非空）", bool(story.get("theme"))))
    results.append(("目标语言已写清（字段 language 非空）", bool(story.get("language"))))
    results.extend(check_culture(story))
    results.extend(check_language(story, prof["code"]))
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
    lang = None
    mode = "general"
    args = sys.argv[1:]
    if "--lang" in args:
        lang = args[args.index("--lang") + 1]
    if "--mode" in args:
        mode = args[args.index("--mode") + 1]
    story = json.load(open(args[0], encoding="utf-8"))
    lang = lang or story.get("language") or "zh"  # v2.8：不默认英语
    prof = load_profile(lang)
    print(f"模式：{mode}")
    ok = True
    for name, passed in check(story, prof, mode):
        print(("通过 " if passed else "不通过 ") + name)
        ok = ok and passed
    print("结论：" + ("通过" if ok else "不通过，改骨架，不生成视频"))
