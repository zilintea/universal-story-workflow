# Universal Story Workflow · 通用故事工作流

**一句话就能完整构建一个故事，先出文字，审核通过后再做视频。主打娱乐中学习，后期有对话和旁白，作语言教学用。**

> 一句话提示 → 自我构思 → 编排情节 → 逻辑 + 语言双审计 → 文字故事（含对话、旁白、单词高亮发音）→ 画布（角色画布 / 故事板画布 / 场景画布）→ 视频 + 分轨音频

## 快速开始

```
用户：出一集[IP 名]，主题是[生活场景]
Muse：按 SKILL.md 跑完 7 步，先给你文字故事（见 examples/songcuo-dexin-text.md 的格式），
      你点头后才出故事板、视频、音频。
```

不用用户去外部工具操作，不用用户补设定。IP 是插件，流程是主体。

## 仓库结构

```
SKILL.md                  主流程（直接调用的入口）
skill.yaml                技能元数据
scripts/
  conceive.py             自我构思：给主题或不给主题，出 3 个点子并初筛
  check_story.py          逻辑 + 语言审计：词频、句长、因果链、反转伏笔自查
  highlight_words.py      单词高亮发音：把词汇表变成带拼音/音标的高亮文本和字幕
  make_canvas.py          画布：生成 9 格故事板空白画布和角色画布模板
templates/                文字输出格式、一句话解析表
checklists/               逻辑审计、语言审计
data/                     儿童故事模式、语言教学、故事结构、单词高亮规范
docs/
  EVALUATION.md           学习类 Skills 全面评估报告
  CANVAS.md               画布系统说明
  WORD_HIGHLIGHTING.md    单词高亮发音规范
  PLOT_ARRANGEMENT.md     情节编排说明
examples/                 示例文字故事（送错的信重制版文字稿、新 IP 示例）
ip_modules/hailukong/     示例 IP 插件：海陆空小队角色表（摘要版）
```

## 核心能力（本仓库新增，区别于旧版）

1. **自我构思**：不只等用户给主题。用户只说“给我一个故事”或只给一个词，`conceive.py` + 结构库能出 3 个点子（主角、主题、物品、反转各不同），经审计初筛后挑一个，不用用户想点子。
2. **画布**：三套画布，见 `docs/CANVAS.md`。角色画布（三视图 + 表情行）、故事板画布（9 格，带序号）、场景画布（固定元素清单）。画布是生成的底图和检查标准，不是让用户自己画。
3. **编排故事情节**：见 `docs/PLOT_ARRANGEMENT.md`。三幕节拍、因果链图、升级一次原则、伏笔- payoff 对照表，情节不是人物接力。
4. **单词高亮发音**：见 `docs/WORD_HIGHLIGHTING.md`。文字里词汇加粗 + 拼音/音标；音频里关键词慢读、重复、停顿；字幕里关键词变色（黄色），其余白色。`highlight_words.py` 可直接跑出高亮文本和 ASS 字幕骨架。

## 安装为 Skill

把本仓库整个文件夹复制到 Muse 的自定义技能目录（例如 `~/workspace/custom-skills/universal-story-workflow/`），或在 Muse 里按技能仓库导入流程导入。Skill 入口是 `SKILL.md`，元数据是 `skill.yaml`。

## 许可

代码 MIT，文字、模板、数据 CC BY-NC 4.0（与 ai-anime-series 仓库的许可结构一致，便于复用和二次创作，但商用需另行授权）。详见 LICENSE。
