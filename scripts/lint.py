#!/usr/bin/env python3
"""统一门禁（v3.22）：按关卡顺序跑全部校验，汇总退出码。

对应上传 shortvideo-pipeline 的 engine.py lint + 四道门顺序（结构→溯源→保鲜→投产），
按本技能四关卡改写：
  关卡 1 文字：check_story.py（故事 JSON：三视图硬门、文化锚点、语言锁、场景模板……）
  关卡 2 画布：check_sceneboard.py（场景七要素 + 图存在）与 check_persona.py（DNA 三段式 + 设定图）
  关卡 3 镜头：check_shotcard.py（镜头卡 16 字段 + 首尾帧连续/切换）与
              check_narration.py（旁白连续性 + 时长预估）与 storyboard.py（分镜时间码 + SRT）
每关卡独立计分；任一关卡不合格即整单不合格（退 1），但默认跑完所有关卡再汇总，
让一次运行看到全部问题。--fail-fast 时第一关失败即停。

用法：
  python3 scripts/lint.py --story story.json --shots shots.json [--scenes canvas/scenes.json]
      [--narration narration.txt] [--base-dir .] [--strict] [--fail-fast]
  --story 必填；--shots、--scenes、--narration 缺省时跳过对应关卡并注明。
退出码：0 全部通过｜1 不合格｜2 参数或路径错｜3 就绪度不足（缺 story.json 或缺 shots.json）。
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def run(script, args):
    p = subprocess.run([sys.executable, str(HERE / script), *args],
                       capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr).strip()


def main():
    argv = sys.argv[1:]
    def opt(name, default=None):
        return argv[argv.index(name) + 1] if name in argv else default
    story = opt("--story")
    shots = opt("--shots")
    scenes = opt("--scenes")
    narration = opt("--narration")
    base_dir = opt("--base-dir", ".")
    strict = "--strict" in argv
    fail_fast = "--fail-fast" in argv
    if not story:
        print("用法：lint.py --story story.json [--shots shots.json] [--scenes canvas/scenes.json] "
              "[--narration narration.txt] [--base-dir .] [--strict] [--fail-fast]")
        return 2
    if not Path(story).exists():
        print(f"找不到 story.json：{story}")
        return 2

    gates = []  # (gate_name, [(label, rc, output)])
    overall = 0

    def gate(name, steps):
        nonlocal overall
        results = []
        failed = False
        for label, script, args in steps:
            rc, out = run(script, args)
            results.append((label, rc, out))
            if rc != 0:
                failed = True
                overall = 1
                if fail_fast:
                    break
        gates.append((name, results, failed))
        return not failed

    # 关卡 1：文字
    gate("关卡 1 文字", [
        ("check_story", "check_story.py", [story]),
    ])
    # 关卡 2：画布
    steps2 = [("check_persona", "check_persona.py",
               ["--story", story, "--base-dir", base_dir] + (["--strict"] if strict else []))]
    if scenes:
        steps2.append(("check_sceneboard", "check_sceneboard.py",
                       ["--scenes", scenes, "--pack-dir", base_dir] + (["--strict"] if strict else [])))
    gate("关卡 2 画布", steps2)
    # 关卡 3：镜头
    steps3 = []
    if shots:
        steps3.append(("check_shotcard", "check_shotcard.py", [shots]))
        steps3.append(("storyboard", "storyboard.py",
                       ["--story", story, "--shots", shots, "--check-only"]))
    if narration:
        steps3.append(("check_narration", "check_narration.py", [narration]))
    if steps3:
        gate("关卡 3 镜头", steps3)

    for name, results, failed in gates:
        print(f"\n{'=' * 10} {name}：{'不通过' if failed else '通过'} {'=' * 10}")
        for label, rc, out in results:
            print(f"--- {label}（退出 {rc}）---")
            print(out if out else "（无输出）")
    print(f"\n结论：{'不通过，改完再进下一关' if overall else '全部通过'}")
    return overall


if __name__ == "__main__":
    sys.exit(main())
