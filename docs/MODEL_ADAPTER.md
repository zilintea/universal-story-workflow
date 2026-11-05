# 多模型自适应（GPT / WorkBuddy / Claude / Muse）

## 原则
- 流程、标准、审计表是模型无关的，不改。
- 适配层只改三样：技能文件放哪里、调用命令怎么写、输出格式怎么对齐（JSON / Markdown）。

## 导入命令（引入脚本技能命令）

### Muse（本仓库默认）
```bash
git clone <你的仓库地址> universal-story-workflow
cp -r universal-story-workflow ~/workspace/custom-skills/
# 入口：~/workspace/custom-skills/universal-story-workflow/SKILL.md
```

### Claude
```bash
git clone <你的仓库地址> universal-story-workflow
cp -r universal-story-workflow ~/.claude/skills/
# 在 Claude 里说：用 universal-story-workflow 技能，出一集……
```

### GPT（自定义 GPT / 项目指令）
```bash
git clone <你的仓库地址> universal-story-workflow
# 把 universal-story-workflow/SKILL.md 全文粘贴到 GPT 的 Instructions 里
# 或把仓库作为项目知识库上传，提示词写：按 universal-story-workflow 的 SKILL.md 流程走
```

### WorkBuddy
```bash
git clone <你的仓库地址> universal-story-workflow
# 把仓库交给 WorkBuddy，指令写：一句话主题，按 universal-story-workflow 的 SKILL.md 跑完文字第一、七审计、四道确认关卡
# WorkBuddy 自主执行的部分：写文字稿、跑审计脚本、生成故事板提示词
```

### 一键导入脚本（推荐）
```bash
python3 scripts/install_skill.py --target muse
python3 scripts/install_skill.py --target claude
python3 scripts/install_skill.py --target workbuddy
python3 scripts/install_skill.py --target gpt --out ./gpt_instructions.md
```
- `--target muse/claude/workbuddy`：复制整个仓库到对应技能目录（dry-run 时加 `--dry-run`，只打印路径不复制）
- `--target gpt`：不复制目录，生成一份可粘贴的 Instructions 文件（SKILL.md + GPT 适配说明，紧凑版；不附安全说明文件，审计用 checklists/ 文字自查代替脚本）
- 适配差异：GPT 没有本地脚本执行环境时，审计表用文字自查代替脚本输出；Claude / WorkBuddy / Muse 有本地执行环境时，优先跑 scripts/edit_check.py 和 check_story.py 的实际输出
