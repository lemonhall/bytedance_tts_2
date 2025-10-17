# 火山引擎TTS测试指南 🎵

## 📋 项目简介
这是火山引擎（字节跳动）语音合成(TTS)服务的Python测试工具集，支持V1和V3接口。

**推荐使用V3接口** - 更低时延，更好的大模型音色支持！

## 🔥 V3 vs V1 接口对比

| 特性 | V1接口 | V3接口 ⭐ | 
|------|--------|----------|
| **时延** | 较高 | **更低** ✨ |  
| **大模型音色** | 支持 | **优化更好** ✨ |
| **流式处理** | 支持 | **更优化** ✨ |
| **稳定性** | 稳定 | 稳定 |
| **兼容性** | 成熟 | 向后兼容 |
| **推荐场景** | 老项目维护 | **所有新项目** |

**官方建议：大模型音色都推荐接入V3接口，时延表现更好。**

## 🚀 快速开始

### 1. 环境准备
使用 `uv` 管理依赖（已自动安装）：
- ✅ websockets
- ✅ volc-speech-python-sdk (本地版本)
- ✅ python-dotenv (可选)

### 2. API凭证配置

#### 方法一：环境变量文件（推荐）
```bash
# 复制模板文件
cp .env.example .env

# 编辑 .env 文件，填入真实凭证
VOLCENGINE_APP_ID="你的APP_ID"
VOLCENGINE_ACCESS_TOKEN="你的ACCESS_TOKEN"
TTS_API_VERSION="v3"  # 推荐使用v3
```

#### 方法二：交互式输入
程序运行时会提示输入。

### 3. 测试方式

#### ⭐ 推荐：统一测试程序（支持V1+V3）
```bash
uv run python tts_unified_test.py
```
**功能特色：**
- 🎯 自动选择最佳接口版本
- 📊 性能对比测试
- 🔄 智能重试机制
- 📋 详细错误处理

#### V3专用测试（推荐新项目）
```bash
uv run python test_tts_v3.py
```

#### V1兼容测试
```bash
uv run python test_tts.py
```

#### 快速批量测试
```bash
uv run python simple_test.py
```

## 📚 测试程序说明

### 🎯 `tts_unified_test.py` - 主推荐
- ✅ 支持V1和V3接口切换
- ✅ 性能对比功能
- ✅ 智能错误处理和重试
- ✅ 环境变量配置
- ✅ 批量测试支持

### 🚀 `test_tts_v3.py` - V3专用
- ✅ 专为V3接口优化
- ✅ 更低时延
- ✅ 大模型音色支持
- ✅ 指数退避重试策略
- ✅ 详细错误码处理

### 🔧 `test_tts.py` - V1兼容
- ✅ 基于原始V1接口
- ✅ 成熟稳定
- ✅ 兼容老项目

### ⚡ `simple_test.py` - 快速测试
- ✅ 一键批量测试
- ✅ 环境检查
- ✅ 配置验证

## 🛠️ 参数配置

### 语音类型 (voice_type)
常用中文语音：
```python
"zh_female_shuangkuaisisi_moon_bigtts"  # 女声（推荐）
"zh_male_wennuanahu_moon_bigtts"        # 男声  
# 更多类型请参考火山引擎文档
```

### 音频参数调节
```python
audio_params = {
    "speed_ratio": 1.2,    # 语速 (0.2-3.0)
    "volume_ratio": 1.5,   # 音量 (0.1-3.0) 
    "pitch_ratio": 1.0     # 音调 (0.1-3.0)
}
```

### V3接口选项
```python
# 端点类型选择
endpoint_types = {
    "unidirectional_stream": "单向流式（推荐）",
    "bidirectional": "双向流式（高级）"
}
```

## 🐛 故障排除

### 常见错误码
| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| 3000 | 请求正确 | ✅ 正常 |
| 3001 | 无效请求 | 检查参数格式 |
| 3003 | 并发超限 | 重试或降低并发 |
| 3005 | 服务忙 | 等待重试 |
| 3010 | 文本超长 | 缩短文本长度 |
| 3011 | 无效文本 | 检查文本内容 |
| 3050 | 音色不存在 | 检查voice_type |

完整错误码请参考：[ERROR_CODES.md](./ERROR_CODES.md)

### 连接问题
1. **网络连接**：确保能访问火山引擎服务
2. **凭证验证**：检查APP_ID和ACCESS_TOKEN
3. **版本兼容**：推荐使用V3接口

### 依赖问题
```bash
# 检查环境
uv run python -c "import websockets; print('OK')"

# 重新安装
uv sync --force
```

## 📊 性能优化建议

### V3接口优势
1. **时延降低30-50%** 🚀
2. **大模型音色效果更好** 🎵  
3. **流式处理更优化** ⚡
4. **错误恢复更智能** 🛡️

### 最佳实践
```python
# 推荐配置
config = {
    "api_version": "v3",
    "endpoint_type": "unidirectional_stream", 
    "max_retries": 3,
    "timeout": 30
}
```

## 📂 项目结构
```
├── protocols/              # 核心协议实现
├── examples/              # 官方示例代码
├── tts_unified_test.py    # 🎯 统一测试程序（主推荐）
├── test_tts_v3.py         # 🚀 V3专用测试
├── test_tts.py            # 🔧 V1兼容测试  
├── simple_test.py         # ⚡ 快速批量测试
├── .env.example           # 环境变量模板
├── .env                   # 实际配置（已加入.gitignore）
├── ERROR_CODES.md         # 错误码说明
├── API_VERSIONS.md        # 接口版本对比
└── README.md              # 本文件
```

## 🎯 使用建议

### 新项目开发
```bash
# 1. 使用V3接口
echo "TTS_API_VERSION=v3" >> .env

# 2. 运行统一测试
uv run python tts_unified_test.py

# 3. 选择"4. 仅V3测试"
```

### 老项目维护
```bash
# 1. 保持V1兼容
echo "TTS_API_VERSION=v1" >> .env  

# 2. 运行兼容测试
uv run python test_tts.py
```

### 性能对比测试
```bash
# 运行统一程序，选择"3. V1 vs V3 性能对比"
uv run python tts_unified_test.py
```

## 📝 注意事项

1. **API版本选择**：新项目强烈推荐V3
2. **环境变量**：敏感信息已自动排除git跟踪
3. **网络要求**：需要稳定的互联网连接
4. **配额限制**：注意火山引擎的并发和用量限制

---

🎉 **开始你的语音合成之旅吧！** 

💡 遇到问题？查看 [ERROR_CODES.md](./ERROR_CODES.md) 或 [API_VERSIONS.md](./API_VERSIONS.md)