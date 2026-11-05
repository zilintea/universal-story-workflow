#!/usr/bin/env python3
"""场景模板硬规则审计（v2.10）：有场景必读必用。
用法：python3 scripts/check_scenario.py story.json shots.json
查：
  1) story.json 必须有 scenario 字段（字符串或 null；没写字段 = 不通过）；
  2) scenario 非空时，必须是 23 个场景之一（名字去掉空格后比对）；
  3) scenario 非空时，story.json 的 scenario_points 至少 2 条（文字稿“场景模板”栏登记的已用关键点）；
  4) 内容型场景：镜头卡全文（shots.json 所有字段拼起来）至少命中该场景 2 组关键词；
     结构型场景（长视频 / 改编 / 延长 / 补全 / 多帧 / 混剪）：不查关键词，只查 1)–3)。
不通过 = 镜头卡没写完，不进视频。
场景定义见 docs/SCENARIO_TEMPLATES.md；场景名由 scripts/suggest_style.py 输出。
"""
import json, sys

# 场景 -> 关键词组（每组命中其一即算该组命中；内容型场景至少命中 2 组）
SCENARIOS = {
    "电商产品广告": [["Orbit", "环绕"], ["微距", "特写"], ["轮廓光", "rim"]],
    "仙侠/奇幻动画": [["丁达尔", "光束"], ["灵力", "仙气"], ["云海", "云雾"]],
    "短剧/对白场景": [["对白", "对话"], ["推近", "拉远"], ["视线", "站位"]],
    "美食特写": [["微距", "特写"], ["蒸汽", "酱汁", "拉丝"], ["慢镜头"]],
    "音乐MV/卡点": [["卡点", "节拍"], ["SpeedRamp", "WhipPan"], ["频闪", "舞台"]],
    "一镜到底": [["一镜到底", "不切"], ["Steadicam", "Gimbal"], ["穿过"]],
    "微距特效/万物生长": [["微距"], ["慢镜头"], ["水滴", "绽放", "冰晶"]],
    "汽车大片": [["航拍", "跟拍"], ["仰拍", "低角度"], ["车漆", "轮胎"]],
    "自然风光/航拍": [["航拍"], ["晨雾", "体积光"], ["瀑布", "花海", "山脊"]],
    "游戏PV/角色出场": [["Orbit", "环绕"], ["SpeedRamp"], ["定格", "Pose"]],
    "恐怖惊悚片段": [["负空间", "黑暗"], ["低调打光", "低饱和"], ["SlowPushIn", "WhipPan"]],
    "旅行/城市氛围片": [["POV", "街景"], ["Gimbal", "跟拍"], ["GoldenHour"]],
    "宠物/萌系": [["平视", "Eye-Level"], ["微距", "毛发"], ["慢镜头"]],
    "Before/After变身类": [["Static"], ["转场", "遮挡", "闪光"], ["同角度"]],
    "Meme/Loop/GIF风格短片": [["循环", "Loop"], ["回到原点"], ["Static", "Orbit"]],
    "时间静止/子弹时间": [["完全静止"], ["穿梭", "环绕"], ["定格"]],
    "极限第一人称视角": [["第一人称", "POV", "FPV"], ["视线转移"], ["拖影"]],
}
# 结构型场景：只查字段与登记，不查镜头卡关键词
STRUCTURAL = {
    "长视频场景化策略（30–180秒）", "视频编辑/剧情颠覆", "视频延长",
    "剧情补全与分镜图转视频", "多帧故事/多宫格分镜", "多镜头混剪序列",
}

def norm(name):
    return name.replace(" ", "").replace("　", "")

def main():
    story = json.load(open(sys.argv[1], encoding="utf-8"))
    shots = json.load(open(sys.argv[2], encoding="utf-8"))
    fails = []
    if "scenario" not in story:
        print("不通过 story.json 缺 scenario 字段（写 null 表示无场景）")
        print("结论：不通过，镜头卡没写完，不进视频")
        return
    sc = story.get("scenario")
    if not sc:
        print("场景：无")
        print("结论：通过")
        return
    known = {norm(k): k for k in list(SCENARIOS) + list(STRUCTURAL)}
    key = norm(sc)
    if key not in known:
        fails.append(f"场景名不在 23 个场景里：{sc}")
        print("不通过 " + fails[0])
        print("结论：不通过，镜头卡没写完，不进视频")
        return
    name = known[key]
    points = story.get("scenario_points") or []
    if len(points) < 2:
        fails.append(f"场景 {name} 的 scenario_points 不足 2 条（文字稿“场景模板”栏登记的已用关键点）")
    if name in SCENARIOS:
        text = " ".join(str(v) for shot in shots for v in shot.values())
        hits = [g for g in SCENARIOS[name]
                if any(k.lower() in text.lower() for k in g)]
        if len(hits) < 2:
            missed = [g for g in SCENARIOS[name] if g not in hits]
            fails.append(f"场景 {name} 的关键点未进镜头卡（命中 {len(hits)}/3 组，缺：{missed}）")
        print(f"场景：{name}，关键词命中 {len(hits)}/3 组")
    else:
        print(f"场景：{name}（结构型，只查登记）")
    for f in fails:
        print("不通过", f)
    print("结论：" + ("不通过，镜头卡没写完，不进视频" if fails else "通过"))

if __name__ == "__main__":
    main()
