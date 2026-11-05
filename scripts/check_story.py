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
默认值（v3.0）：人物类剧集用户没特别指定时，目标语言一律中文，人物形象一律东方人物；
  只在用户明确指定其他语言或非中国背景时才改。见 docs/CHARACTER_DEFAULTS.md。
  查人物形象：story.json 的 characters 存在时，每位人物 appearance 非空；
  character_origin 未写或为 eastern 时 appearance 须含东方标记（黑发/黑眼睛/东亚/东方/亚洲/黄皮肤/中国面孔）；
  origin 明确写了其他值时不查标记；characters 缺失时跳过。
多语言对话（v3.2）：旁白始终用目标语言；对话每句按说话人的语言查——
  显式 lang > character_languages[说话人] > 目标语言；character_languages 的值
  须有语言档案（data/languages/<code>.yaml），没有即不通过。见 docs/LANGUAGE_LOCK.md。
  查国家形象标志：正文 + 对话里不得出现国旗、国徽、旗帜等（FLAG_WORDS）。
三视图硬门（v3.1）：故事 JSON 有 characters 字段时，character_sheet 字段必填，
  且指向的三视图文件必须存在（相对路径按 story.json 所在目录解析）；
  缺字段、路径为空、文件不存在，任一即不通过，不进故事板。
  characters 缺失时跳过（v3.1 之前的旧稿不受影响）。见 docs/CHARACTER_CONSISTENCY.md。
  生成视频的参考图必须是三视图，不许拿 9 格故事板当人物参考。
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

def dialogue_lines(story):
    """对话行归一化：条目可是纯字符串（目标语言），也可以是 {"speaker": "C1", "text": "..."}，
    还可带 "lang" 显式指定本句语言。返回 [(text, speaker, explicit_lang)]。"""
    out = []
    for d in story.get("dialogue", []):
        if isinstance(d, dict):
            out.append((d.get("text", ""), d.get("speaker"), d.get("lang")))
        else:
            out.append((str(d), None, None))
    return out

def lang_rule(code, text):
    """单句语言规则（v2.8）：返回 (通过, 说明)。未知语言无规则可查，返回通过。"""
    if code == "zh":
        latin = re.findall(r"[A-Za-z]+", text)
        return (not latin, "zh 无拉丁字母单词")
    if code == "en":
        cjk = re.findall(r"[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]", text)
        return (not cjk, "en 无 CJK 字符")
    if code == "ko":
        return (bool(re.search(r"[\uac00-\ud7af]", text)), "ko 含韩文")
    if code == "ja":
        return (bool(re.search(r"[\u3040-\u30ff]", text)), "ja 含假名")
    return (True, f"{code} 无规则可查")

def check_language(story, code):
    """语言一致性（v2.8）：对话 + 旁白必须与目标语言一致。
    多语言对话（v3.2）：旁白始终用目标语言；对话每句按说话人的语言查——
    显式 lang > character_languages[说话人] > 目标语言。见 docs/LANGUAGE_LOCK.md。"""
    results = []
    ok, note = lang_rule(code, story.get("text", ""))
    results.append((f"语言一致性：旁白 {note}", ok))
    char_langs = story.get("character_languages") or {}
    for text, speaker, explicit in dialogue_lines(story):
        eff = explicit or (char_langs.get(speaker) if speaker else None) or code
        ok, note = lang_rule(eff, text)
        who = f"（{speaker}，{eff}）" if speaker or explicit else ""
        results.append((f"语言一致性：对话{who} {note}", ok))
    if char_langs:
        langs_dir = Path(__file__).resolve().parent.parent / "data" / "languages"
        for cid, lang in char_langs.items():
            results.append((f"人物 {cid} 的语言 {lang} 有语言档案（data/languages/{lang}.yaml）",
                            (langs_dir / f"{lang}.yaml").is_file()))
    return results

EASTERN_MARKERS = ["黑发", "黑眼睛", "东亚", "东方", "亚洲", "黄皮肤", "中国面孔"]
FLAG_WORDS = ["国旗", "国徽", "旗帜", "五星红旗", "星条旗", "国歌"]

def check_characters(story):
    """人物形象（v3.0）：characters 存在时查；缺失时跳过（v3.0 之前的旧稿不受影响）。
    每位人物 appearance 非空；character_origin 未写或为 eastern 时，appearance 须含东方标记；
    origin 明确写了其他值时不查标记。"""
    chars = story.get("characters")
    if not chars:
        return []
    origin = story.get("character_origin") or "eastern"
    results = []
    for c in chars:
        ap = (c.get("appearance") or "").strip()
        name = c.get("name") or c.get("id") or "?"
        results.append((f"人物 {name} 形象已写（appearance 非空）", bool(ap)))
        if origin == "eastern":
            results.append((f"人物 {name} 形象含东方标记（默认东方人物）",
                            any(m in ap for m in EASTERN_MARKERS)))
    return results

def check_flags(story):
    """国家形象标志（v3.0）：正文 + 对话里不得出现国旗、国徽、旗帜等。"""
    text = story.get("text", "") + " ".join(t for t, _, _ in dialogue_lines(story))
    hit = [w for w in FLAG_WORDS if w in text]
    return [("画面与文字无国家形象标志（国旗、国徽、旗帜等）", not hit)]

def check_character_sheet(story, base_dir):
    """三视图硬门（v3.1）：有 characters 字段时，character_sheet 必填且文件必须存在。
    相对路径按 story.json 所在目录解析。characters 缺失时跳过，旧稿不受影响。"""
    if not story.get("characters"):
        return []
    sheet = (story.get("character_sheet") or "").strip()
    if not sheet:
        return [("三视图文件已写（字段 character_sheet 非空）", False)]
    p = Path(sheet)
    if not p.is_absolute() and base_dir:
        p = Path(base_dir) / p
    return [("三视图文件存在（character_sheet 指向的文件可读）", p.is_file())]

def check(story, prof, mode="general", base_dir=None):
    text = story.get("text", "") + " ".join(t for t, _, _ in dialogue_lines(story))
    low = text.lower()
    results = []
    results.append(("主角唯一（字段非空）", bool(story.get("protagonist"))))
    results.append(("主题一句话（字段非空）", bool(story.get("theme"))))
    results.append(("目标语言已写清（字段 language 非空）", bool(story.get("language"))))
    results.extend(check_culture(story))
    results.extend(check_language(story, prof["code"]))
    results.extend(check_characters(story))
    results.extend(check_flags(story))
    results.extend(check_character_sheet(story, base_dir))
    if mode == "teaching":
        results.append(("词汇 ≤5 个", len(story.get("vocab", [])) <= 5))
        results.append(("句型 ≤2 个", len(story.get("patterns", [])) <= 2))
        results.append((f"对话每句 ≤{prof['dialogue_max_words']} 词（{prof['code']} 档案）",
                        all(count_words(t, prof["word_unit"]) <= prof["dialogue_max_words"] for t, _, _ in dialogue_lines(story))))
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
    base_dir = str(Path(args[0]).resolve().parent)  # v3.1：三视图相对路径按 story.json 所在目录解析
    print(f"模式：{mode}")
    ok = True
    for name, passed in check(story, prof, mode, base_dir):
        print(("通过 " if passed else "不通过 ") + name)
        ok = ok and passed
    print("结论：" + ("通过" if ok else "不通过，改骨架，不生成视频"))
