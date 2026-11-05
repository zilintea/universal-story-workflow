#!/usr/bin/env python3
"""风格建议（v2.9）：按一句话提示里的题材/IP 信号，给主推 + 备选 + 理由 + 命中的场景。
用法：python suggest_style.py "一句话提示"
只建议，不锁定；锁定发生在文字稿关卡 1。用户没别的提示时用主推。
建议表见 docs/STYLE_SUGGESTION.md（v2.9 评估后）；场景见 docs/SCENARIO_TEMPLATES.md。
"""
import sys, json

TABLE = [
    (("西游", "神话", "仙侠", "封神", "八仙", "哪吒"), "guoman3d", "disneypixar3d",
     "中国风 3D 才是仙侠的原生质感；迪士尼与皮克斯只在喜剧合家欢时用", "仙侠/奇幻动画"),
    (("红楼", "古典", "诗词", "典故", "卖炭翁"), "inkwash", "liveaction",
     "水墨留白合古典气质", None),
    (("美食", "吃播", "菜谱"), "liveaction", "pixar3d",
     "写实特写拍得出油光蒸汽", "美食特写"),
    (("做饭", "现代", "日常", "职场", "生活"), "liveaction", "pixar3d",
     "真人写实最省解释成本", None),
    (("儿童", "动物", "原创", "卡通"), "pixar3d", "ghibli",
     "圆润 3D 最稳，儿童接受度最高", None),
    (("科幻", "未来", "太空"), "pixar3d", "cel2d",
     "3D 质感合科技感", None),
    (("历史", "写实", "传记"), "liveaction", "inkwash",
     "真人写实最可信", None),
    (("恐怖", "悬疑", "惊悚"), "liveaction", "cel2d",
     "恐怖靠低调打光和负空间，动画向才用扁平 2D", "恐怖惊悚片段"),
    # 以下按场景模板匹配（见 docs/SCENARIO_TEMPLATES.md）：题材已定风格时优先用场景行
    (("汽车", "赛车", "公路"), "liveaction", "pixar3d",
     "金属光泽和路面反射靠写实", "汽车大片"),
    (("宠物", "猫", "狗", "萌"), "liveaction", "pixar3d",
     "暖色柔光 + 平视机位拍毛发质感", "宠物/萌系"),
    (("旅行", "城市", "Vlog", "街头"), "liveaction", "ghibli",
     "蒙太奇碎片拼贴，生活化自然光", "旅行/城市氛围片"),
    (("游戏", "PV", "角色出场", "登场"), "pixar3d", "cel2d",
     "高精度 CG + 技能光效", "游戏 PV / 角色出场"),
    (("MV", "卡点", "舞蹈"), "liveaction", "cel2d",
     "节拍命中动作，音画同步", "音乐MV/卡点"),
    (("一镜到底", "长镜头"), "liveaction", "pixar3d",
     "Steadicam 全程不切", "一镜到底"),
    (("风光", "航拍", "山水"), "liveaction", "ghibli",
     "自然光 + 大气透视", "自然风光/航拍"),
    (("微距", "绽放", "水滴"), "liveaction", "pixar3d",
     "浅景深 + 慢镜头拍微观物理", "微距特效/万物生长"),
    (("变身", "改造", "换装"), "liveaction", "pixar3d",
     "前后同机位对比", "Before/After 变身类"),
    (("循环", "Loop", "GIF"), "pixar3d", "cel2d",
     "首尾帧无缝衔接", "Meme/Loop/GIF 风格短片"),
    (("子弹时间", "时间静止"), "liveaction", "pixar3d",
     "场景完全静止 + 穿梭运镜", "时间静止/子弹时间"),
    (("第一人称", "POV", "FPV", "飞剑"), "liveaction", "pixar3d",
     "视线转移写清顺序", "极限第一人称视角"),
]

def suggest(prompt):
    for signals, primary, alt, reason, scenario in TABLE:
        if any(s in prompt for s in signals):
            out = {"primary": primary, "alternative": alt, "reason": reason,
                   "matched": [s for s in signals if s in prompt]}
            if scenario:
                out["scenario"] = scenario
            return out
    return {"primary": "pixar3d", "alternative": "ghibli",
            "reason": "默认最稳组合", "matched": []}

if __name__ == "__main__":
    print(json.dumps(suggest(" ".join(sys.argv[1:])), ensure_ascii=False, indent=1))
