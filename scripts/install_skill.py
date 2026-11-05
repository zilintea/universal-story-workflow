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
        skill = open(os.path.join(args.src, "SKILL.md"), encoding="utf-8").read()
        safety = open(os.path.join(args.src, "docs", "CHILD_SAFETY.md"), encoding="utf-8").read()
        out = "# Universal Story Workflow (GPT Instructions)\n\n" + skill + "\n\n" + safety
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
