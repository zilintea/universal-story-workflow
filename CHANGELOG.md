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

## v1.9（2026-11-05，镜头语言 + 旁白连续 + 风格档案版）
- 新增 docs/IP_MANUAL.md：用户提供的《IP 故事短片创作全要素手册（提示词封装版）》全文，作为补充修正；品牌名只作选择简称，不进提示词。
- 新增 docs/SHOT_LANGUAGE.md + scripts/check_shotcard.py：镜头卡 14 字段（景别/机位/运镜/构图/光线/色彩/动作起—中—止/环境动态/首尾帧/情绪），首尾帧锁定 SOP（上一段尾帧当参考图，`Continue from this exact frame.`），试点已验（旧纯文字版背景跑到集市、人换了；镜头卡+尾帧版同人同景，勉强可以）。
- 新增 docs/NARRATION_CONTINUITY.md + scripts/check_narration.py：旁白轨与教学轨分开，旁白一整段连续自然语言，时间、地点、主语至少两项连续，剪辑点落在句子中间；连续短句跳跃、相邻断档、词汇罗列即不通过。
- 新增 data/styles/：ghibli、pixar3d、stopmotion、liveaction、inkwash、cel2d 六张风格档案，每张只写描述性字段，品牌名只在 alias 栏作简称。
- 新增 docs/WORLD_MAP.md：第 0 步世界空间线（地点线、时间线、世界规则），中国典故、美国故事都先画地图再写故事。
- 新增 docs/TOKEN_BUDGET.md：先试点 1 段再批量、只传编号不传全文、只重做错段、镜头卡短码；换平台前先报成本。教训：一个视频在豆包上测试，一个月用量一次用完。
- 审计变八审计：安全+逻辑+语言+剪辑+人物+场景+流程+旁白连续性。

## v2.0（2026-11-05，通用剧集脚本版）
- 定位升级：从少儿动画/语言启蒙升级为通用剧集脚本，适用剧集、电影、短视频、系列预告、世界观概念片、角色登场片，题材不限（中国典故、美国故事、原创 IP），受众默认通用观众；语言教学、少儿动画只是其中两种模式。
- 安全线改为可选模块，默认不加载（新增 docs/SAFETY_OPTIONAL.md）：只有用户明确说小朋友/少儿/教学或“开安全线”时，才加载 docs/CHILD_SAFETY.md 的 8 项并作为第一审计、一票否决；默认审计为逻辑+语言+剪辑+人物+场景+流程+旁白连续性七审计。
- README 顶部重写：30 秒安装（install_skill.py 四种目标/手动复制）、怎么使用（先文字后视频）、怎么调用（一句话 + 5 个调用示例）、默认值。
- skill.yaml 描述同步改为通用剧集脚本。

## v2.1（2026-11-05，全场景通用版，修正 v2.0 理解错误）
- 安全只是技能里的说明文件（docs/SAFETY_OPTIONAL.md、docs/CHILD_SAFETY.md），默认不加载，不参与审计，不当关卡，不一票否决；审计链里没有安全，审计仍为逻辑+语言+剪辑+人物+场景+流程+旁白连续性七审计。
- 主流程不预设少儿、语言教学、生活场景：生活场景主题库、词汇/句型/警示点要求从 SKILL.md 主流程移出，另存为可选模式 docs/TEACHING_MODE.md，只有用户明确说语言教学/英语启蒙/给小朋友看时才用。
- 文字输出模板改为通用版（不再是英语启蒙版）；交付、归档、对话分工、禁止事项里的教学默认值同步改为通用，教学项只在教学模式时出现。

## v2.2（2026-11-05，短视频默认 30 秒版）
- 短视频默认时长从 60 秒改为 30 秒：文字 30 秒、视频 30 秒，短视频 10–90 秒可选，30 秒 = 3 段 × 10 秒；SKILL.md、docs/FORMATS.md、templates/、docs/TOKEN_BUDGET.md、docs/IP_MANUAL.md 的备注同步改。
- README.md 按最新说明重写：默认值 30 秒、调用示例去掉“开安全线”（安全只是说明文件）、仓库结构与 v2.1/v2.2 对齐、审计七项（审计链里没有安全）。

## v2.3（2026-11-05，确认关卡 + 多模型版，用户要求按逻辑再评估、补遗漏）
- 补四道确认关卡（docs/EVALUATION_V23.md 第 1–3 项）：文字→画布→试点→批量，缺一不可；画布先出、用户确认才进视频，试点给用户看过、点头后才批量；批量段数修正为剩下 2 段（默认 30 秒共 3 段，60 秒才 5 段）。
- check_story.py 默认通用模式（--mode general|teaching）：警示点、词汇频次只在教学模式查，通用故事没警示点不再被打回（实测修正）。
- GPT 安装修正：install_skill.py 的 GPT 输出不再附 CHILD_SAFETY.md，改为 SKILL.md + GPT 适配说明，审计用 checklists/ 文字自查；MODEL_ADAPTER 的“双审计、三审计”改为七审计、四道确认关卡。
- 检查表补齐：新增 checklists/narration_audit.md、shotcard_audit.md；continuity_audit.md 补首尾帧衔接、镜头卡完整；logic_audit.md 去 IP 专属项（能力第二次更夸张、不沾蜜等）；language_audit.md 标明只在教学模式查。
- 模板去教学默认值：templates/episode_brief.md 的“目标语言默认中文”“难度默认初级”“受保护物品”改为通用；skill.yaml 加 triggers；SKILL.md 乱码标题“对话与旁白���工”修正。
- 自评：v2.2 约 3.4，v2.3 约 4.5，见 docs/EVALUATION_V23.md；诚实短板：GPT 等无脚本环境只能文字自查，成片帧验收仍靠人工抽帧。

## v2.4（2026-11-05，参数化版，用户要求删除固定编码、README 顶部写操作重点和引用模式）
- 参数化：时长、段数、格数、画幅全部改为参数。成片时长 D 用户指定（如直出 60 秒），没说默认 30 秒；段数 N = D ÷ 10；格数 G = N × 3；文字时长 = D。SKILL.md 顶部新增参数表，通用性硬规则扩展为“禁止写死任何数值”。
- README.md 顶部新增操作重点（六条）和引用模式（只传编号，不传全文）两节，参数表同步到 README 顶部。
- make_canvas.py 支持 --panels G（格数参数化）；TOKEN_BUDGET.md 预算表按 D 算；模板里的时长改为 D。
