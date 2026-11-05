# CHANGELOG

## v1.2 (2026-11-05) — 英语启蒙修正版
- 修正 v1.1 的关键错误：目标语言从中文改为英语。英语启蒙系列小故事，面向中文母语儿童。
- 新增：生活场景主题库（火灾、过马路、陌生人、洗手、触电、玩水），每集必须有警示点和教学点。
- 新增：语言审计硬项——目标语言是否为英语、警示行为是否正确。
- 修正：check_story.py 英文词按词边界、不区分大小写计数，对话上限改为 ≤8 词。
- 新增示例：examples/fire-english-text.md（《Fire! Run First!》），上一版中文火灾故事稿作废。

## v1.1 (2026-11-05)
- GitHub 仓库版：自我构思、画布、情节编排、单词高亮发音、全面评估。

## v1.3 (2026-11-05) — 分镜单独交付版
- 新增：分镜单独成片，合并由用户选（默认不合并）。
- 新增：音频单独生成、单独成文件（旁白、对话分开）。
- 新增：内嵌字幕（ASS burn-in，关键词黄色），内嵌版与无字幕原片分开保存。
- 新增：每段必须动起来；一段失败时改用更安全讲法重拍（例如只拍烟、不拍明火特写），静态桥接只能作临时占位。
- 新增文档：docs/VIDEO_DELIVERY.md、docs/AUDIO_DELIVERY.md、docs/SUBTITLES.md。

## v1.4 (2026-11-05) — 一致性 + 剪辑标准版
- 新增：人物/物品/场景三张锁定表，故事开始前写死，故事中不改。
- 新增：分镜转场一致性禁令，逐对核对人物/物品/场景/时间/背景，禁止物品瞬移、场景无故变色、服装无故变、背景角色无故出现/消失。
- 改版：字幕改为单独的、带时间戳的文件（默认 SRT，教学用 ASS），不内嵌进视频；v1.3 内嵌字幕默认作废，烧录版只在用户明确要求时另出。
- 脚本自我评估按影视剪辑标准改写：新增 scripts/edit_check.py，查 180 度轴线、30 度规则、动作匹配、视线匹配、景别节奏、转场类型、物品/场景连续；实测好分镜通过、坏分镜（物品瞬移、轴线翻转、跳切、场景硬切）被拦下。
- 新增文档：docs/CONTINUITY.md、docs/EDITING_STANDARDS.md、docs/SCRIPT_EVALUATION.md、checklists/continuity_audit.md，示例：examples/fire_en_subtitles.srt。

## v1.5 (2026-11-05) — 少儿影视标准版
- 再评估：按少儿影视标准重评，旧版安全系统、世界/时间线、规模伸缩、Token 优化、多模型五项不足，综合从通用标准 4.4 下调到少儿影视标准约 3.2，新版目标补到 4.5 以上，安全线一票否决。
- 新增：少儿安全线 8 条（CHILD_SAFETY.md），宏大叙事世界空间与完整时间线（WORLD_TIMELINE.md），剧集/电影/短视频三种规模与横竖屏选择（FORMATS.md），动画制作标准流程（ANIMATION_PIPELINE.md）。
- 新增：Token 优化（TOKEN_OPTIMIZATION.md + templates/compact_story.txt + scripts/token_check.py，实测紧凑模板 789 字符 vs 散文示例 2297 字符）。
- 新增：多模型自适应（MODEL_ADAPTER.md + scripts/install_skill.py，支持 Muse / Claude / WorkBuddy / GPT，含导入命令，dry-run 实测通过）。
- 新增评估：docs/EVALUATION_CHILDREN_FILM.md、docs/SCRIPT_EVALUATION.md（v1.4 已有，v1.5 沿用）。
