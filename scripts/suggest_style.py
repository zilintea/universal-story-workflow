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
    (("恐怖", "悬疑", "惊悚", "鬼", "吓人"), "liveaction", "cel2d",
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
    # v3.27 新增风格映射（常用风格补齐）
    (("赛博朋克", "赛博", "未来都市"), "cyberpunk", "liveaction",
     "霓虹未来都市靠赛博朋克", None),
    (("像素", "复古游戏", "街机", "8位", "16位"), "pixelart", "cel2d",
     "像素块是复古游戏的本体", None),
    (("剪纸", "年画", "民间艺术"), "papercut", "inkwash",
     "红纸剪影合民间年味", None),
    (("皮影", "皮影戏"), "shadowpuppet", "papercut",
     "皮影是背光皮偶，不是剪纸", None),
    (("水彩", "淡彩"), "watercolor", "ghibli",
     "透明晕染合轻盈题材", None),
    (("王家卫", "文艺片", "雨夜霓虹"), "wongkarwai", "liveaction",
     "潮湿霓虹 + 抽帧 + 浅景深是王家卫的招牌", None),
    (("敦煌", "飞天", "壁画"), "dunhuang", "inkwash",
     "矿物颜料与飞天合敦煌", None),
    (("绘本", "睡前故事", "幼儿"), "picturebook", "ghibli",
     "蜡笔水彩合睡前绘本", None),
    (("素描", "线稿", "速写"), "sketch", "liveaction",
     "铅笔排线合草稿手绘感", None),
    (("低多边形", "几何", "扁平3D"), "lowpoly", "pixar3d",
     "面片几何合极简游戏感", None),
    (("扁平", "插画", "科普", "讲解"), "flat2d", "cel2d",
     "大色块扁平合科普讲解", None),
    (("油画", "古典油画", "肖像画"), "oilpainting", "liveaction",
     "厚重笔触与明暗合古典油画", None),
]

def suggest(prompt):
    for signals, primary, alt, reason, scenario in TABLE:
        if any(s in prompt for s in signals):
            out = {"primary": primary, "alternative": alt, "reason": reason,
                   "matched": [s for s in signals if s in prompt]}
            if scenario:
                out["scenario"] = scenario
            return out
    # v3.26：无匹配信号时不再默认 3D。风格跟提示词走，没有默认风格；
    # 未指定时 primary/alternative 为 null，剧本风格栏写“未指定”，
    # 提示词只写内容本身的视觉语言，不混入任何风格卡的描述。
    return {"primary": None, "alternative": None,
            "reason": "无匹配信号，风格未指定——按内容推断或由用户定，不默认 3D",
            "matched": []}

if __name__ == "__main__":
    print(json.dumps(suggest(" ".join(sys.argv[1:])), ensure_ascii=False, indent=1))
