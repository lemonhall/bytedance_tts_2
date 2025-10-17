# 对话TTS编辑器 - 项目总览

## 📋 项目概述

这是一个基于Web的可视化对话TTS编辑器,用于快速创建多人对话的语音合成工程。

### 核心功能

1. **智能分析**: 输入纯文本对话,AI自动识别说话人、性别、年龄和情感
2. **可视化编辑**: Web界面实时调整所有TTS参数
3. **批量生成**: 一键生成整段对话音频并自动拼接
4. **工程管理**: 保存/加载工程文件,支持重新生成单句

### 设计亮点

- ✅ **轻量级**: Python后端仅3个核心依赖(FastAPI + Pydantic + Uvicorn)
- ✅ **无框架前端**: 纯JavaScript,无需npm/webpack等构建工具
- ✅ **美观界面**: 现代化Material Design风格,响应式布局
- ✅ **工程化**: JSON格式工程文件,便于版本控制和分享

## 🏗️ 技术架构

```
┌─────────────────────────────────────────────────┐
│                   前端 (Web UI)                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │ 输入编辑 │  │ 参数调整 │  │ 音频预览 │      │
│  └──────────┘  └──────────┘  └──────────┘      │
│         HTML + CSS + Vanilla JavaScript         │
└─────────────────────────────────────────────────┘
                        ↕ REST API
┌─────────────────────────────────────────────────┐
│              后端 (FastAPI Server)               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │ 对话分析 │  │ TTS生成  │  │ 工程管理 │      │
│  └──────────┘  └──────────┘  └──────────┘      │
│         ai_analyzer.py + tts_generator.py       │
└─────────────────────────────────────────────────┘
         ↕                  ↕                 ↕
    DeepSeek API    火山引擎TTS API      FFmpeg
```

## 📂 文件结构

```
dialogue_editor/
│
├── app.py                      # FastAPI Web服务器
├── project_schema.py           # Pydantic数据模型
├── ai_analyzer.py              # AI对话分析器
├── tts_generator.py            # TTS音频生成器
│
├── static/                     # 前端静态文件
│   ├── index.html             # 主页面
│   ├── style.css              # 样式表
│   └── app.js                 # 前端逻辑
│
├── projects/                   # 工程文件存储目录
├── dialogue_output/            # 音频输出目录
│
├── requirements.txt            # Python依赖
├── .env.template              # 环境变量模板
├── README.md                  # 使用文档
├── start.ps1                  # 启动脚本(PowerShell)
└── test.py                    # 功能测试
```

## 🔄 工作流程

### 1. 输入对话 (用户)
```
你好,最近怎么样?
挺好的,就是工作有点累。
那要注意休息啊!
```

### 2. AI分析 (DeepSeek)
```json
{
  "speakers": [
    {"id": "speaker_1", "gender": "male", "age_group": "adult"},
    {"id": "speaker_2", "gender": "female", "age_group": "adult"}
  ],
  "dialogues": [
    {"speaker_id": "speaker_1", "text": "你好,最近怎么样?", "emotion": "中性"},
    {"speaker_id": "speaker_2", "text": "挺好的,就是工作有点累。", "emotion": "疲惫"},
    {"speaker_id": "speaker_1", "text": "那要注意休息啊!", "emotion": "关心"}
  ]
}
```

### 3. 可视化编辑 (Web UI)
- 修改说话人名称和音色
- 调整每句话的情感、语速、音量、音调
- 重新生成单句音频

### 4. 批量生成 (TTS + FFmpeg)
```
line_000.wav (你好,最近怎么样?)
line_001.wav (挺好的,就是工作有点累。)
line_002.wav (那要注意休息啊!)
       ↓ FFmpeg合并
final_merged.wav
```

## 🎯 数据模型

### DialogueProject (工程文件)
```python
{
    "version": "1.0",
    "title": "对话标题",
    "original_text": "原始文本",
    "speakers": [...],          # 说话人列表
    "dialogues": [...],         # 对话列表
    "output_audio": "路径",      # 最终音频
    "created_at": "时间戳",
    "updated_at": "时间戳"
}
```

### Speaker (说话人)
```python
{
    "id": "speaker_1",
    "name": "小明",
    "gender": "male|female|child",
    "age_group": "child|teenager|adult|elder",
    "voice_type": "zh_male_..."  # 火山引擎音色ID
}
```

### DialogueLine (对话行)
```python
{
    "id": "line_1",
    "speaker_id": "speaker_1",
    "text": "对话内容",
    "emotion": "开心",              # 24种中文情感
    "speed_ratio": 1.0,            # 0.2-3.0
    "volume_ratio": 1.0,           # 0.1-3.0
    "pitch_ratio": 1.0,            # 0.1-3.0
    "context": "上一句对话",        # 用于上下文理解
    "audio_file": "生成的音频路径",
    "duration": 2.5                # 音频时长
}
```

## 🔌 API接口

### 分析对话
```http
POST /api/analyze
Content-Type: application/json

{
  "text": "对话文本"
}

Response:
{
  "project_id": "uuid",
  "project": { ... }
}
```

### 获取配置
```http
GET /api/config

Response:
{
  "emotions": {
    "chinese": ["开心", "悲伤", ...],
    "english": [...]
  },
  "voice_types": { ... },
  "tts_params": { ... }
}
```

### 更新对话行
```http
PUT /api/projects/{project_id}/line/{line_id}
Content-Type: application/json

{
  "emotion": "开心",
  "speed_ratio": 1.2
}
```

### 生成全部音频
```http
POST /api/projects/{project_id}/generate

Response:
{
  "success": true,
  "audio_url": "/audio/project_id_final.wav"
}
```

### 重新生成单句
```http
POST /api/projects/{project_id}/generate-line/{line_id}

Response:
{
  "success": true,
  "audio_url": "/audio/line_001.wav"
}
```

### 列出工程
```http
GET /api/projects

Response:
{
  "projects": [
    {
      "id": "uuid",
      "title": "标题",
      "created_at": "...",
      "updated_at": "..."
    }
  ]
}
```

## 🎨 UI设计

### 颜色方案
- Primary: `#6366f1` (靛蓝)
- Secondary: `#8b5cf6` (紫色)
- Success: `#10b981` (绿色)
- Danger: `#ef4444` (红色)
- Background: `#f8fafc` (浅灰)

### 交互流程
1. **步骤1 - 输入**: 大文本框 + AI分析按钮
2. **步骤2 - 编辑**: 说话人卡片 + 对话列表 + 参数滑块
3. **步骤3 - 预览**: 音频播放器 + 下载按钮

### 响应式设计
- 桌面: 双栏布局(说话人 + 对话)
- 平板: 单栏堆叠
- 手机: 简化界面,垂直滚动

## 🔧 依赖说明

### Python依赖 (最小化)
- **fastapi** (0.104.0+): Web框架
- **uvicorn** (0.24.0+): ASGI服务器
- **pydantic** (2.5.0+): 数据验证
- **requests** (2.31.0+): HTTP客户端
- **python-multipart** (0.0.6+): 文件上传支持

### 外部依赖
- **FFmpeg**: 音频合并(必需)
- **DeepSeek API**: AI分析(可选)
- **火山引擎TTS**: 语音合成(必需)

## 🚀 快速开始

```powershell
# 1. 进入目录
cd dialogue_editor

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境变量
cp .env.template ../.env
# 编辑 .env 填入凭证

# 4. 启动服务
.\start.ps1
# 或
python app.py

# 5. 访问
http://localhost:8000
```

## 📊 性能考虑

- **并发**: FastAPI异步支持,单个对话生成不阻塞
- **缓存**: 已生成的音频文件可重用
- **流式**: HTTP流式接口减少等待时间
- **优化**: 使用火山引擎推荐的参数(24kHz采样率)

## 🔒 安全性

- API密钥存储在环境变量中
- 工程文件存储在本地目录
- 无用户认证(单机使用)
- 输入验证使用Pydantic

## 🛣️ 未来扩展

- [ ] 用户账户系统
- [ ] 工程分享和协作
- [ ] 音频波形可视化
- [ ] 实时预览单句
- [ ] 导出SRT字幕
- [ ] 支持更多TTS引擎
- [ ] 批量导入CSV
- [ ] 移动端优化

## 📝 开发笔记

### 为什么选择这些技术?

1. **FastAPI**: 快速开发,自动API文档,异步支持
2. **Vanilla JS**: 避免构建复杂度,适合小型项目
3. **Pydantic**: 类型安全,自动验证,易于维护
4. **FFmpeg**: 业界标准,功能强大,跨平台

### 设计决策

- **单页应用**: 减少页面刷新,提升体验
- **JSON工程文件**: 人类可读,便于调试和版本控制
- **异步TTS**: 支持大量对话的批量生成
- **模块化**: 各组件职责清晰,易于测试和扩展

---

**项目状态**: ✅ MVP完成,可投入使用

**作者**: GitHub Copilot
**日期**: 2025年10月17日
