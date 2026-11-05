#!/usr/bin/env python3
"""单词高亮发音：输入词汇表 JSON，输出高亮文本 + ASS 字幕骨架。
词汇表 JSON：[{"word": "画", "pinyin": "huà", "meaning": "drawing"}, ...]
用法：python highlight_words.py vocab.json "这是给你的画，谢谢你。"
ASS 时间轴需在配音完成后按实际音频对齐，本脚本只出骨架，不编时间。
"""
import sys, json

def highlight(text, vocab):
    out = text
    for v in vocab:
        w = v["word"]
        pron = v.get("pinyin") or v.get("ipa") or ""
        out = out.replace(w, f"**{w}（{pron}）**")
    return out

def ass_skeleton(vocab):
    lines = ["[Script Info]", "ScriptType: v4.00+", "",
             "[V4+ Styles]", "Format: Name, Fontname, Fontsize, PrimaryColour",
             "Style: Default,Arial,24,&H00FFFFFF", "",
             "[Events]", "Format: Start, End, Style, Text"]
    for v in vocab:
        w = v["word"]
        lines.append(f"Dialogue: 0:00:00.00,0:00:02.00,Default,,0,0,0,,{{\\c&H00FFFF&}}{w}{{\\c&H00FFFFFF&}}")
    return "\n".join(lines)

if __name__ == "__main__":
    vocab = json.load(open(sys.argv[1], encoding="utf-8"))
    text = sys.argv[2] if len(sys.argv) > 2 else ""
    print(highlight(text, vocab))
    print("\n--- ASS 骨架 ---")
    print(ass_skeleton(vocab))
