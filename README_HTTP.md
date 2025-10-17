# 火山引擎TTS V3 HTTP接口实现

基于HTTP流式接口的火山引擎语音合成服务，支持豆包语音合成模型2.0、复刻2.0和混音功能。

## 功能特点

- ✅ HTTP流式接口，比WebSocket更简单稳定
- ✅ 支持豆包语音合成模型1.0/2.0
- ✅ 支持声音复刻2.0
- ✅ 支持多音色混音(Mix)
- ✅ 支持上下文情感合成(TTS2.0专用)
- ✅ 连接复用，提升性能
- ✅ 完整的错误处理和日志记录
- ✅ 支持多种音频格式(WAV/MP3/PCM/OGG_OPUS)

## 快速开始

### 1. 安装依赖

```bash
pip install requests python-dotenv
```

### 2. 配置环境变量

复制配置模板:
```bash
cp .env.template .env
```

编辑 `.env` 文件，填入您的配置:
```bash
# 必需配置
VOLCENGINE_APP_ID=你的APP_ID
VOLCENGINE_ACCESS_TOKEN=你的访问令牌

# 可选配置
TTS_V3_RESOURCE_ID=seed-tts-2.0
VOLCENGINE_VOICE_TYPE=zh_female_vv_uranus_bigtts
```

### 3. 运行测试

交互式测试:
```bash
python tts_http_v3.py
```

代码示例:
```bash
python tts_http_examples.py
```

## 使用方法

### 基础合成

```python
from tts_http_v3 import TTSHttpClient

client = TTSHttpClient()

# 简单合成
client.synthesize_speech(
    text="你好，世界！",
    output_file="hello.wav"
)

client.close()
```

### 高级参数

```python
# 带参数的合成
client.synthesize_speech(
    text="快速语音测试",
    output_file="fast.wav",
    speech_rate=50,        # 语速 (-50到100)
    loudness_rate=20,      # 音量 (-50到100)  
    audio_format="mp3",    # 音频格式
    sample_rate=24000,     # 采样率
    emotion="happy",       # 情感(部分音色支持)
    emotion_scale=4,       # 情感强度(1-5)
    use_cache=True         # 启用缓存
)
```

### TTS 2.0 上下文合成

```python
# 需要使用 seed-tts-2.0 资源
client = TTSHttpClient()
client.resource_id = "seed-tts-2.0"

client.synthesize_speech(
    text="今天天气真不错",
    output_file="context.wav",
    context_texts=["你可以用开心的语气说话吗？"]  # 上下文提示
)
```

### 混音合成

```python
# 多音色混音
mix_speakers = [
    {"source_speaker": "zh_male_bvlazysheep", "mix_factor": 0.4},
    {"source_speaker": "zh_female_shuangkuaisisi_moon_bigtts", "mix_factor": 0.6}
]

client.synthesize_with_mix(
    text="这是混音效果",
    output_file="mix.wav", 
    mix_speakers=mix_speakers
)
```

## 支持的资源ID

| 资源ID | 说明 | 音色兼容性 |
|--------|------|------------|
| `seed-tts-1.0` | 豆包1.0字符版 | 豆包1.0音色 |
| `seed-tts-1.0-concurr` | 豆包1.0并发版 | 豆包1.0音色 |
| `seed-tts-2.0` | 豆包2.0字符版 | 豆包2.0音色 |
| `volc.megatts.default` | 复刻2.0字符版 | 复刻2.0音色 |
| `volc.megatts.concurr` | 复刻2.0并发版 | 复刻2.0音色 |

## 支持的音频格式

- `wav` - WAV格式(推荐流式使用pcm)
- `mp3` - MP3格式
- `pcm` - PCM原始音频
- `ogg_opus` - OGG Opus格式

## 采样率选项

支持: 8000, 16000, 22050, 24000, 32000, 44100, 48000 Hz

## 错误处理

程序包含完整的错误处理机制:

- HTTP请求错误
- 服务端错误码处理
- JSON解析错误
- 文件IO错误
- 网络超时处理

常见错误码:
- `20000000`: 正常结束
- `40402003`: 文本长度超限
- `45000000`: 音色权限错误
- `55000000`: 服务端内部错误

## 性能优化

1. **连接复用**: 使用 `requests.Session()` 复用TCP连接
2. **流式处理**: 边接收边处理音频数据
3. **缓存功能**: 相同文本可启用缓存加速
4. **并发版本**: 对于高并发场景使用并发版资源ID

## 注意事项

1. **资源ID匹配**: 确保资源ID与音色兼容
2. **混音限制**: 最多支持3个音色混音，权重总和必须为1
3. **TTS2.0功能**: 上下文合成等功能仅在2.0版本可用
4. **音色权限**: 确保账户有对应音色的使用权限
5. **网络稳定**: 流式接口需要稳定的网络连接

## 与WebSocket版本对比

| 特性 | HTTP版本 | WebSocket版本 |
|------|----------|---------------|
| 实现复杂度 | 简单 | 复杂 |
| 连接稳定性 | 高 | 中等 |
| 实时性 | 流式 | 实时 |
| 错误处理 | 简单 | 复杂 |
| 连接复用 | 支持 | 需要重连 |
| 推荐场景 | 批量处理 | 实时交互 |

## 文件说明

- `tts_http_v3.py` - 主要实现文件
- `tts_http_examples.py` - 使用示例
- `.env.template` - 配置文件模板
- `README_HTTP.md` - 本说明文档

## 更新日志

- 2025.10.17: 创建HTTP版本实现
- 支持完整的V3 HTTP流式接口
- 支持豆包2.0、复刻2.0、混音功能
- 添加连接复用和错误处理