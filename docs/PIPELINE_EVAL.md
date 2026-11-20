# 评估：上传 shortvideo-pipeline 与本技能的缺口（v3.22）

日期：2026-11-20。参照物：用户上传 `shortvideo-pipeline.zip`（本地短视频产线，
SKILL.md + scripts/server.py/bootstrap.py + references/9 篇 + assets/project/engine/25 个
Python 文件共 5,599 行 + packs/_template、dao-demon、story-essay、wisdom-dialogue 四个内容包）。

## 结论先行

本技能（v3.21）是**文档丰富、代码薄**：40+ 篇文档、8 张审计表、10 张风格卡、
15 个脚本共 1,117 行，全是校验器，没有一条可执行的端到端产线。上传产线正好反过来：
**代码厚、文档薄**，是一套能跑的本地 CLI 引擎（run → 扩写 → 脚本 → 分镜 → 画布 → 交付包），
带四道质量门与统一退出码 0–5。

缺口不在“想法”，在“可执行”：技能 v3.17–v3.21 定的规则（剧本先行、场景设定板、
角色辨识度、首尾帧连续/切换）都只有文字版，没有代码去算、去拦、去出交付物。
本次 v3.22 按技能模型改写、补齐四件，不照搬产线的内容模型。

## 逐项对照

| 产线能力 | 本技能 v3.21 原状 | v3.22 补齐 | 说明 |
|---|---|---|---|
| storyboard.py：镜表校验 + 旁白/逐镜一致 + 时长模型 + SRT + 时间码 | 无。check_narration.py 只查连续性与时长预估（提示级），不排时间码、不出 SRT | 新增 scripts/storyboard.py | 按技能模型改写：输入 story.json（text+dialogue）与 shots.json（镜头卡），旁白按句切、按段打包，字幕一段一条（与本技能交付一致），不照搬产线“一句一条 ≤26 字”的口播尺子；时长模型沿用 check_narration.py 语速（zh 280 字/分钟）；开口第一分句 ≤8 字（2 秒内开口）；旁白塞不下、超总时长即硬失败 |
| sceneboard.py：场景定义七要素校验 + 图存在性（--strict） | 只有 docs/SCENE_BOARD.md 文字版，无代码 | 新增 scripts/check_sceneboard.py | 七硬项与产线 missing_hard 一致：锚点、三段光、三机位、平面≥3、材质≥4、色板、使用痕迹；--strict 验无人版主图与六格板存在；登记 has_people=true 判不合格 |
| persona.py：角色设定板校验 + 锁脸/重锁 | 只有 docs/CHARACTER_DISTINCTIVENESS.md 文字版，无代码；v3.1 三视图硬门只查文件存在 | 新增 scripts/check_persona.py | DNA 三段式（体态→记号→面料）硬校验 + 设定图存在 + 品牌风格词禁入；--strict 验多角色单列设定图 |
| engine.py lint + 四道门 + 退出码 0–5 | 8 个校验脚本各自为政，无统一入口、无门禁顺序、无退出码约定 | 新增 scripts/lint.py | 按本技能四关卡排序：关卡 1 文字（check_story）→ 关卡 2 画布（check_persona、check_sceneboard）→ 关卡 3 镜头（check_shotcard、check_narration、storyboard --check-only）；默认跑完全部再汇总，--fail-fast 首败即停；退出码 0/1/2/3 |
| script.py / storyboard write_outputs：七件交付包 | 旁白/SRT/时间轴手工拼，无代码 | 并入 storyboard.py（--out-dir） | 出 .srt、旁白-<id>.md（连读 + 逐段时间的码）、shots-timed-<id>.json（每镜起止 + 该段旁白） |
| provenance.py / freshness.py：溯源门 + 保鲜门 | 只有“不确定写‘未确认’”一条文字规则，无登记表、无过期判断 | 未实施（P2） | 只对史实/事实类题材有价值；本技能多数为虚构故事。待有史实题材需要时再加 claim 登记表（source + 日期 + 过期判） |
| repeat_check.py / fingerprint.py：重复门 | 无 | 未实施（P2） | 金句同句/句尾同构判重；虚构故事复用台词少见，优先级低 |
| intake.py / expand.py：一句话 → 母题 → 扩写包 | conceive.py 仅 34 行（极薄） | 未实施（P3） | 技能是 AI 执机（由 Muse 构思），不是本地 CLI；母题 1–5 与钩子机制 M1 是产线内容模型，不宜硬套进通用故事流 |
| selftest.py（39 项） | 无测试 | 未实施（P3） | 新脚本已用正负样本实测（见下）；独立 selftest 可后续补 |
| server.py（HTTP 四接口） | 无 | 不做 | 技能跑在 Muse 内，不走 HTTP；跨平台调用不在本技能边界内 |

## 刻意不搬的东西（及原因）

- 产线内容模型（母题 1–5、钩子机制、payload 配比、豆瓣/微信平台参数、对谈/旁白包形态）：
  产线是“短视频内容号”模型，技能是“通用故事”模型；硬搬等于把技能收窄成内容号工具。
- 产线“不合成 mp4 / 不做 TTS”的边界：产线无 ffmpeg 与 TTS，交付止于素材包；
  本技能恰恰要出视频与旁白（由生成工具做），交付模型不同，不照搬。
- 内容包（packs/*）：产线用 profile.json + semantic 规则 + topics/hooks 驱动选题；
  技能用 ip_modules/ + data/ 驱动风格与语言；包体系可后续再议，不在这次补。

## 自测（2026-11-20，全部通过）

- storyboard.py：nail_biting 真实数据（9 句旁白 35.4s / 60s 成片 / 6 段）通过，
  正确报“旁白短 41%”与“第 6 段静默”两条提醒；负例（30 句旁白塞 3 段）退 1。
- check_sceneboard.py：ant_elephant 两场（森林空地/河边）定义全，通过（非 strict）；
  --strict 因缺六格板图退 1；坏例（缺光/机位/平面/材质/色板/痕迹）退 1 并列出缺项。
- check_persona.py：nail_biting 两角色 DNA 三段式 + 设定图存在，通过；负例（DNA 一段 +
  图不存在）退 1。
- lint.py：nail_biting 三关卡全过，退 0；storyboard 在 lint 内走 --check-only，
  不写文件（修过一次污染：首版 lint 把 story.srt 等写进了 scripts/ 目录，已清掉并加 --check-only）。

## 版本

v3.22（2026-11-20）：分镜时间引擎 + 场景/角色设定板校验 + 统一门禁。
