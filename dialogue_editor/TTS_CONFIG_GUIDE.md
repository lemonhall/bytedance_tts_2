# TTS配置文件使用说明

## 📄 tts_config.py

这个文件包含了所有TTS相关的配置，你可以根据需要随时修改。

## 🎭 情感配置

### 中文情感 (CHINESE_EMOTIONS)

包含24种中文情感，格式为字典：

```python
CHINESE_EMOTIONS = {
    "开心": "happy",
    "悲伤": "sad",
    "生气": "angry",
    ...
}
```

- **键**: 中文显示名称（用于UI界面）
- **值**: 英文API标识（用于调用火山引擎API）

### 英文情感 (ENGLISH_EMOTIONS)

包含10种英文情感，格式相同。

## 🎤 音色配置

### 基础音色 (VOICE_TYPES)

```python
VOICE_TYPES = {
    "male_adult": "zh_male_wennuanahu_moon_bigtts",
    "female_adult": "zh_female_shuangkuaisisi_moon_bigtts",
    "male_child": "zh_male_yangguang_moon_bigtts",
    "female_child": "zh_female_tianmei_moon_bigtts",
}
```

### 详细音色信息 (VOICE_TYPE_DETAILS)

包含每个音色的详细信息：
- name: 音色名称
- gender: 性别
- age: 年龄段
- description: 描述

## 🔧 如何修改配置

### 添加新情感

在 `tts_config.py` 中的 `CHINESE_EMOTIONS` 字典中添加：

```python
CHINESE_EMOTIONS = {
    ...现有情感...,
    "新情感名称": "new_emotion_api_value"
}
```

### 添加新音色

1. 在 `VOICE_TYPES` 中添加基础配置：

```python
VOICE_TYPES = {
    ...现有音色...,
    "key_name": "actual_voice_id_from_volcengine"
}
```

2. 在 `VOICE_TYPE_DETAILS` 中添加详细信息：

```python
VOICE_TYPE_DETAILS = {
    ...现有音色...,
    "actual_voice_id_from_volcengine": {
        "name": "音色显示名称",
        "gender": "male/female",
        "age": "adult/child",
        "description": "音色描述"
    }
}
```

### 修改TTS参数范围

在 `TTS_PARAM_RANGES` 中修改：

```python
TTS_PARAM_RANGES = {
    "speed_ratio": {
        "min": 0.2,      # 最小值
        "max": 3.0,      # 最大值
        "default": 1.0,  # 默认值
        "description": "语速比例"
    },
    ...
}
```

## 🔌 在代码中使用

### 导入配置

```python
from tts_config import (
    CHINESE_EMOTION_NAMES,     # 中文情感名称列表
    CHINESE_EMOTIONS,          # 中文情感字典
    VOICE_TYPES,              # 音色配置
    get_voice_type,           # 获取音色的辅助函数
    get_emotion_value,        # 获取情感API值
    is_valid_emotion          # 验证情感是否有效
)
```

### 使用辅助函数

```python
# 根据性别和年龄获取音色
voice = get_voice_type("male", "adult")
# 返回: "zh_male_wennuanahu_moon_bigtts"

# 获取情感的API值
emotion_api = get_emotion_value("开心")
# 返回: "happy"

# 验证情感是否有效
is_valid = is_valid_emotion("开心")
# 返回: True
```

## 📝 注意事项

1. **API兼容性**: 确保添加的情感和音色在火山引擎TTS API中实际支持
2. **同步更新**: 修改配置后，前端和后端会自动使用新配置
3. **备份**: 修改前建议备份原配置文件
4. **测试**: 添加新配置后建议先小范围测试

## 🔄 自动生效

修改 `tts_config.py` 后：
- ✅ AI分析器会使用新的情感列表
- ✅ Web界面会显示新的选项
- ✅ TTS生成器会使用新的音色配置
- ✅ 无需重启服务（Python会自动重新加载）

## 🚀 快速测试

修改配置后，运行测试脚本验证：

```bash
python test_deepseek.py
```

或者直接启动服务：

```bash
python app.py
```

然后访问 http://localhost:8000 查看新配置是否生效。
