#!/usr/bin/env python3
"""分镜时间引擎（v3.22）：把 story.json 的旁白/对白按 shots.json 的段落排时间码。

对应上传 shortvideo-pipeline 的 storyboard.py，但按本技能模型改写：
- 输入是技能的 story.json（text 旁白 + dialogue 对白 + language）与 shots.json（镜头卡），
  不是产线的 beats JSON。旁白按“句”切分、按段打包；字幕一镜一段（与本技能交付一致），
  不照搬产线“一句一条 ≤26 字”的口播尺子。
- 时间模型沿用 check_narration.py 的语速：zh 280 字/分钟，en 150 词/分钟，
  ko/ja 300 字/分钟。每段默认 10 秒（--segment-sec 可改）。
- 校验（硬失败退 1）：旁白总时长超过成片时长；某段塞不下；开口第一分句超 8 字
  （2 秒内开不了口）；镜头卡缺必填字段；段号不连续。
- 软提醒（退 0 但打印）：旁白比成片短 20% 以上（留白多）；某句超 40 字（一口气难念）；
  某段只有一镜且旁白为空。
- 产出（--out-dir）：<id>.srt（一段一条字幕）、旁白-<id>.md（连读版 + 逐段
  时间码）、shots-timed-<id>.json（每镜起止时间 + 该段旁白）。

用法：
  python3 scripts/storyboard.py --story story.json --shots shots.json [--out-dir out/<id>]
  python3 scripts/storyboard.py --story story.json --shots shots.json --segment-sec 10 --duration 60
退出码：0 通过｜1 不合格｜2 参数或路径错｜3 就绪度不足（无旁白/无镜头卡）。
"""
import json
import re
import sys
from pathlib import Path

RATES = {"zh": 280, "en": 150, "ko": 300, "ja": 300}
DEFAULT_SEG_SEC = 10.0
MAX_FIRST_CLAUSE = 8          # 开口第一分句 ≤8 字（2 秒内开口）
MAX_SENT_CHARS = 40           # 单句超 40 字只提醒（一口气难念）
LONG_CUE_WARN = 60            # 一段字幕超 60 字只提醒


def split_sentences(text):
    parts = re.split(r"[。？！!?；;.\n]+", text)
    return [p.strip() for p in parts if p.strip()]


def first_clause(s):
    return re.split(r"[，,。？！!?；;.]", s)[0]


def count_units(text, lang):
    if lang == "en":
        return len(text.split())
    return len(re.findall(r"[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]", text))


def dur_of(text, lang):
    rate = RATES.get(lang, 280)
    return count_units(text, lang) / rate * 60.0


def fmt_ts(sec):
    ms = int(round(sec * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def load_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as e:
        print(f"读 {path} 失败：{e}", file=sys.stderr)
        sys.exit(2)


def main():
    argv = sys.argv[1:]
    def opt(name, default=None):
        return argv[argv.index(name) + 1] if name in argv else default
    story_path = opt("--story")
    shots_path = opt("--shots")
    out_dir = opt("--out-dir")
    seg_sec = float(opt("--segment-sec", str(DEFAULT_SEG_SEC)))
    duration = opt("--duration")
    duration = float(duration) if duration else None
    if not story_path or not shots_path:
        print("用法：storyboard.py --story story.json --shots shots.json [--out-dir DIR] [--segment-sec 10] [--duration 60]")
        return 2
    story = load_json(story_path)
    shots = load_json(shots_path)
    if isinstance(shots, dict):
        shots = shots.get("shots") or shots.get("shot_cards") or []
    if not isinstance(shots, list) or not shots:
        print("就绪度不足：shots.json 里没有镜头卡")
        return 3
    check_only = "--check-only" in argv
    lang = (story.get("language") or "zh").strip().lower()
    narration = (story.get("text") or "").strip()
    dialogue = story.get("dialogue") or []
    if not narration and not dialogue:
        print("就绪度不足：story.json 里没有旁白（text）也没有对白（dialogue）")
        return 3

    hard, soft = [], []

    # ---- 镜头卡必填字段（与 check_shotcard.py 的 18 字段一致，v3.24 加 camera_pos、anchor）----
    required = ["id", "segment", "characters", "scale", "angle", "camera_side",
                "move", "camera_pos", "anchor", "comp", "light", "color", "action_start", "action_end",
                "moving", "move_reason", "env", "first", "last", "emotion"]
    segments = sorted({s.get("segment") for s in shots if isinstance(s.get("segment"), int)})
    for i, s in enumerate(shots, 1):
        miss = [k for k in required if s.get(k) in (None, "", [])]
        if miss:
            hard.append(f"第 {i} 镜（id={s.get('id')}）缺字段：" + "、".join(miss))
    if segments != list(range(1, len(segments) + 1)):
        hard.append(f"段号不连续：{segments}，应为 1–{len(segments)} 连续")
    if hard:
        print("不通过：")
        for h in hard:
            print("  - " + h)
        return 1
    n_seg = len(segments)
    video_dur = duration if duration else n_seg * seg_sec
    per_seg_chars = int(RATES.get(lang, 280) / 60 * seg_sec)  # 每段能念的字数（贪心分法用）

    # ---- 旁白按句切分，按段打包 ----
    # 剧本已按段分好旁白时（story.json 的 narration_segments），直接按段取，
    # 不贪心重排——贪心按字数打包会把段 2 的台词塞进段 1。没给时才按字数贪心分。
    sents = split_sentences(narration) if narration else []
    seg_narration = story.get("narration_segments")
    if seg_narration and len(seg_narration) == n_seg:
        plan = [split_sentences(s) for s in seg_narration]
        # 校验：按段旁白拼起来须等于全文（逐字一致，标点除外）
        flat = re.sub(r"[^\u4e00-\u9fa5A-Za-z0-9]", "", "".join("".join(p) for p in plan))
        whole = re.sub(r"[^\u4e00-\u9fa5A-Za-z0-9]", "", "".join(sents))
        if flat != whole:
            hard.append("narration_segments 拼起来与 text 全文不一致：有句子漏了或被改了")
            print("不通过：")
            for h in hard:
                print("  - " + h)
            return 1
        sents = [s for p in plan for s in p]
    else:
        plan = [[] for _ in range(n_seg)]  # 每段分到的句子
        seg_idx = 0
        cur_chars = 0
        for s in sents:
            n = count_units(s, lang)
            if n > MAX_SENT_CHARS:
                soft.append(f"单句超 {MAX_SENT_CHARS} 字（一口气难念）：「{s}」")
            if cur_chars + n > per_seg_chars and plan[seg_idx]:
                seg_idx += 1
                cur_chars = 0
                if seg_idx >= n_seg:
                    hard.append(f"旁白塞不下：{n_seg} 段×{seg_sec:.0f} 秒放不下 {len(sents)} 句旁白，"
                                "砍旁白或加段")
                    break
            plan[seg_idx].append(s)
            cur_chars += n
        if hard:
            print("不通过：")
            for h in hard:
                print("  - " + h)
            return 1
    # 单句超长提醒（两种分法都查）
    for s in sents:
        if count_units(s, lang) > MAX_SENT_CHARS:
            soft.append(f"单句超 {MAX_SENT_CHARS} 字（一口气难念）：「{s}」")

    # ---- 时长与开口 ----
    total_nar = sum(dur_of(s, lang) for s in sents)
    if total_nar > video_dur:
        hard.append(f"旁白总时长 {total_nar:.1f}s 超过成片 {video_dur:.1f}s，砍旁白或加段")
    elif video_dur and (video_dur - total_nar) / video_dur > 0.2:
        soft.append(f"旁白 {total_nar:.1f}s，比成片 {video_dur:.1f}s 短 {(video_dur - total_nar) / video_dur * 100:.0f}%"
                    "（留白多：加长旁白或接受静默）")
    if sents:
        fc = first_clause(sents[0])
        if count_units(fc, lang) > MAX_FIRST_CLAUSE:
            hard.append(f"开口超时：首句第一分句「{fc}」{count_units(fc, lang)} 字，"
                        f"2 秒内开不了口——压到 {MAX_FIRST_CLAUSE} 字以内")
    for i, ss in enumerate(plan, 1):
        joined = "".join(ss)
        if len(joined) > LONG_CUE_WARN:
            soft.append(f"第 {i} 段字幕 {len(joined)} 字（> {LONG_CUE_WARN} 字），10 秒内读完偏赶")
        if not ss:
            soft.append(f"第 {i} 段没有旁白（静默段：确认是有意留白）")
    if hard:
        print("不通过：")
        for h in hard:
            print("  - " + h)
        return 1

    # ---- 产出（--check-only 时只校验，不写文件）----
    if check_only:
        print(f"旁白 {len(sents)} 句 / {total_nar:.1f}s，成片 {video_dur:.1f}s，{n_seg} 段")
        for w in soft:
            print("提醒", w)
        print("结论：通过（--check-only，未写文件）")
        return 0
    stem = Path(story_path).stem
    if out_dir:
        out = Path(out_dir)
        out.mkdir(parents=True, exist_ok=True)
    else:
        out = Path(".")
    # SRT：一段一条（句与句之间补回句号，方便阅读）
    def join_sents(ss):
        return "。".join(ss) + "。" if ss else ""
    srt_lines = []
    for i, ss in enumerate(plan, 1):
        if not ss:
            continue
        start = (i - 1) * seg_sec
        end = i * seg_sec
        srt_lines.append(f"{len(srt_lines) + 1}\n{fmt_ts(start)} --> {fmt_ts(end)}\n{join_sents(ss)}\n")
    (out / f"{stem}.srt").write_text("\n".join(srt_lines), encoding="utf-8")
    # 旁白时间码
    md = [f"# 旁白时间码（{stem}）\n", f"总旁白 {total_nar:.1f}s / 成片 {video_dur:.1f}s / {n_seg} 段 × {seg_sec:.0f}s\n"]
    for i, ss in enumerate(plan, 1):
        md.append(f"\n## 段 {i}（{fmt_ts((i - 1) * seg_sec)[:8]}–{fmt_ts(i * seg_sec)[:8]}）\n")
        md.append(join_sents(ss) if ss else "（静默）")
        md.append("\n")
    (out / f"旁白-{stem}.md").write_text("".join(md), encoding="utf-8")
    # 每镜时间码
    timed = []
    for s in shots:
        seg = s["segment"]
        timed.append({**s, "t_start": (seg - 1) * seg_sec, "t_end": seg * seg_sec,
                      "narration": join_sents(plan[seg - 1])})
    (out / f"shots-timed-{stem}.json").write_text(
        json.dumps(timed, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"旁白 {len(sents)} 句 / {total_nar:.1f}s，成片 {video_dur:.1f}s，{n_seg} 段")
    for w in soft:
        print("提醒", w)
    print(f"已出：{stem}.srt、旁白-{stem}.md、shots-timed-{stem}.json（→ {out}）")
    print("结论：通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
