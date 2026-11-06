# IP 故事短片创作全要素手册（提示词封装版）

> 来源：用户 2026-11-05 提供，作为通用故事工作流 v1.9 的补充修正。
> 用途：写脚本、拆分镜、封装图生图 / 图生视频 / 文生视频提示词时逐条查表。
> 读法：第 1–2 章定“讲什么”，第 3–4 章定“怎么拍”，第 5–7 章定“长什么样”，第 8 章直接抄公式。
> 品牌名规则（用户定）：品牌名是选风格的简称，不直接写进提示词。提示词只写描述性字段（见 `data/styles/`），品牌名只出现在风格选择的简称里。

## 目录

0. 三种速查表（先看这个）
1. IP 短片的类型与任务定位
2. 剧情发展：结构、节拍、钩子、结尾
3. 镜头语言：景别 / 机位 / 运镜 / 构图 / 光线 / 色彩 / 剪辑
4. 角色设定技术要点
5. 常用拍摄手法 16 式
6. 动画风格谱系
7. 影视风格谱系
8. 提示词封装：公式、模板、词库、参数表、一致性 SOP
9. 交付前质检清单

## 0. 三种速查表

### 0.1 时长—节拍速查（最重要）

| 时长 | 镜头数 | 结构拆法 | 节拍点 | 适用 |
|---|---|---|---|---|
| 6s | 1–2 | 单事件 | 0–1s 异常 / 1–4s 爆发 / 4–6s 落点 | 开屏、信息流、封面 |
| 15s | 6–9 | 钩子→升级→高潮→落点 | 0–3 / 3–9 / 9–13 / 13–15 | 抖音、视频号主力 |
| 30s | 8–14 | 微三幕 | 0–3 钩 / 3–12 建立+激励 / 12–20 对抗 / 20–27 高潮 / 27–30 收 | 品牌短片、IP 预告 |
| 60s | 16–25 | 标准三幕 | 每 15s 一个节拍 | 官方 PV、概念片 |
| 90–120s | 25–40 | 三幕 + 一条暗线 | 每 20–30s 一个节拍 | 世界观概念片、系列预告 |

注：本技能短视频默认 30 秒，按 3 段 × 10 秒交付（每段一段视频），镜头数以分镜卡计，不以生成段数计；手册 0.1 里 60 秒 16–25 镜是分镜密度目标，生成时多镜可合在一段里用运镜完成。

### 0.2 情绪—镜头速查

| 要的情绪 | 首选镜头语言 |
|---|---|
| 孤独、渺小、世界观体量 | 大远景 + 人物占画幅 <1/8 + 高地平线 + 冷调 |
| 压迫、威权、英雄感 | 仰角 + 广角近身 + 硬光 + 低机位贴地 |
| 亲密、共情 | 85mm 中近景 + 柔光 + 浅景深 + 平视 |
| 不安、崩坏 | 荷兰角 + 手持 + 冷绿/洋红双色 + 颗粒 |
| 悬念 | 大特写局部（眼、手、门缝）+ 框架构图 + 遮挡 |
| 速度、爽感 | 低机位贴地 + 甩镜 + 一级动作跟拍 + 高帧率慢放 |
| 仪式感、史诗 | 对称构图 + 低机位 + 逆光轮廓 + 上升运镜 + 升格 |
| 温情收束 | 缓推 + 暖色 3200K + 上升/后拉 + 环境声留白 |

### 0.3 一句话镜头公式（写分镜就套这个）

```
[景别] + [机位/角度] + [运镜(速度+方向)] + 主语 + 动作 + 环境动态 + [光线] + [情绪落点]
```

例：`大特写 / 平视 / 缓推 2cm-per-sec / 少女瞳孔 / 映出一座燃烧的城市 / 单侧冷蓝实用光 / 认知崩塌`。

## 1. IP 短片的类型与任务定位

写之前先定“这片子替 IP 干什么活”，四种任务对应四套叙事骨架：

| 类型 | 任务 | 骨架 | 镜头偏好 | 失败症状 |
|---|---|---|---|---|
| **角色登场片**（Character Reveal） | 让人记住一张脸 | 局部特写堆叠 → 全貌揭示 → 标志动作 → 定格 | 大特写为主，最后一镜才给全景 | 一上来就给全身，观众记不住 |
| **世界观概念片**（Concept / Mood Film） | 立规则、立氛围 | 环境空镜 → 异常入侵 → 规则显形 → 尺度揭示 | 大远景、航拍、长焦压缩、无人称视角 | 只有风景没有人，看完不知谁在活 |
| **品牌 / 产品形象片** | 把符号卖给情绪 | 痛点 → 反差 → 产品作为解 → 金句收 | 商业级光、微距材质、机械臂 | 产品出现太晚或太像广告 |
| **系列预告 / PV** | 造“下一集必须看” | 三个碎片事件 → 共同威胁 → 名字/日期落下 | 快切、卡点、甩镜、遮罩转场 | 信息过载，没有一处留白 |

**IP 短片与普通短片的分歧点**（直接影响创作决策）：

1. **角色即品牌**——每个镜头都要能单独截成海报或头像。
2. **动作即人设**——不解释性格，只让性格在一次动作里暴露（擦桌角、扶眼镜、数硬币）。
3. **道具即符号**——全片只允许 1 件反复出现的标志物（伞、怀表、耳机、机械臂）。
4. **台词上限 3 句**——第 1 句给情境，第 2 句给冲突，第 3 句是金句，放最后 2 秒。
5. **信息密度**：每 8–10 秒必须换一次信息层级（景别跳变 / 场景跳变 / 情绪跳变），否则划走。

## 2. 剧情发展

### 2.1 三条铁律

1. **一个片子只讲一个动词**。整片压缩成一句“她为了 X，做了 Y”，多一个动词就砍。
2. **前 3 秒必须是“未完成状态”**——动作做了一半、问题没解决、视线指向画外。完成态没有钩子。
3. **结尾必须重构开头**。同一个构图、同一句台词、同一件道具，含义变了，片子的“故事感”就成立。

### 2.2 冲突公式

```
张力 = 想要（Want）× 阻碍（Obstacle）× 代价（Stake）
```

- Want 必须可视化：不是“想变强”，而是“想够到那盏灯”。
- Obstacle 分三层，短片只用最外层：物理（门锁着）／关系（对方不认）／自我（手在抖）。
- Stake 用画面给，不用台词说：镜头扫一眼倒计时、一张照片、空掉的钱包。

### 2.3 十分钟能写完的骨架（推荐用于 30–60s）

| 步骤 | 内容 | 时长占比 | 镜头要求 |
|---|---|---|---|
| 1 常态 | 一个可辨识的日常，1 个细节暗示不安 | 15% | 一个固定的“母镜头”（后面要重复） |
| 2 激励 | 一个异物闯入常态（人、光、声音、裂缝） | 10% | 用景别突变，不用特效堆 |
| 3 拒绝 | 主角第一次尝试失败，暴露弱点 | 20% | 动作被打断，留 0.5s 空镜 |
| 4 升级 | 阻碍加码，代价显形（第二次尝试更狠） | 25% | 运镜加速、剪辑变短、音乐升 key |
| 5 抉择 | 主角主动选择付出代价 | 15% | 全片唯一一次特写停顿（2s） |
| 6 重构 | 回到步骤 1 的构图，但世界/角色已不同 | 15% | 同机位同焦段，只改光和色 |

这套骨架的好处：**镜头可以复用**，AI 生成时“同机位同构图”是最省成本、最出效果的反转手法。

### 2.4 钩子类型（0–3s 用哪个）

| 钩子 | 做法 | 提示词落点 |
|---|---|---|
| 异常画面 | 正常场景里出现一个不该有的东西 | “a red umbrella standing alone in a crowded subway” |
| 反常识动作 | 角色做了违和的事（穿西装爬树） | 强调动作与身份冲突 |
| 未完成动作 | 手停在半空、门只开一条缝 | “hand frozen mid-air” |
| 直视镜头 | 角色看向观众，打破第四面墙 | “looking directly into the lens” |
| 声音先入 | 画面未现，声音先到（玻璃碎、心跳） | 需在剪辑层做，纯生成时用“画面暗示声源” |
| 文字悬念 | 一行字 + 一个问号，3s 足够 | 需精确文字排版能力 |
| 极端对比 | 极小 vs 极大、极静 vs 极吵、极新 vs 极旧 | “tiny paper boat beside a giant cargo ship” |
| 痛点共鸣 | 一个所有人都经历过的窘境瞬间 | 生活细节精度决定成败 |

### 2.5 结尾六型

1. **回环**：同构图、同动作，含义反转（最稳，最省镜头）。
2. **反转**：最后 2 秒给出一个推翻前 13 秒的信息（藏在背景里的第二个人）。
3. **留白**：动作停在最高点，不解释（适合概念片）。
4. **符号定格**：角色剪影/道具/纹样占满画幅，做成 logo 位。
5. **金句 + 定格**：一行字压全片情绪，字幕位置恒定在安全区内。
6. **破壁**：角色回头看向镜头，把观众拉进世界观（系列预告常用）。

### 2.6 台词与字幕写法

- 台词三句：**情境句 / 冲突句 / 金句**，每句 ≤12 字。
- 金句要“可截屏”：有主语、有动词、有反差，不要形容词堆砌。
  - 差：`愿每一份热爱都被温柔以待`
  - 好：`它不会等你，但会记得你`
- 字幕：竖屏安全区距上下各留 12%，字号占画幅宽 6–8%，最多两行，出现时长短于台词 0.3s（先看完再听）。

## 3. 镜头语言

### 3.1 景别系统

| 景别 | 中/英 | 画幅占比 | 功能 | 情绪 | 提示词 |
|---|---|---|---|---|---|
| 大远景 | Extreme Wide / Establishing | 人 <1/10 | 交待时空、世界观体量 | 渺小、宿命 | `extreme wide shot, tiny figure in vast landscape` |
| 远景 | Wide / Full Shot | 人 ≈1/3 | 动作完整性、人与环境关系 | 客观、叙述 | `wide shot, full body, environmental context` |
| 全景 | Medium Full / Cowboy | 膝以上 | 姿态、步伐、气场 | 角色感 | `cowboy shot, knees up, confident stance` |
| 中景 | Medium Shot | 腰以上 | 对话、手势、双人关系 | 中性、社交 | `medium shot, waist up, hands visible` |
| 中近景 | Medium Close-up | 胸以上 | 情绪起势、表情开始 | 靠近 | `medium close-up, chest up` |
| 特写 | Close-up | 面部 | 情绪爆点、决策瞬间 | 强共情 | `close-up, face fills frame` |
| 大特写 | Extreme Close-up | 眼/唇/手 | 象征、微观真相 | 侵入、私密 | `extreme close-up, only the eye, iris reflection` |
| 插入 | Insert | 道具 | 递信息（钥匙、倒计时） | 提示 | `insert shot of a ticking pocket watch` |

**景别节奏规则**：连续同景别 ≤2 镜；情绪升级时景别必须递进（远→中→近→大特写）；爆发后必须有一次性“退回远景”的呼吸。

### 3.2 机位与角度

| 角度 | 语义 | 用法 |
|---|---|---|
| 平视 Eye level | 平等、客观、可信 | 对话、纪实、品牌口播 |
| 仰角 Low angle | 权力、威压、英雄化 | 登场、变身、宣言；机位越低越神化 |
| 俯角 High angle | 弱势、被审视、全貌 | 失败、被围、无辜 |
| 荷兰角 Dutch / canted | 失衡、精神崩坏 | 转折点、危机；倾斜 10–25°，别超 30° |
| 顶拍 Top / God's eye | 命运视角、棋盘感 | 开场、布局揭示、群像 |
| 鸟瞰 Aerial | 尺度、地理、史诗 | 世界观片必备 |
| 过肩 OTS | 对话代入 | 正反打的标准件 |
| POV 第一人称 | 强代入、恐怖/沉浸 | 竖屏短片极有效 |
| 反打 Reverse | 关系揭示 | 揭示“他一直在看” |
| 贴地 Worm's eye | 速度、压迫、玩具视角 | 追车、怪兽、脚步 |

### 3.3 运镜

| 运镜 | 英 | 语义 | 速度建议 |
|---|---|---|---|
| 推 Push in / Dolly in | 聚焦、情绪收紧、真相逼近 | 慢推 3–5s 走完，别匀速到突兀 |
| 拉 Pull out | 抽离、揭示环境、收尾、孤独 | 结尾常用，拉出后留 1s 静止 |
| 摇 Pan | 扫视、揭示、跟视线 | 一次只摇一个信息点 |
| 移 Track / Truck | 平行跟随、展示横向布局 | 与主体同速，主体保持在构图同一点 |
| 跟 Follow | 沉浸、紧张 | 手持跟=纪实，稳定器跟=优雅 |
| 升降 Crane / Boom | 揭示规模、升/降情绪 | 上升=升华，下降=沉降/压抑 |
| 手持 Handheld | 真实、慌乱、纪录 | 微抖即可，大幅抖动只给冲击瞬间 |
| 稳定长镜 Steadicam / Oners | 沉浸、空间连续 | 60s 片子里一条 15s 长镜就是记忆点 |
| 环绕 Orbit / Arc | 展示主体、英雄时刻、凝视 | 180° 环绕是最通用的“帅” |
| 变焦 Zoom | 压缩空间、突兀强调 | 快推 crash zoom 用于喜剧/惊悚节拍 |
| 滑动变焦 Dolly Zoom | 认知崩塌、眩晕 | 主体大小不变、背景暴涨；恐怖片标配 |
| 甩镜 Whip pan | 节奏切换、喜剧、转场 | 甩出时运动模糊，落点接下一镜 |
| 俯冲 Drone dive / FPV | 速度、体量、失重 | 竖屏短片的开场王炸 |
| 微距 Macro | 材质、细节、机械感 | 产品片、质感建立 |
| 天旋地转 Roll | 混乱、坠落、主观失控 | 不超过 1 次，否则廉价 |
| 机械臂 Motion control | 精确重复、合成、魔法感 | 同机位重复拍摄做“时间冻结” |

**运镜四条纪律**：
1. 一个镜头只做一件事（要么移动、要么变焦，别同时推+摇+变焦）。
2. 起幅和落幅都要“能独立成图”。
3. 慢镜头必须给“能看清的位移”，原地慢放=废镜。
4. 运镜方向要有动机：被人带走、被声音吸引、被视线牵引；无动机运镜=炫技。

### 3.4 构图

| 构图法 | 英 | 效果 | 提示词 |
|---|---|---|---|
| 三分法 | Rule of thirds | 通用、耐看 | `subject on the right third line` |
| 中心对称 | Symmetrical | 仪式、秩序、荒诞 | `perfectly symmetrical composition, one-point perspective` |
| 框架式 | Framing / Natural frame | 窥视、被困、聚焦 | `framed by a doorway, silhouette in frame` |
| 前景遮挡 | Foreground framing | 层次、偷窥感 | `foreground bokeh leaves, subject behind` |
| 引导线 | Leading lines | 视线牵引、纵深 | `road leading to the horizon` |
| 负空间 | Negative space | 孤独、高级感、留白 | `large empty sky, small figure at bottom` |
| 对角线 | Diagonal | 动感、不稳定 | `diagonal composition, dynamic angle` |
| 重复图案 | Pattern / Repetition | 秩序被打破的前奏 | `rows of identical windows, one lit` |
| 三层纵深 | Fore/mid/back layers | 电影感的核心 | `layered depth: foreground grass, midground figure, background mountains` |

**三条落地口诀**：
- 画面只留一个“最亮的东西”，观众的眼睛一定去那儿——那就是你的信息点。
- 主体不要压中轴十字点，压就压三分交点。
- 大片留白必须“有内容”（云、雾、水、光），空白天=没做完。

### 3.5 光线

| 光型 | 英 | 语义 | 提示词 |
|---|---|---|---|
| 三点布光 | Three-point (key/fill/rim) | 标准、立体、商业 | `three-point lighting, soft key, subtle rim light` |
| 硬光 | Hard light | 戏剧、强对比、狠 | `hard directional sunlight, sharp shadows` |
| 柔光 | Soft / Diffused | 温柔、高级、无攻击 | `soft diffused window light, gentle falloff` |
| 伦勃朗 | Rembrandt | 古典、有故事的脸 | `Rembrandt lighting, triangle of light on cheek` |
| 蝴蝶光 | Butterfly | 美颜、广告、正脸 | `butterfly lighting, shadow under nose` |
| 轮廓光 | Rim / Backlight | 分离背景、神性 | `strong rim light outlining silhouette` |
| 剪影 | Silhouette | 符号化、匿名、神秘 | `backlit silhouette against bright haze` |
| 顶光 | Top light | 压抑、审判、恐怖 | `harsh top light, deep eye sockets` |
| 底光 | Underlight | 邪恶、诡异 | `light from below, inverted shadows` |
| 实用光源 | Practical | 真实、氛围、霓虹 | `neon sign as only light source, magenta and cyan` |
| 体积光 | Volumetric / God rays | 神性、尘埃感、史诗 | `volumetric light beams through fog` |
| 百叶窗影 | Blind shadows | 窥视、城市、黑色电影 | `venetian blind shadows across the face` |
| 高调 | High-key | 干净、商业、无害 | `high-key lighting, minimal shadows` |
| 低调 | Low-key | 悬疑、压迫、高级 | `low-key lighting, 80% shadow` |

**光的三件套描述法**（比形容词有效）：`方向 + 质感 + 色温`。
`top-left hard 5600K key, cool 4300K rim, no fill` —— 一句话就把光说清楚了。

### 3.6 色彩

- **色彩脚本（Color Script）**：全片只规划 5–7 个色块，按情绪排成一条渐变。
  - 常态：低饱和暖灰 → 激励：冷青入侵 → 升级：洋红/橙对撞 → 高潮：单色爆白 → 收束：回到暖灰但更亮。
- **双色调是最快的“电影感”**：青橙（teal & orange，商业/英雄）、粉蓝（pink & blue，都市/青春）、绿紫（毒感/赛博）、红黑（暴力/权力）。
- **单色统治**：一帧里一个主色占 70%，辅色 20%，点缀 10%（同一个“三色原则”用于角色与画面）。
- **情绪对应**：暖橙=安全/回忆，冷青=疏离/科技，绿=病态/异化，洋红=欲望/失真，纯白=超验/审判，低饱和灰=麻木。
- **LUT / 胶片参考**（写进提示词的有效词）：`Kodak Portra 400`（暖柔人像）、`Kodak 2383`（标准电影印片）、`Fuji 3510`（冷青绿）、`bleach bypass`（高对比低饱和）、`CineStill 800T`（夜景洋红）、`VHS`（扫描线+色偏）。

### 3.7 剪辑与转场

| 手法 | 英 | 用途 |
|---|---|---|
| 动作衔接 | Match on action | 同一动作跨镜连续，最隐形最专业 |
| 图形匹配 | Graphic match | 圆接圆、线接线，仪式感转场 |
| 跳切 | Jump cut | 时间压缩、焦虑、网感 |
| J-cut / L-cut | 声先入 / 声延后 | 让剪辑“听不出来”，最有效的顺滑手段 |
| 蒙太奇 | Montage | 时间流逝、训练、准备 |
| 交叉剪辑 | Cross cutting | 双线并进、倒计时张力 |
| 视线匹配 | Eyeline match | 保证观众知道“他在看什么” |
| 180° 轴线 | 180-degree rule | 对话不晕的基础；破轴=刻意制造错乱 |
| 30° 原则 | 30-degree rule | 相邻两镜机位差 >30°，否则像跳帧 |
| 卡点剪辑 | Beat sync | 音乐重拍切镜，竖屏传播利器 |

**转场菜单（含提示词可落地性）**：

| 转场 | 做法 | 生成可行性 |
|---|---|---|
| 硬切 | 直接换 | ★★★★★ |
| 遮挡转场 | 主体/墙/手掠过镜头遮黑 | ★★★★ |
| 甩镜转场 | 甩出运动模糊接下一镜 | ★★★★ |
| 相似形 | 圆月→车轮→瞳孔 | ★★★ |
| 白闪 / 黑闪 | 全白/全黑 2 帧 | ★★★★★（剪辑层做） |
| 叠化 | 溶解 | ★★★★ |
| 遮罩划像 | 形状擦除 | ★★★（剪辑层最稳） |
| 匹配剪辑 | 同构图换时空 | ★★★★（同机位复用最省成本） |
| 声音桥 | 上镜声音延续到下一镜 | 剪辑层 |

## 4. 角色设定技术要点

### 4.1 识别度工程（先做这四件事，再谈好看）

1. **剪影测试**：把角色涂成全黑，缩小到 200px，还能认出是谁 → 通过。不通过就加形状特征（帽檐、角、尾巴、外扩的裙摆、机械臂）。
2. **三色原则**：主色 60%（可直接给 HEX）、辅色 30%、点缀 10%。点缀色只用在“会动的、会发光的那一处”，让观众一眼锁定。
3. **单锚点特征**：只留 1 个强记忆点（眼罩 / 断角 / 蝴蝶发饰 / 左手机械）。多留=没有。
4. **形状语言**：圆=亲和/无害，方=可靠/力量，三角=危险/机敏，细长=脆弱/高雅，矮宽=顽固/喜剧。头身比：Q 版 2–3、卡通 4–5、半写实 6–7、写实 7.5–8。

### 4.2 角色卡字段（直接当人物提示词模板）

```
姓名 / 物种或身份 / 年龄感（不写具体岁数，写“看起来像”）
身高比 · 体型 · 头身比
脸型 · 五官：眼型+瞳色+睫毛 · 鼻 · 唇 · 下颌
发型（长度+轮廓+分缝）· 发色（HEX）
服装三层：内层（贴身材质）/ 中层（主视觉，最大色块）/ 外层（轮廓，决定剪影）
配饰 1 件（标志物）· 道具 1 件（可动作化）
主色 HEX / 辅色 HEX / 点缀色 HEX（发光点）
材质关键词：哑光布 / 硬表面金属 / 半透明胶质 / 毛绒 / 鳞片
性格三词（必须互斥互补，如“克制 · 记仇 · 心软”）
口头禅 1 句（≤8 字）
习惯动作 1 个（每集重复，成为 IP 记忆点）
能力视觉化：能力必须以“光/粒子/材质变化”显形
弱点 1 个（决定故事可写性）
成长弧：从 A 到 B，一句话
参考风格：画风锚（anime cel / stylized 3D / ink wash）
```

注：角色卡里的“参考风格”只写 `data/styles/` 里的风格 ID，不写品牌名。

### 4.3 性格外化公式

```
性格 → 习惯动作 → 随身道具 → 所处环境 → 服装细节
```

示例链：

| 性格 | 习惯动作 | 道具 | 环境 | 服装 |
|---|---|---|---|---|
| 控制欲 | 反复把桌角对齐 | 卷尺 | 极整洁、量过尺寸的房间 | 扣到最上一颗 |
| 逃避 | 说话时退半步 | 耳机 | 永远在门边、走廊 | 宽松、包住手 |
| 暴烈但心软 | 抬手又放下 | 创可贴 | 满地碎片但养着花 | 旧皮衣 + 缝补痕迹 |

**原理**：观众记住的是“行为差异”，不是形容词。写人设时先写行为，形容词只是备注。

### 4.4 表演与微表情节拍（按帧设计）

| 阶段 | 时长 | 内容 |
|---|---|---|
| 预备 Pre-beat | 0.3s | 呼吸停、眼睛先动（看的方向决定观众注意力） |
| 变化 Beat | 0.4–0.6s | 眉毛/嘴角/瞳孔单点变化，不要全套一起动 |
| 维持 Hold | 0.5–1s | 停在半表情，这是“可截屏”的一帧 |
| 回落 Release | 0.3s | 视线移开或眨眼，情绪落地 |

**动画/生成的表演规则**：
- 一个镜头只给一个微表情变化，两种以上会变成“表情包”。
- 情绪越强，动作越小（真哭是肩膀抖，不是张嘴）。
- 停顿比动作贵：高潮前留 1 秒静止，观众才会屏息。
- 视线永远有目标：看向画外某物 → 观众自动补全故事。

### 4.5 AI 生成的角色一致性 SOP

1. **先做 Character Sheet（角色设定板）**：正面 / 3/4 侧 / 背面 / 表情 3 款 / 关键动作 2 款 / 主色色卡。这张图是全片唯一的“宪法”。
2. **锁三样**：参考图（角色板）、种子 seed、风格锚词。三者任一变动就会漂移。
3. **锁拍摄条件**：同一焦段、同一光位、同一色温写进每个提示词，不靠“看起来差不多”。
4. **分批生成**：先出“全身标准像”，再出“同角度半身”，再出“同角度特写”，逐级逼近，别一步跨到特写。
5. **权重控制**：参考图权重过高=贴图死板、过低=脸变。中近景以上权重可高，远景（小于画面 1/8）权重可低，此时靠剪影和配色识别。
6. **禁忌**：同一片子不要混两种画风参考；不要让模型“自由发挥发型”；不要用不同平台生成同一角色。

## 5. 常用拍摄手法 16 式

| # | 手法 | 效果 | 典型用法 | 提示词要点 |
|---|---|---|---|---|
| 1 | 英雄镜头 Hero Shot | 低机位+仰角+逆光，人立刻变大 | 登场、变身 | `low angle hero shot, backlit, wind in hair` |
| 2 | 子弹时间 Bullet Time | 时间冻结环绕 | 高潮、能力展示 | `frozen mid-air particles, camera orbiting` |
| 3 | 升格慢动作 Slow Motion | 放大细节与情绪 | 打击、落泪、雨滴 | `120fps slow motion, water droplets suspended` |
| 4 | 延时 Time-lapse | 时间流逝、城市呼吸 | 转场、世界观 | `time-lapse clouds, day to night` |
| 5 | 一镜到底 Oners | 沉浸、空间连续 | 开场、跟随 | `continuous take, no cuts, following` |
| 6 | 主观镜头 POV | 强代入 | 恐怖、沉浸、竖屏 | `first person view, hands visible at frame edge` |
| 7 | 过肩对话 OTS | 关系张力 | 对峙、告白 | `over-the-shoulder, shallow depth on listener` |
| 8 | 反射/镜面 Mirror | 双重信息、心理 | 分裂、真相 | `reflection in cracked mirror, two faces` |
| 9 | 前景掠影 Wipe by Foreground | 层次与速度 | 街拍、转场 | `crowd blurring past foreground` |
| 10 | 微距材质 Macro | 高级感、质感 | 产品、机械 | `macro shot, water on brushed metal` |
| 11 | 光斑与漏光 Bokeh / Flare | 梦幻、胶片感 | 夜景、回忆 | `anamorphic lens flare, heavy bokeh` |
| 12 | 烟雾/粉尘氛围 Haze | 光的形状、史诗 | 逆光、战场 | `volumetric haze, dust in light beams` |
| 13 | 水面/雨 Rain & Water | 情绪外化、反射 | 告别、黑帮 | `rain hitting neon puddles, reflections` |
| 14 | 影子戏 Shadow Play | 隐喻、低成本高级 | 悬念、暴力暗示 | `shadow on wall, source off-screen` |
| 15 | 定格/时间冻结 Freeze | 强调、海报帧 | 收尾、系列预告 | `everything frozen mid-action` |
| 16 | 视角切换（人→物→兽） | 世界规则显形 | 世界观片 | `from the perspective of a cat / a drone / a coin` |

**用多少合适**：15s 片最多 2 种特殊手法，60s 最多 4 种。手法是盐，不是饭。

## 6. 动画风格谱系

### 6.1 二维（2D）

| 风格 | 特征 | 提示词关键词 | 适配 IP |
|---|---|---|---|
| 日式赛璐璐 | 硬边阴影、干净线稿、发丝高光 | `anime cel shading, clean lineart, hard shadow edges` | 少年、奇幻、校园 |
| 90s 复古赛璐璐 | 低分辨率、色偏、胶片颗粒 | `90s retro anime, VHS grain, slightly off-register colors` | 怀旧、机甲 |
| 美式黄金时代 | 软弹形变、橡胶肢体 | `rubber hose animation, 1930s Fleischer style` | 喜剧、怪诞 |
| 现代美式卡通（CalArts） | 无描边、几何化、表情夸张 | `modern flat cartoon, no outline, geometric shapes` | 合家欢、吉祥物 |
| 国漫水墨/工笔 | 墨分五色、留白、笔触呼吸 | `Chinese ink wash animation, brush texture, negative space` | 东方、武侠、文化 IP |
| 剪纸/皮影 | 关节分层、平面侧影 | `paper cut-out animation, articulated layers` | 民俗、寓言 |
| 沙画 | 颗粒、即时性、单色 | `sand animation, grainy monochrome` | 纪实、抒情 |
| 定格（黏土/纸偶） | 12fps 顿感、材质瑕疵 | `stop-motion claymation, 12fps, visible fingerprints` | 童趣、怪奇 |
| 像素 | 16bit 色板、锯齿 | `pixel art, 16-bit, limited palette` | 游戏 IP、赛博 |
| 版画/木刻 | 粗黑线、高对比 | `woodcut print style, bold black lines` | 黑暗、寓言 |
| 水彩/水粉 | 晕染、纸纹 | `watercolor animation, wet-on-wet, paper grain` | 治愈、文艺 |
| 扁平矢量 | 纯色块、无渐变 | `flat vector illustration, solid color blocks` | 社交、品牌 |
| 动态漫（有限动画） | 局部动、镜头动 | `limited animation, manga motion comic` | 低成本系列 |

### 6.2 三维（3D）

| 风格 | 特征 | 关键词 | 适配 |
|---|---|---|---|
| 风格化写实（皮克斯式） | 大眼、软皮肤、次表面散射 | `stylized realistic 3D, Pixar-like, subsurface scattering` | 合家欢、品牌 |
| 夸张卡通 3D（梦工厂式） | 拉伸挤压、夸张比例 | `exaggerated cartoon 3D, squash and stretch` | 喜剧、吉祥物 |
| 写实 CG | 皮肤毛孔、布料纤维、物理光 | `photorealistic CG, skin pores, cloth fibers, ray tracing` | 硬核、科幻 |
| 三渲二 | 3D 模型 + 2D 描边/色块 | `3D cel-shaded, toon outline, anime-style 3D` | 二次元游戏 IP |
| 硬表面机甲 | 分件、蚀刻线、金属反射 | `hard-surface mecha, panel lines, brushed metal` | 机甲、玩具 |
| 毛绒/布料 | 绒毛散射、织物重量 | `fluffy fur shading, soft cloth simulation` | 萌系 IP |
| 低多边形 | 面块感、扁平色 | `low poly 3D, flat shading` | 独立、复古 |
| 体素 | 方块构成 | `voxel art, cubic geometry` | 沙盒游戏 IP |

注：上表“皮克斯式”“梦工厂式”是风格简称，提示词里只写描述性关键词（大眼、软皮肤、次表面散射），不写品牌名。见 `data/styles/`。

### 6.3 混合

- **2D 角色 + 3D 场景**：角色有手绘温度，场景有物理可信度（多数国产动画的做法）。
- **实拍 + CG 角色**：难点在“接触阴影 + 同一套镜头畸变 + 同一胶片颗粒”。
- **转描 Rotoscope**：真实运动 + 手绘外观，适合舞蹈、打斗。
- **动态图形 Motion Graphics**：几何 + 文字 + 节奏，适合信息型品牌短片。
- **实拍 + 手绘叠加**：情绪外化（涂鸦、光斑、记忆碎片）。

**风格选择的判断标准**（不是好看，是匹配）：
1. 角色的“形状语言”能不能承载这个故事（圆角色讲不了硬核暴力）。
2. 生产成本与镜头数：定格/水墨的单镜成本是赛璐璐的 3–5 倍。
3. 平台清晰度：竖屏小窗里，细节型写实会糊成一团，高对比卡通更抗压缩。

## 7. 影视风格谱系

### 7.1 类型片风格（按“看什么”分）

| 风格 | 视觉三要素 | 提示词关键词 |
|---|---|---|
| 赛博朋克 Cyberpunk | 霓虹双色 + 湿地面反射 + 巨构压迫 | `cyberpunk, neon magenta and cyan, wet asphalt reflections, megastructure` |
| 蒸汽朋克 Steampunk | 黄铜 + 蒸气 + 齿轮 | `steampunk, brass gears, steam, sepia warm` |
| 废土 Post-apocalyptic | 沙尘黄 + 灰蓝 + 空旷 | `post-apocalyptic wasteland, dust haze, muted ochre` |
| 黑色电影 Film Noir | 高对比黑白 + 百叶窗影 + 烟雾 | `film noir, high contrast black and white, venetian shadows` |
| 新黑色 Neo-noir | 霓虹 + 冷蓝 + 雨夜 | `neo-noir, rain-soaked neon street, cool blue` |
| 武侠 Wuxia | 竹/雾/水 + 慢动作 + 留白 | `wuxia, bamboo forest mist, slow motion silk` |
| 新中式 Oriental | 朱红 + 墨黑 + 鎏金 + 对称 | `new Chinese aesthetic, vermilion and ink black, gold accents, symmetry` |
| 港风霓虹 HK Neon | 抽帧 + 狭构图 + 洋红绿 | `Hong Kong neon, step-printing motion blur, cramped framing` |
| 日式治愈 Japanese | 高调自然光 + 低饱和绿 + 生活细节 | `Japanese slice-of-life, soft natural light, muted green, film grain` |
| 千禧复古 Y2K | CCD 锐化 + 闪粉 + 蓝紫 | `Y2K aesthetic, CCD camera look, glitter, silver blue` |
| 蒸汽波 Vaporwave | 粉紫渐变 + 网格 + 石膏像 | `vaporwave, pink purple gradient, wireframe grid, marble bust` |
| 太空歌剧 Space Opera | 巨物 + 冷白 + 星云 | `space opera, enormous scale, cold white light, nebula` |
| 特摄 Tokusatsu | 微缩布景 + 硬光 + 夸张模型 | `tokusatsu, miniature set, hard studio light` |
| 恐怖 Giallo / 悬疑 | 洋红绿 + 强色光 + 几何 | `giallo horror, saturated magenta green, geometric shadows` |
| A24 冷峻 | 自然光 + 低饱和 + 静态构图 | `A24 style, naturalistic light, desaturated, static framing` |
| 韦斯·安德森 | 绝对对称 + 粉彩 + 正侧机位 | `Wes Anderson, symmetrical composition, pastel palette, flat frontal framing` |
| 诺兰冷峻 | 冷蓝 + IMAX 大画幅 + 实拍质感 | `cold blue palette, large format, practical realism` |
| 塔可夫斯基式 | 长镜 + 水/火/废墟 + 诗意 | `long take, water and fire, ruined poetry, earthy palette` |
| 纪录片纪实 | 手持 + 自然光 + 不完美构图 | `documentary handheld, available light, imperfect framing` |
| 商业广告级 Commercial | 完美光 + 微距 + 无瑕材质 | `high-end commercial, perfect lighting, macro texture, glossy` |

### 7.2 年代风格

| 年代 | 视觉标记 | 关键词 |
|---|---|---|
| 民国 1920–40s | 旗袍、香烟、钨丝灯暖黄、颗粒 | `1930s Shanghai, qipao, tungsten warm, heavy grain` |
| 80s 港片 | 霓虹、烟、宽肩西装、变焦 | `1980s Hong Kong, neon, shoulder pads, zoom lens` |
| 90s 录像带 | 扫描线、色偏、低清 | `1990s VHS, scanlines, chroma bleed, low resolution` |
| 2000s 千禧 | 高饱和、塑料感、银蓝 | `2000s, oversaturated, plastic texture, silver blue` |
| 近未来 Near-future | 洁净白 + 全息 + 无尘 | `near-future, clean white, holographic UI, dust-free` |

### 7.3 “电影感”到底由什么构成（五个可写进提示词的参数）

1. **画幅**：2.39:1 或 1.85:1（越宽越史诗，竖屏反而要 9:16 + 竖向构图，别把横构图裁进竖屏）。
2. **浅景深**：85–135mm + f/1.8，把背景化成色块。
3. **胶片质感**：`35mm film grain, halation on highlights, slight breathing`。
4. **变形宽银幕特征**：`anamorphic lens, oval bokeh, horizontal blue flare`。
5. **不完美**：轻微暗角、色温不一致的实用光源、镜头呼吸——完美 CG 感恰恰最不电影。

## 8. 提示词封装

### 8.1 两个主公式

**图像公式（7 段）**

```
谁 + 状态/年龄感
一个动词 + 姿态细节
三层服装 + 1 件标志物
地点 + 时间 + 天气 + 一层氛围元素
景别 + 机位角度 + 焦段 + 构图法
方向 + 质感 + 色温 + 主辅点缀三色
画风/年代/胶片 + 材质细节 + 画质词 + 负向
```

**视频公式（6 段，v3.7 起作废，见 templates/video_prompt_7seg.md 的七段式）**

> 下面 6 段只作历史参考：v3.7 起视频提示词按七段式拼（画风/镜头/构图与配色/人物/逐秒/声音/约束），
> 其中【逐秒】0–0.2 秒静止等于首帧、最后 0.3 秒停住等于尾帧。

```
类型 + 速度 + 起点构图 → 终点构图
起始状态 → 过程 → 结束状态（三段式）
烟/水/风/人群/光变化（视频“活着”的关键）
焦段 + 光圈 + 帧率 + 快门 + 稳定方式
时间推进 or 光源移动
最后一个画面停留给什么感受
```

**关键经验**：视频提示词里“主体动作写三段（起—中—止）”比写形容词有效 3 倍；不加环境动态，画面会像 PPT。

### 8.2 分镜表模板（复制到表格里用）

| 镜号 | 时长 | 景别 | 机位 | 运镜 | 画面内容 | 角色动作 | 台词/字幕 | 音效音乐 | 转场 | 情绪值 | 提示词 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 01 | 2.5s | 大远景 | 俯角航拍 | 缓降 | 荒原上一个白色身影 | 静止抬头 | — | 低频风噪 | 硬切 | 3/10 | … |
| 02 | 1.8s | 大特写 | 平视 | 缓推 | 瞳孔里映出火光 | 瞳孔收缩 | — | 心跳 | 图形匹配 | 7/10 | … |

### 8.3 提示词词库（按需拼装）

**镜头**：`wide shot / medium shot / close-up / extreme close-up / over-the-shoulder / POV / low angle / high angle / dutch angle / aerial / macro / insert shot / two-shot / silhouette shot`

**运镜**：`slow push in / pull back / orbit around / tracking shot / handheld follow / crane up / whip pan / crash zoom / dolly zoom / steadicam walk / drone dive / tilt down / pan left`

**构图**：`rule of thirds / centered symmetry / one-point perspective / framed by doorway / leading lines / negative space / layered foreground-midground-background / diagonal composition`

**光**：`soft key light / hard rim light / backlit silhouette / volumetric god rays / practical neon / candlelight / window light / harsh top light / underlight / teal-orange lighting / low-key / high-key`

**色/质感**：`teal and orange / monochrome / desaturated / warm amber / cyan magenta / Kodak Portra 400 / film grain / halation / anamorphic flare / brushed metal / wet asphalt / dust particles / volumetric fog`

**画质**：`cinematic / 35mm film / 8k detail / shallow depth of field / realistic skin texture / ray-traced reflections / cinematic color grading / anamorphic 2.39:1`

**负向（常用）**：`no text, no watermark, no extra fingers, no distorted face, no plastic skin, no oversaturated colors, no modern objects (年代片用), no logo`

### 8.4 参数对照表（写提示词时直接查）

**焦段 → 景别 → 空间感**

| 焦段 | 对应景别 | 透视 | 景深 | 语义 |
|---|---|---|---|---|
| 14–24mm | 大远景 / 环境 | 夸张、边缘拉伸 | 深 | 体量、压迫、速度 |
| 28–35mm | 全景 / 纪实 | 轻微广角 | 中 | 现场感、新闻感 |
| 50mm | 中景 / 对话 | 接近人眼 | 中浅 | 客观、可信 |
| 85mm | 中近景 / 特写 | 轻微压缩 | 浅 | 人像、亲密度 |
| 100mm macro | 微距 | — | 极浅 | 材质、细节 |
| 135–200mm | 特写 / 偷窥 | 强压缩、背景扁平 | 极浅 | 隔离、监视、怀旧 |

**帧率 / 快门**

| 帧率 | 用途 | 快门 |
|---|---|---|
| 24fps | 电影感（原生运动模糊） | 1/48 |
| 25fps | PAL / 国内播出 | 1/50 |
| 30fps | 网络常规 | 1/60 |
| 60fps | 轻微慢放、游戏感 | 1/120 |
| 120fps | 强慢动作（雨、碎片、发丝） | 1/240 |
| 240fps | 极慢（水花、爆点） | 1/480 |

**画幅 / 平台**

| 比例 | 用途 | 构图注意 |
|---|---|---|
| 2.39:1 | 电影感、概念片 | 别把关键信息放两侧 15% |
| 16:9 | 横屏主流、B 站 | 通用 |
| 9:16 | 抖音、视频号、Story | 主体居中偏上，字幕留上下 12% |
| 4:5 | 小红书、信息流 | 竖构图但保留横向空间 |
| 1:1 | 头像、封面、商品 | 剪影识别的最佳测试比例 |

### 8.5 全流程一致性 SOP（七步）

1. **风格锚点图**：先出 1 张“这就是我们要的味道”的定调图，全片所有提示词共用它的风格段。
2. **角色卡 + Character Sheet**（见 4.5）。
3. **场景卡**：每个场景出 1 张空镜定调（光位、色温、材质），后续所有该场景镜头复用这段场景描述。
4. **色彩脚本**：5–7 个色块排成情绪曲线，决定每一镜的主色。
5. **分镜 → 提示词**：按 8.1 公式逐镜写，每镜必须包含“风格段 + 角色段 + 场景段”三段共用文本（保证漂移最小）。
6. **抽卡与收敛**：每镜生成 4–8 张，只按“剪影是否可辨 / 光位是否一致 / 色是否在同一色块”三个标准筛，不看“好不好看”。
7. **串片质检**：把成片缩略图排成一排（contact sheet），一眼扫过：有没有突然变亮/变暖/变焦段的镜头，那就是不一致的元凶。

## 9. 交付前质检清单

**故事层**
- [] 能用一句话说出“谁为了什么做了什么”？
- [] 前 3 秒是不是未完成状态？
- [] 结尾是否重构了开头（同构图/同台词/同道具）？
- [] 台词是否 ≤3 句、金句是否可截屏？
- [] 每 8–10 秒是否换过一次信息层级？

**镜头层**
- [] 相邻两镜机位差 >30°？
- [] 对话是否守住 180° 轴线？
- [] 每镜是否有明确的信息点（一个最亮/最动的东西）？
- [] 运镜是否有动机，起幅落幅是否都能独立成图？
- [] 情绪爆发后是否有一次“退回远景”的呼吸？
- [] 是否 ≤2（15s）/ ≤4（60s）种特殊手法？

**角色层**
- [] 200px 剪影测试通过？
- [] 主/辅/点缀三色是否贯穿全片？
- [] 标志道具是否出现 ≥2 次并参与叙事？
- [] 每个镜头里角色的脸、发型、服装是否完全一致？

**视觉层**
- [] 全片是否只有 5–7 个色块？
- [] 有无突然风格/焦段/色温跳变的镜头？
- [] 画幅与平台匹配（竖屏别套横构图）？
- [] 文字排版是否在安全区内、无错字、无乱码？

**传播层**
- [] 有没有一帧可以直接当封面/海报？
- [] 有没有一句可以直接当文案？
- [] 有没有一个 1 秒就能认出的 IP 符号？

## 附：三段可直接改写用的示例提示词

**1）角色登场（图生图 / 首帧）**
> 大远景，俯角航拍，缓降。荒原上只有她一个人，白裙在当前 1/20 的画幅里，风把裙摆吹向左侧。黄昏逆光，色温 4300K，暖橙主色 70%、冷青天空 25%、裙摆上一点金 5%。影调低调，空气中有细尘。35mm 胶片颗粒、轻微高光溢散。中国水墨式留白的构图逻辑，但材质写实。

**2）情绪转折（图生视频）**
> 缓推 3 秒，从中近景推到面部特写，主体位置不动。她的视线从画外左下方缓慢抬到镜头正前方，睫毛抖了一次，嘴唇张开但没有声音（起—中—止三段）。背景的雨滴在她脸侧形成细小的反射位移，前景有一片叶子飘过遮挡 0.4 秒。85mm、f/1.8、24fps、1/48。光从右后方硬光切入，轮廓光变强，主光衰减。落点是“她终于决定说谎”。

**3）结尾符号化**
> 完全对称的中心构图，正侧机位，她站在画面正中，手里的伞还滴着水。背景是纯色雾面墙，朱红 60%、墨黑 30%、伞骨的铜色 10%。顶光压暗眼窝，地面反光打亮下巴。画面静止 1.5 秒后，伞面缓缓合拢遮住她的脸，最后一帧只有伞的剪影。2.39:1，Kodak 2383 色调，粒子极细。

---
*注：本手册第 0.1 节的 60 秒 16–25 镜是分镜密度目标；本技能短视频默认 30 秒，按 3 段 × 10 秒生成、每段内可含多镜运镜，不强制每镜单独生成一段（那会烧掉 16–25 段视频的额度）。*
