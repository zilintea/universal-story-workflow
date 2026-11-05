# 人物审计（v3.0 新增，见 docs/CHARACTER_CONSISTENCY.md、docs/CHARACTER_DEFAULTS.md）

- [ ] 每位出场人物三视图已锁定（正面 / 侧面 / 背面），故事板和视频只沿用，不重新发明外形
- [ ] 三视图硬门（v3.1）：故事 JSON 的 `character_sheet` 字段已写三视图文件路径，文件存在（脚本 scripts/check_story.py 输出）；有 `characters` 字段时缺字段、路径为空、文件不存在，任一即不通过，不进故事板
- [ ] 参考图规则（v3.1）：故事板生成时传三视图当人物参考图；视频生成的人物参考图必须是三视图，不许拿 9 格故事板当人物参考；第一段试点没有上一段尾帧时用三视图当参考图
- [ ] 角色 DNA 一句话，之后每段提示词逐字复用，一字不改（脚本 scripts/character_check.py 输出）
- [ ] 人物形象默认值（v3.0）：人物类剧集用户没特别指定时，形象一律东方人物（东亚面孔、黑发、黑眼睛），写进角色表“形象”栏和 DNA；用户明确指定其他背景时写指定的
- [ ] 故事 JSON 的 `characters` 字段：每位人物 `appearance` 非空；`character_origin` 未写或为 `eastern` 时 `appearance` 含东方标记（黑发/黑眼睛/东亚/东方/亚洲/黄皮肤/中国面孔之一）；`origin` 明确写了其他值时不查标记（脚本 scripts/check_story.py 输出）
- [ ] 成片帧对照三视图验收：颜色、体型、标志物、比例任一项漂移即不通过，重生成
