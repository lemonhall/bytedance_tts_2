# 火山引擎 TTS API 版本对照

## 概览

火山引擎提供了两个主要版本的TTS API：V1和V3。**推荐使用V3接口，时延表现更佳**。

## V1 接口 (兼容性支持)

### WebSocket 流式接口
- **端点**: `wss://openspeech.bytedance.com/api/v1/tts/ws_binary`
- **特点**: 
  - 单向流式传输
  - 兼容性好
  - 相对较高的时延

### HTTP 非流式接口  
- **端点**: `https://openspeech.bytedance.com/api/v1/tts`
- **特点**: 
  - 一次性返回完整音频
  - 适合小文本处理
  - 等待时间较长

## V3 接口 (推荐使用) ⭐

### WebSocket 单向流式 (推荐)
- **端点**: `wss://openspeech.bytedance.com/api/v3/tts/unidirectional/stream`
- **特点**: 
  - ✅ 最低时延
  - ✅ 边合成边返回
  - ✅ 适合实时场景

### WebSocket 双向流式
- **端点**: `wss://openspeech.bytedance.com/api/v3/tts/bidirection`
- **特点**: 
  - 支持双向通信
  - 可动态调整参数
  - 适合复杂交互场景

### HTTP 单向流式
- **端点**: `https://openspeech.bytedance.com/api/v3/tts/unidirectional`
- **特点**: 
  - HTTP协议流式返回
  - 相比V1时延更低
  - 适合HTTP环境

## 在项目中的配置

### .env 文件配置
```bash
# 推荐配置 - 使用V3单向WebSocket流式
TTS_API_VERSION=v3
TTS_V3_TYPE=unidirectional_ws

# 完整的V3端点配置
VOLCENGINE_V3_UNIDIRECTIONAL_WS=wss://openspeech.bytedance.com/api/v3/tts/unidirectional/stream
VOLCENGINE_V3_BIDIRECTIONAL_WS=wss://openspeech.bytedance.com/api/v3/tts/bidirection
VOLCENGINE_V3_UNIDIRECTIONAL_HTTP=https://openspeech.bytedance.com/api/v3/tts/unidirectional
```

### 在代码中使用
```python
# 自动选择最佳端点
endpoint = get_endpoint()  # 根据配置返回对应的V3端点

# V3单向WebSocket (推荐)
endpoint = "wss://openspeech.bytedance.com/api/v3/tts/unidirectional/stream"

# V3双向WebSocket  
endpoint = "wss://openspeech.bytedance.com/api/v3/tts/bidirection"

# V3 HTTP单向
endpoint = "https://openspeech.bytedance.com/api/v3/tts/unidirectional"
```

## 性能对比

| 接口版本 | 时延 | 实时性 | 兼容性 | 推荐场景 |
|---------|------|--------|--------|----------|
| V1 WS | 高 | 一般 | 最佳 | 兼容性要求高的场景 |
| V1 HTTP | 最高 | 差 | 好 | 小文本、非实时场景 |
| **V3 WS单向** | **最低** | **最佳** | 好 | **实时语音合成** ⭐ |
| V3 WS双向 | 低 | 很好 | 好 | 复杂交互场景 |
| V3 HTTP | 中等 | 好 | 最佳 | HTTP环境流式处理 |

## 迁移建议

1. **新项目**: 直接使用V3单向WebSocket接口
2. **现有项目**: 逐步迁移到V3，先保持V1作为备用
3. **实时应用**: 必须使用V3接口以获得最佳性能