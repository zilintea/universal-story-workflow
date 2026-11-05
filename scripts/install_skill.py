#!/usr/bin/env python3
"""导入技能到不同模型/平台：复制仓库或生成 GPT Instructions。
用法：
  python3 scripts/install_skill.py --target muse [--dry-run]
  python3 scripts/install_skill.py --target claude [--dry-run]
  python3 scripts/install_skill.py --target workbuddy [--dry-run]
  python3 scripts/install_skill.py --target gpt --out ./gpt_instructions.md
"""
import argparse, os, shutil, sys

TARGETS = {
    "muse": os.path.expanduser("~/workspace/custom-skills/universal-story-workflow"),
    "claude": os.path.expanduser("~/.claude/skills/universal-story-workflow"),
    "workbuddy": os.path.expanduser("~/workspace/custom-skills/universal-story-workflow"),
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", required=True, choices=["muse", "claude", "workbuddy", "gpt"])
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--out", default="./gpt_instructions.md")
    ap.add_argument("--src", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    args = ap.parse_args()
    if args.target == "gpt":
        # v2.3 修正：GPT 输出不再附安全说明文件（安全只是说明文件，不参与审计）；
        # GPT 没有本地脚本执行环境，审计用 checklists/ 逐项文字自查代替脚本输出。
        skill = open(os.path.join(args.src, "SKILL.md"), encoding="utf-8").read()
        note = ("\n\n## GPT 适配说明\n"
                "- 本平台没有本地脚本执行环境：scripts/*.py 不能运行，"
                "审计用 checklists/ 逐项文字自查代替脚本输出（逻辑、语言、剪辑、镜头卡、旁白连续性各一份表）。\n"
                "- 安全只是说明文件（docs/CHILD_SAFETY.md），不参与审计，不附在这里；需要时用户会另外给。\n"
                "- 确认关卡不变：文字、画布、试点、批量四道关，每道都要用户点头才进下一步。\n")
        out = "# Universal Story Workflow (GPT Instructions)\n\n" + skill + note
        if args.dry_run:
            print(f"GPT instructions would be written to {args.out} ({len(out)} chars)")
        else:
            open(args.out, "w", encoding="utf-8").write(out)
            print(f"Wrote {args.out} ({len(out)} chars)")
        return
    dest = TARGETS[args.target]
    if args.dry_run:
        print(f"Dry run: copy {args.src} -> {dest}")
        return
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(args.src, dest, ignore=shutil.ignore_patterns(".git", "__pycache__"))
    print(f"Installed to {dest}")

if __name__ == "__main__":
    main()
