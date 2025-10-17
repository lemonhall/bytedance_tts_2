# 火山引擎TTS V3完整测试套件# 火山引擎TTS V3完整测试套件



🎵 **火山引擎语音合成服务全面测试工具集** - 支持WebSocket/HTTP双协议，豆包2.0模型，情感合成，上下文控制🎵 **火山引擎语音合成服务全面测试工具集** - 支持WebSocket/HTTP双协议，豆包2.0模型，情感合成，上下文控制



## 🌟 功能特点## 🌟 功能特点



- ✅ **双协议支持**: WebSocket + HTTP流式接口- ✅ **双协议支持**: WebSocket + HTTP流式接口

- ✅ **豆包2.0**: 支持最新的豆包语音合成模型2.0- ✅ **豆包2.0**: 支持最新的豆包语音合成模型2.0

- ✅ **情感合成**: 24种中文情感 + 10种英文情感- ✅ **情感合成**: 24种中文情感 + 10种英文情感

- ✅ **上下文控制**: 智能语速、语气、音量调节- ✅ **上下文控制**: 智能语速、语气、音量调节

- ✅ **多音色混音**: 最多3个音色混合- ✅ **多音色混音**: 最多3个音色混合

- ✅ **日文支持**: 5种日文音色测试- ✅ **日文支持**: 5种日文音色测试

- ✅ **音频处理**: 自动合并WAV转高质量MP3- ✅ **音频处理**: 自动合并WAV转高质量MP3

- ✅ **批量测试**: 一键测试所有功能- ✅ **批量测试**: 一键测试所有功能



## 📁 文件结构## 📁 文件结构



### 🎯 核心实现### 🎯 核心实现

- `tts_universal.py` - WebSocket V3协议实现- `tts_universal.py` - WebSocket V3协议实现

- `tts_http_v3.py` - HTTP V3流式接口实现- `tts_http_v3.py` - HTTP V3流式接口实现

- `protocols/protocols.py` - 协议处理核心- `protocols/protocols.py` - 协议处理核心



### 🧪 功能测试### 🧪 功能测试

- `test_emotion.py` - 情感参数批量测试- `test_emotion.py` - 情感参数批量测试

- `test_context.py` - 上下文功能完整测试- `test_context.py` - 上下文功能完整测试

- `test_japanese.py` - 日文语音合成测试- `test_japanese.py` - 日文语音合成测试

- `test_mp3_output.py` - MP3格式输出测试- `test_mp3_output.py` - MP3格式输出测试



### 📚 使用示例### 📚 使用示例

- `tts_http_examples.py` - HTTP接口使用示例- `tts_http_examples.py` - HTTP接口使用示例

- `test_context_quick.py` - 上下文功能快速验证- `test_context_quick.py` - 上下文功能快速验证

- `test_japanese_quick.py` - 日文合成快速测试- `test_japanese_quick.py` - 日文合成快速测试

- `test_mp3_quick.py` - MP3输出快速测试- `test_mp3_quick.py` - MP3输出快速测试



### 🛠️ 工具脚本### 🛠️ 工具脚本

- `Merge-WAV-to-MP3.ps1` - PowerShell音频合并脚本- `Merge-WAV-to-MP3.ps1` - PowerShell音频合并脚本

- `merge_wav_to_mp3.bat` - 批处理音频合并工具- `merge_wav_to_mp3.bat` - 批处理音频合并工具



### 📖 文档说明### 📖 文档说明

- `README_HTTP.md` - HTTP接口详细文档- `README_HTTP.md` - HTTP接口详细文档

- `API_VERSIONS.md` / `ERROR_CODES.md` - API文档- `API_VERSIONS.md` / `ERROR_CODES.md` - API文档



## 🚀 快速开始## 🚀 快速开始



### 1. 环境准备### 1. 环境准备

```bash```bash

# 安装依赖# 安装依赖

pip install requests websockets python-dotenvpip install requests websockets python-dotenv



# 或使用uv (推荐)# 或使用uv (推荐)

uv syncuv sync

``````



### 2. 配置凭证### 2. 配置凭证

复制配置模板并填入真实信息：复制配置模板并填入真实信息：

```bash```bash

cp .env.template .envcp .env.template .env

# 编辑.env文件，填入：# 编辑.env文件，填入：

# VOLCENGINE_APP_ID=你的APP_ID# VOLCENGINE_APP_ID=你的APP_ID

# VOLCENGINE_ACCESS_TOKEN=你的访问令牌# VOLCENGINE_ACCESS_TOKEN=你的访问令牌

# TTS_V3_RESOURCE_ID=seed-tts-2.0# TTS_V3_RESOURCE_ID=seed-tts-2.0

``````



### 3. 选择测试方式### 3. 选择测试方式



#### 🎭 情感合成测试#### 🎭 情感合成测试

```bash```bash

python test_emotion.pypython test_emotion.py

# 测试24种中文情感效果 + 10种英文情感# 测试24种中文情感效果 + 10种英文情感

``````



#### 🗣️ 上下文控制测试  #### 🗣️ 上下文控制测试  

```bash```bash

python test_context.pypython test_context.py

# 智能语速/语气/音量控制# 智能语速/语气/音量控制

``````



#### 🗾 日文语音测试#### 🗾 日文语音测试

```bash```bash

python test_japanese.py  python test_japanese.py  

# 5种日文音色完整测试# 5种日文音色完整测试

``````



#### 🎵 音频格式测试#### 🎵 音频格式测试

```bash```bash

python test_mp3_output.pypython test_mp3_output.py

# 多种音频格式和比特率测试# 多种音频格式和比特率测试

``````



#### ⚡ 快速验证#### ⚡ 快速验证

```bash```bash

python test_context_quick.py    # 上下文效果对比python test_context_quick.py    # 上下文效果对比

python test_japanese_quick.py   # 日文合成验证  python test_japanese_quick.py   # 日文合成验证  

python test_mp3_quick.py        # MP3输出验证python test_mp3_quick.py        # MP3输出验证

``````



## 🎯 支持的功能## 🎯 支持的功能



### 🤖 支持的模型版本### 🤖 支持的模型版本

| 资源ID | 说明 | 音色兼容性 || 资源ID | 说明 | 音色兼容性 |

|--------|------|------------||--------|------|------------|

| `seed-tts-1.0` | 豆包1.0字符版 | 豆包1.0音色 || `seed-tts-1.0` | 豆包1.0字符版 | 豆包1.0音色 |

| `seed-tts-1.0-concurr` | 豆包1.0并发版 | 豆包1.0音色 || `seed-tts-1.0-concurr` | 豆包1.0并发版 | 豆包1.0音色 |

| `seed-tts-2.0` | 豆包2.0字符版 | 豆包2.0音色 || `seed-tts-2.0` | 豆包2.0字符版 | 豆包2.0音色 |

| `volc.megatts.default` | 复刻2.0字符版 | 复刻2.0音色 || `volc.megatts.default` | 复刻2.0字符版 | 复刻2.0音色 |



### 🎭 情感参数支持 (仅TTS 2.0)### 🎭 情感参数支持 (仅TTS 2.0)

**中文情感** (24种)：**中文情感** (24种)：

开心、悲伤、生气、惊讶、恐惧、厌恶、激动、冷漠、中性、沮丧、撒娇、害羞、安慰、紧张、温柔、讲故事、电台、磁性、广告、气泡音、ASMR、新闻、娱乐、方言开心、悲伤、生气、惊讶、恐惧、厌恶、激动、冷漠、中性、沮丧、撒娇、害羞、安慰、紧张、温柔、讲故事、电台、磁性、广告、气泡音、ASMR、新闻、娱乐、方言



**英文情感** (10种)：**英文情感** (10种)：

中性、愉悦、愤怒、悲伤、兴奋、对话、ASMR、温暖、深情、权威中性、愉悦、愤怒、悲伤、兴奋、对话、ASMR、温暖、深情、权威



### 🗣️ 上下文控制 (仅TTS 2.0)### 🗣️ 上下文控制 (仅TTS 2.0)

- **语速调整**: "你可以说慢一点吗？"- **语速调整**: "你可以说慢一点吗？"

- **情绪控制**: "你可以用开心的语气说话吗？"- **情绪控制**: "你可以用开心的语气说话吗？"

- **音量调节**: "你嗓门再小点"- **音量调节**: "你嗓门再小点"

- **风格控制**: "请用播音员的风格说话"- **风格控制**: "请用播音员的风格说话"



### 🎵 音频格式支持### 🎵 音频格式支持

- **WAV**: 无损质量，适合后期处理- **WAV**: 无损质量，适合后期处理

- **MP3**: 压缩格式，64k-320k比特率- **MP3**: 压缩格式，64k-320k比特率

- **PCM**: 原始音频，流式推荐- **PCM**: 原始音频，流式推荐

- **OGG_OPUS**: 高效压缩格式- **OGG_OPUS**: 高效压缩格式



### 🎤 采样率选项### 🎤 采样率选项

8000, 16000, 22050, **24000**, 32000, 44100, 48000 Hz8000, 16000, 22050, **24000**, 32000, 44100, 48000 Hz



## 🔧 高级功能## 🔧 高级功能



### 🎵 音频合并工具### 🎵 音频合并工具

将所有生成的WAV文件合并为高质量MP3：将所有生成的WAV文件合并为高质量MP3：



**PowerShell (推荐)**:**PowerShell (推荐)**:

```powershell```powershell

.\Merge-WAV-to-MP3.ps1.\Merge-WAV-to-MP3.ps1

# 自定义参数# 自定义参数

.\Merge-WAV-to-MP3.ps1 -OutputFile "my_audio.mp3" -BitRate 320.\Merge-WAV-to-MP3.ps1 -OutputFile "my_audio.mp3" -BitRate 320

``````



**批处理**:**批处理**:

```cmd```cmd

merge_wav_to_mp3.batmerge_wav_to_mp3.bat

``````



### 🌐 协议选择### 🌐 协议选择



#### HTTP流式 (推荐)#### HTTP流式 (推荐)

- ✅ 实现简单，稳定性高- ✅ 实现简单，稳定性高

- ✅ 支持连接复用- ✅ 支持连接复用

- ✅ 标准HTTP错误处理- ✅ 标准HTTP错误处理

- 📁 文件: `tts_http_v3.py`- 📁 文件: `tts_http_v3.py`



#### WebSocket#### WebSocket

- ✅ 实时双向通信- ✅ 实时双向通信

- ✅ 精确协议控制- ✅ 精确协议控制

- ⚠️ 实现复杂- ⚠️ 实现复杂

- 📁 文件: `tts_universal.py`- 📁 文件: `tts_universal.py`



## 📊 测试结果展示## 📊 测试结果展示



生成的测试音频文件会自动保存到当前目录：生成的测试音频文件会自动保存到当前目录：

- `emotion_zh_*.wav` - 中文情感测试- `emotion_zh_*.wav` - 中文情感测试

- `emotion_en_*.wav` - 英文情感测试  - `emotion_en_*.wav` - 英文情感测试  

- `context_*.wav` - 上下文控制测试- `context_*.wav` - 上下文控制测试

- `japanese_*.wav` - 日文语音测试- `japanese_*.wav` - 日文语音测试

- `mp3_test_*.mp3` - MP3格式测试- `mp3_test_*.mp3` - MP3格式测试

- `all_audio_combined.mp3` - 合并后的完整音频- `all_audio_combined.mp3` - 合并后的完整音频



## 🎯 最佳实践## 🎯 最佳实践



1. **推荐配置**: 使用 `seed-tts-2.0` + 24000Hz采样率1. **推荐配置**: 使用 `seed-tts-2.0` + 24000Hz采样率

2. **情感合成**: 配合合适的文本内容效果更佳2. **情感合成**: 配合合适的文本内容效果更佳

3. **上下文控制**: 比emotion参数更灵活自然3. **上下文控制**: 比emotion参数更灵活自然

4. **音频格式**: 流式场景用PCM，存储用WAV，分发用MP34. **音频格式**: 流式场景用PCM，存储用WAV，分发用MP3

5. **性能优化**: HTTP协议 + 连接复用 + 缓存功能5. **性能优化**: HTTP协议 + 连接复用 + 缓存功能



## 🔍 故障排除## 🔍 故障排除



### 常见错误码### 常见错误码

- `20000000`: 正常完成- `20000000`: 正常完成

- `40402003`: 文本长度超限  - `40402003`: 文本长度超限  

- `45000000`: 音色权限错误- `45000000`: 音色权限错误

- `55000000`: 服务端内部错误- `55000000`: 服务端内部错误



### 调试技巧### 调试技巧

1. 检查资源ID与音色匹配1. 检查资源ID与音色匹配

2. 确认账户权限2. 确认账户权限

3. 查看LogID定位问题3. 查看LogID定位问题

4. 检查网络连接稳定性4. 检查网络连接稳定性



## 📚 扩展阅读## 📚 扩展阅读



- [HTTP接口详细文档](README_HTTP.md)- [HTTP接口详细文档](README_HTTP.md)

- [API版本说明](API_VERSIONS.md) - [API版本说明](API_VERSIONS.md) 

- [错误码对照表](ERROR_CODES.md)- [错误码对照表](ERROR_CODES.md)

- [火山引擎官方文档](https://www.volcengine.com/docs/6561/1598757)- [火山引擎官方文档](https://www.volcengine.com/docs/6561/1598757)



## 🤝 贡献## 🤝 贡献



欢迎提交Issue和Pull Request来改进这个项目！欢迎提交Issue和Pull Request来改进这个项目！



## 📄 许可证## 📄 许可证



本项目仅供学习和测试使用，请遵守火山引擎的服务条款。本项目仅供学习和测试使用，请遵守火山引擎的服务条款。
    )
    print("成功!" if success else "失败!")

asyncio.run(my_test())
```

## 📝 参数说明

### 语音类型 (voice_type)
常用的中文语音类型：
- `zh_female_shuangkuaisisi_moon_bigtts` - 女声
- `zh_male_wennuanahu_moon_bigtts` - 男声  
- 更多类型请参考火山引擎文档

### 音频参数
可以在 `test_tts.py` 中的 `request_data` 修改：
- `speed_ratio`: 语速比例 (0.2-3.0)
- `volume_ratio`: 音量比例 (0.1-3.0) 
- `pitch_ratio`: 音调比例 (0.1-3.0)

## 🛠️ 故障排除

### 1. 连接错误
- 检查网络连接
- 确认APP_ID和ACCESS_TOKEN正确
- 查看日志中的具体错误信息

### 2. 没有音频输出
- 检查语音类型是否支持
- 确认文本内容不为空
- 查看服务器返回的错误码

### 3. 依赖问题
运行检查脚本：
```bash
uv run python simple_test.py
```

## 📂 项目结构
```
├── protocols/          # 核心协议实现
├── examples/           # 官方示例
├── test_tts.py         # 完整测试程序
├── simple_test.py      # 简化测试程序
├── pyproject.toml      # 项目配置
└── README.md           # 这个文件
```

## 🎯 使用建议

1. **开发阶段**: 使用交互式测试快速验证
2. **批量处理**: 使用配置文件测试
3. **生产集成**: 参考 `test_tts.py` 中的 `test_tts` 函数

---

💡 **提示**: 这是一个本地源码包，每次使用都需要在虚拟环境中安装。使用 `uv run` 可以自动激活环境并运行代码。