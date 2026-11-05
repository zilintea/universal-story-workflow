# Braised Fish / 红烧鱼（流程型示例，只作示例，不写死在流程里）

## 一句话提示
做一道菜：红烧鱼。

## 流程锁定表
- 成品：红烧鱼，最终状态 dish ready（鱼熟了、摆盘好了）
- 材料：鱼 1 条（初始 raw）、酱汁 2 勺（初始 in bowl）、姜 1 块（摆盘用）
- 工具：锅、刀（危险：锋利）、铲
- 步骤：
  1. 洗鱼：用鱼，前置 fish raw，做完 fish clean
  2. 划刀花：用鱼、刀，前置 fish clean，做完 fish scored，危险 sharp，安全做法：大人拿刀，孩子只看
  3. 热油：用锅，做完 pan hot，危险 hot，安全做法：大人掌勺，孩子站远
  4. 煎鱼：用鱼、锅，前置 fish scored + pan hot，做完 fish golden，危险 hot，安全做法：大人煎，孩子站远
  5. 加酱汁：用酱汁、鱼，前置 fish golden + sauce in bowl，做完 fish sauced
  6. 炖：用鱼，前置 fish sauced，做完 fish cooked
  7. 摆盘：用鱼，前置 fish cooked，做完 dish ready
- 创意点（用户创意，1 处）：姜切成花摆盘。改了摆盘造型，没改步骤顺序、没改成品、没绕安全。

## 审计
- 流程审计：scripts/check_process.py 通过（好流程），坏流程（跳洗鱼、先加酱汁、热油没安全做法）被拦下
- 安全审计：危险步骤都有大人做，孩子只做安全的一半
