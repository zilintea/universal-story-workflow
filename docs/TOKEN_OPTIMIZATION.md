# Token 优化（减少浪费，不减质量）

## 原则
- 锁定表只写一次，之后只用 ID 引用，不重复写全描述
- 分镜用紧凑行格式，不用散文段落
- 审计表只写不通过项和改法，通过项只写“通过”二字，不展开
- 词汇表只在第一集写全，之后只写新词，旧词用 ID 引用

## 紧凑格式（示例，短视频版）
```
TITLE: Fire! Run First! | LANG: EN | LEVEL: beginner | FORMAT: short 60s 16:9
CHARS: [C1, C2, C3, C4, C5]（本集角色名只写在锁定表里，这里只用 ID）
SCENES: [S1 kitchen, S2 grass path, S3 river bay]
ITEMS: [I1 pot, I2 scarf, I3 towel]
VOCAB: fire/smoke/run/shout/safe | PATTERNS: Fire! Run! / Don't go back!
WARNING: Do not go back for things in a fire.
SHOTS:
1|S1|C1|cook, smoke rises|Nar: C1 cooks.|10s
2|S1|C1|smoke billows, cover mouth, run to door|Dia: Fire!|10s
3|S2|C1,C5|run out, magpie flies high|Dia: Fire! Run!|10s
4|S2|C2,C3,C4|run to river bay|Nar: Friends run out.|10s
5|S3|C1,C2,C3,C4|friends hold C1 back|Dia: Don't go back!|10s
6|S3|C1,C2,C3,C4,C5|count, all safe|Dia: We are safe!|10s
```
- 人物、场景、物品的完整描述在锁定表里，不在每集里重复
- 每集新写的内容只有：标题、词汇、句型、警示点、分镜行、审计不通过项

## 实测（字符数作 token 代理，见 scripts/token_check.py，2026-11-05 实测）
- 散文示例（examples/fire-english-text.md）：2297 字符
- 紧凑模板（templates/compact_story.txt）：789 字符，约为散文示例的 34%
- 注意：紧凑模板不含完整人物描述（锁定表另存），这个 34% 是模板本身的对比，不是整集的精确 token 节省率；只做一集时，第一次读锁定表多花的 token 会抵消一部分节省，集数越多越省
