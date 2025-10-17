"""
TTS配置文件 - 情感列表和音色配置
这个文件包含了火山引擎TTS支持的所有情感和音色配置
可以根据需要随时修改
"""

# ============================================
# 情感配置 (Emotion Configuration)
# ============================================

# 中文情感列表 (Chinese Emotions)
# 支持的情感及其英文标识
CHINESE_EMOTIONS = {
    "开心": "happy",
    "悲伤": "sad",
    "生气": "angry",
    "惊讶": "surprised",
    "恐惧": "fear",
    "厌恶": "hate",
    "激动": "excited",
    "冷漠": "coldness",
    "中性": "neutral",
    "沮丧": "depressed",
    "撒娇": "lovey-dovey",
    "害羞": "shy",
    "安慰": "comfort",
    "紧张": "tension",
    "温柔": "tender",
    "讲故事": "storytelling",
    "电台": "radio",
    "磁性": "magnetic",
    "广告": "advertising",
    "气泡音": "vocal-fry",
    "ASMR": "asmr",
    "新闻": "news",
    "娱乐": "entertainment",
    "方言": "dialect"
}

# 英文情感列表 (English Emotions)
ENGLISH_EMOTIONS = {
    "中性": "neutral",
    "愉悦": "happy",
    "愤怒": "angry",
    "悲伤": "sad",
    "兴奋": "excited",
    "对话": "chat",
    "ASMR": "asmr",
    "温暖": "warm",
    "深情": "affectionate",
    "权威": "authoritative"
}

# 仅中文名称列表 (用于UI显示)
CHINESE_EMOTION_NAMES = list(CHINESE_EMOTIONS.keys())
ENGLISH_EMOTION_NAMES = list(ENGLISH_EMOTIONS.keys())

# 仅英文标识列表 (用于API调用)
CHINESE_EMOTION_VALUES = list(CHINESE_EMOTIONS.values())
ENGLISH_EMOTION_VALUES = list(ENGLISH_EMOTIONS.values())


# ============================================
# 音色配置 (Voice Type Configuration)
# 严格按照火山引擎TTS 2.0支持的音色列表
# ============================================

# 常用音色配置 (用于快速选择)
# 使用你提供的列表中的音色作为默认
VOICE_TYPES = {
    # 成年男性 - 使用儒雅逸辰
    "male_adult": "zh_male_ruyayichen_saturn_bigtts",
    
    # 成年女性 - 使用vivi
    "female_adult": "zh_female_vv_uranus_bigtts",
    
    # 男性少年 - 使用爽朗少年
    "male_teenager": "ICL_zh_male_shuanglangshaonian_tob",
    
    # 女性少年 - 使用可爱女生
    "female_teenager": "ICL_zh_female_keainvsheng_tob",
}

# 详细音色列表 (严格限定在提供的列表中)
VOICE_TYPE_DETAILS = {
    # 通用场景
    "zh_female_vv_uranus_bigtts": {
        "name": "vivi",
        "gender": "female",
        "age": "adult",
        "category": "通用场景",
        "language": "中文、英语",
        "description": "通用女声，支持中英文",
        "support_mix": False
    },
    
    # 视频配音系列
    "zh_male_dayi_saturn_bigtts": {
        "name": "大壹",
        "gender": "male",
        "age": "adult",
        "category": "视频配音",
        "language": "中文",
        "description": "适合视频配音的男声",
        "support_mix": False
    },
    "zh_female_mizai_saturn_bigtts": {
        "name": "黑猫侦探社咪仔",
        "gender": "female",
        "age": "teenager",
        "category": "视频配音",
        "language": "中文",
        "description": "黑猫侦探社咪仔",
        "support_mix": False
    },
    "zh_female_jitangnv_saturn_bigtts": {
        "name": "鸡汤女",
        "gender": "female",
        "age": "adult",
        "category": "视频配音",
        "language": "中文",
        "description": "温暖治愈系女声",
        "support_mix": False
    },
    "zh_female_meilinvyou_saturn_bigtts": {
        "name": "魅力女友",
        "gender": "female",
        "age": "adult",
        "category": "视频配音",
        "language": "中文",
        "description": "魅力十足的女友音",
        "support_mix": False
    },
    "zh_female_santongyongns_saturn_bigtts": {
        "name": "流畅女声",
        "gender": "female",
        "age": "adult",
        "category": "视频配音",
        "language": "中文",
        "description": "流畅自然的女声",
        "support_mix": False
    },
    "zh_male_ruyayichen_saturn_bigtts": {
        "name": "儒雅逸辰",
        "gender": "male",
        "age": "adult",
        "category": "视频配音",
        "language": "中文",
        "description": "儒雅有内涵的男声",
        "support_mix": False
    },
    
    # 角色扮演系列
    "ICL_zh_female_keainvsheng_tob": {
        "name": "可爱女生",
        "gender": "female",
        "age": "teenager",
        "category": "角色扮演",
        "language": "中文",
        "description": "可爱活泼的女生角色",
        "support_mix": False
    },
    "ICL_zh_female_tiaopigongzhu_tob": {
        "name": "调皮公主",
        "gender": "female",
        "age": "teenager",
        "category": "角色扮演",
        "language": "中文",
        "description": "调皮可爱的公主角色",
        "support_mix": False
    },
    "ICL_zh_male_shuanglangshaonian_tob": {
        "name": "爽朗少年",
        "gender": "male",
        "age": "teenager",
        "category": "角色扮演",
        "language": "中文",
        "description": "爽朗阳光的少年角色",
        "support_mix": False
    },
    "ICL_zh_male_tiancaitongzhuo_tob": {
        "name": "天才同桌",
        "gender": "male",
        "age": "teenager",
        "category": "角色扮演",
        "language": "中文",
        "description": "聪明伶俐的同桌角色",
        "support_mix": False
    },
}

# 按分类组织的音色
VOICE_TYPES_BY_CATEGORY = {
    "通用场景": [
        "zh_female_vv_uranus_bigtts",
    ],
    "视频配音": [
        "zh_male_dayi_saturn_bigtts",
        "zh_female_mizai_saturn_bigtts",
        "zh_female_jitangnv_saturn_bigtts",
        "zh_female_meilinvyou_saturn_bigtts",
        "zh_female_santongyongns_saturn_bigtts",
        "zh_male_ruyayichen_saturn_bigtts",
    ],
    "角色扮演": [
        "ICL_zh_female_keainvsheng_tob",
        "ICL_zh_female_tiaopigongzhu_tob",
        "ICL_zh_male_shuanglangshaonian_tob",
        "ICL_zh_male_tiancaitongzhuo_tob",
    ],
}


# ============================================
# 辅助函数 (Helper Functions)
# ============================================

def get_emotion_value(chinese_name: str, language: str = "chinese") -> str:
    """
    根据中文情感名称获取英文标识
    
    Args:
        chinese_name: 中文情感名称，如"开心"
        language: 语言类型，"chinese"或"english"
        
    Returns:
        英文标识，如"happy"
    """
    emotions = CHINESE_EMOTIONS if language == "chinese" else ENGLISH_EMOTIONS
    return emotions.get(chinese_name, "neutral")


def get_voice_type(gender: str, age_group: str = "adult") -> str:
    """
    根据性别和年龄段获取音色ID
    
    Args:
        gender: 性别，"male"或"female"
        age_group: 年龄段，"child"、"teenager"或"adult"
        
    Returns:
        音色ID字符串
    """
    # child映射到teenager（因为列表中没有child分类）
    if age_group == "child":
        age_group = "teenager"
    
    key = f"{gender}_{age_group}"
    
    # 如果没有找到对应的，使用成人音色作为默认
    if key not in VOICE_TYPES:
        key = f"{gender}_adult"
    
    return VOICE_TYPES.get(key, VOICE_TYPES["male_adult"])


def get_voice_info(voice_id: str) -> dict:
    """
    获取音色的详细信息
    
    Args:
        voice_id: 音色ID
        
    Returns:
        音色详细信息字典
    """
    return VOICE_TYPE_DETAILS.get(voice_id, {
        "name": "未知音色",
        "gender": "male",
        "age": "adult",
        "category": "通用场景",
        "description": ""
    })


def get_voices_by_category(category: str) -> list:
    """
    获取指定分类的所有音色
    
    Args:
        category: 分类名称，如"视频配音"、"角色扮演"
        
    Returns:
        音色ID列表
    """
    return VOICE_TYPES_BY_CATEGORY.get(category, [])


def get_all_voice_categories() -> list:
    """
    获取所有音色分类
    
    Returns:
        分类名称列表
    """
    return list(VOICE_TYPES_BY_CATEGORY.keys())


def search_voices(keyword: str = "", gender: str = "", category: str = "") -> list:
    """
    搜索符合条件的音色
    
    Args:
        keyword: 关键词（在名称和描述中搜索）
        gender: 性别筛选
        category: 分类筛选
        
    Returns:
        符合条件的音色ID列表
    """
    results = []
    
    for voice_id, info in VOICE_TYPE_DETAILS.items():
        # 性别筛选
        if gender and info.get("gender") != gender:
            continue
        
        # 分类筛选
        if category and info.get("category") != category:
            continue
        
        # 关键词搜索
        if keyword:
            keyword_lower = keyword.lower()
            if (keyword_lower not in info.get("name", "").lower() and
                keyword_lower not in info.get("description", "").lower()):
                continue
        
        results.append(voice_id)
    
    return results


def is_valid_emotion(emotion: str, language: str = "chinese") -> bool:
    """
    检查情感是否有效
    
    Args:
        emotion: 情感名称或标识
        language: 语言类型
        
    Returns:
        是否有效
    """
    emotions = CHINESE_EMOTIONS if language == "chinese" else ENGLISH_EMOTIONS
    return emotion in emotions or emotion in emotions.values()


def is_valid_voice(voice_id: str) -> bool:
    """
    检查音色ID是否有效
    
    Args:
        voice_id: 音色ID
        
    Returns:
        是否有效
    """
    return voice_id in VOICE_TYPE_DETAILS


# ============================================
# TTS参数配置 (TTS Parameters)
# ============================================

TTS_PARAM_RANGES = {
    "speed_ratio": {
        "min": 0.2,
        "max": 3.0,
        "default": 1.0,
        "description": "语速比例"
    },
    "volume_ratio": {
        "min": 0.1,
        "max": 3.0,
        "default": 1.0,
        "description": "音量比例"
    },
    "pitch_ratio": {
        "min": 0.1,
        "max": 3.0,
        "default": 1.0,
        "description": "音调比例"
    }
}

# 默认TTS参数
DEFAULT_TTS_PARAMS = {
    "speed_ratio": 1.0,
    "volume_ratio": 1.0,
    "pitch_ratio": 1.0,
    "sample_rate": 24000,
    "audio_format": "wav"
}


# ============================================
# 导出配置 (用于向后兼容)
# ============================================

# 为了保持向后兼容，导出原有的列表格式
CHINESE_EMOTIONS_LIST = CHINESE_EMOTION_NAMES
ENGLISH_EMOTIONS_LIST = ENGLISH_EMOTION_NAMES
