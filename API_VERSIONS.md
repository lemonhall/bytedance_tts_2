# 火山引擎TTS接口版本对比

## V1 vs V3 接口对比

### V1 接口 (当前使用的)
- **WebSocket单向流式**: `wss://openspeech.bytedance.com/api/v1/tts/ws_binary`
- **HTTP非流式**: `https://openspeech.bytedance.com/api/v1/tts`
- **特点**: 传统接口，稳定但时延较高

### V3 接口 (推荐)
- **WebSocket单向流式**: `wss://openspeech.bytedance.com/api/v3/tts/unidirectional/stream`  
- **WebSocket双向流式**: `wss://openspeech.bytedance.com/api/v3/tts/bidirection`
- **HTTP单向流式**: `https://openspeech.bytedance.com/api/v3/tts/unidirectional`
- **特点**: **时延更低，大模型音色表现更好**

## 推荐升级原因
1. ✅ **更低时延** - 更快的语音生成
2. ✅ **大模型音色优化** - 针对新一代AI音色优化
3. ✅ **更好的流式体验** - 边合成边返回，实时性更强
4. ✅ **向后兼容** - 支持更多参数和功能

## 升级建议
- 对于**大模型音色** (如最新的AI声音)，强烈建议使用V3
- 对于**实时应用** (如对话系统)，V3的低时延优势明显
- 对于**批量处理**，V1和V3差别不大，但V3未来兼容性更好