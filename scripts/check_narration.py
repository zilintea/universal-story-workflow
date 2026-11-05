#!/usr/bin/env python3
"""旁白连续性审计（v1.9）：旁白轨一整段连续自然语言，句子不跳跃。
用法：python3 scripts/check_narration.py narration.txt [--words a,b,c]
输入：每句一行（或一段按句号/问号/感叹号切分）。
查：1) 连续短句跳跃；2) 相邻两句时间/地点/主语三者至少两项连续；
3) 词汇表式罗列。词表只按本集锁定表查，不写死具体词。
"""
import re, sys, json

def split_sentences(text):
    parts = re.split(r'[。？！；\n]+', text)
    return [p.strip() for p in parts if p.strip()]

def main():
    path = sys.argv[1]
    text = open(path, encoding='utf-8').read()
    sents = split_sentences(text)
    fails = []
    # 1) 连续短句：中文 <6 字且连续 3 句以上
    run = 0
    for s in sents:
        run = run + 1 if len(s) < 6 else 0
        if run >= 3:
            fails.append(f"连续短句跳跃：{sents}")
            break
    # 2) 相邻两句共享词：时间/地点/主语，任一词重叠即算一项连续；
    # 简化为：相邻两句至少共享 1 个长度>=2 的词（不含标点），否则判断档
    for a, b in zip(sents, sents[1:]):
        wa = {a[i:i+2] for i in range(len(a)-1)}
        wb = {b[i:i+2] for i in range(len(b)-1)}
        if not (wa & wb):
            fails.append(f"相邻两句断档（无共享词）：「{a}」→「{b}」")
    # 3) 词汇罗列：同一句里目标词 >=3 且无动词连接（简化：句长<15 且含 >=3 个逗号分隔的词）
    if '--words' in sys.argv:
        words = sys.argv[sys.argv.index('--words')+1].split(',')
        for s in sents:
            hit = [w for w in words if w in s]
            if len(hit) >= 3 and len(s) < 20:
                fails.append(f"词汇表式罗列：{s}（{hit}）")
    print(f"旁白 {len(sents)} 句")
    for f in fails:
        print("不通过", f)
    print("结论：" + ("不通过，改旁白，不进视频" if fails else "通过"))

if __name__ == '__main__':
    main()
