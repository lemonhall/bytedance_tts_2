# 对话TTS编辑器

一个基于Web的对话TTS编辑器,用于快速创建多人对话的语音合成工程。

## ✨ 特性

- 🤖 **AI智能分析**: 使用DeepSeek自动识别说话人和情感
- 🎛️ **可视化编辑**: 直观的Web界面,实时调整TTS参数
- 🎵 **批量生成**: 一键生成整个对话的音频
- 💾 **工程管理**: 保存和加载工程文件
- 🎨 **美观界面**: 现代化、简洁的UI设计

## 📦 安装

### 1. 安装Python依赖

```bash
# 进入目录
cd dialogue_editor

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置环境变量

复制配置模板并填入真实信息:

```bash
cp .env.template ../.env
```

编辑 `.env` 文件:

```env
# 火山引擎TTS凭证 (必需)
VOLCENGINE_APP_ID=your_app_id
VOLCENGINE_ACCESS_TOKEN=your_token
TTS_V3_RESOURCE_ID=seed-tts-2.0

# DeepSeek API (可选,用于AI分析)
DEEPSEEK_API_KEY=your_deepseek_key
```

### 3. 安装FFmpeg (用于音频合并)

**Windows:**
- 下载: https://ffmpeg.org/download.html
- 添加到系统PATH

**Mac:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt-get install ffmpeg
```

## 🚀 启动

```bash
cd dialogue_editor
python app.py
```

访问: http://localhost:8000

## 📖 使用流程

### 1. 输入对话文本

在文本框中输入2-3人的对话,每句话一行:

```
你好,最近怎么样?
挺好的,就是工作有点累。
那要注意休息啊!
```

### 2. AI分析

点击 **"AI分析对话"** 按钮:
- 自动识别说话人
- 推理性别和年龄
- 分配合适的音色
- 推测情感参数

### 3. 编辑参数

在编辑页面可以调整:
- 📝 修改对话文本
- 🎭 调整情感标签
- ⚡ 调节语速、音量、音调
- 🔄 重新生成单句音频

### 4. 生成音频

点击 **"生成全部音频"**:
- 逐句生成TTS音频
- 自动合并为完整对话
- 支持下载

## 🏗️ 技术架构

### 后端
- **FastAPI**: 轻量级Web框架
- **Pydantic**: 数据验证
- **火山引擎TTS**: 语音合成
- **DeepSeek API**: 对话分析

### 前端
- **Vanilla JavaScript**: 无依赖
- **现代CSS**: 响应式设计
- **单页应用**: 流畅体验

### 数据格式

工程文件采用JSON格式:

```json
{
  "title": "对话工程",
  "original_text": "原始对话文本",
  "speakers": [
    {
      "id": "speaker_1",
      "name": "说话人A",
      "gender": "male",
      "age_group": "adult",
      "voice_type": "zh_male_wennuanahu_moon_bigtts"
    }
  ],
  "dialogues": [
    {
      "id": "line_1",
      "speaker_id": "speaker_1",
      "text": "对话内容",
      "emotion": "开心",
      "speed_ratio": 1.0,
      "volume_ratio": 1.0,
      "pitch_ratio": 1.0,
      "context": "上一句对话"
    }
  ]
}
```

## 📁 项目结构

```
dialogue_editor/
├── app.py                 # FastAPI后端服务
├── project_schema.py      # 数据模型定义
├── ai_analyzer.py         # AI对话分析
├── tts_generator.py       # TTS音频生成
├── requirements.txt       # Python依赖
├── .env.template         # 环境变量模板
├── static/               # 前端静态文件
│   ├── index.html
│   ├── style.css
│   └── app.js
├── projects/             # 工程文件存储
└── dialogue_output/      # 音频输出目录
```

## 🎯 支持的TTS参数

### 情感 (24种中文)
开心、悲伤、生气、惊讶、恐惧、厌恶、激动、冷漠、中性、沮丧、撒娇、害羞、安慰、紧张、温柔、讲故事、电台、磁性、广告、气泡音、ASMR、新闻、娱乐、方言

### 音色
- 男性成年: `zh_male_wennuanahu_moon_bigtts`
- 女性成年: `zh_female_shuangkuaisisi_moon_bigtts`
- 男童: `zh_male_yangguang_moon_bigtts`
- 女童: `zh_female_tianmei_moon_bigtts`

### 参数范围
- 语速: 0.2 - 3.0
- 音量: 0.1 - 3.0
- 音调: 0.1 - 3.0

## 🔧 API接口

### 分析对话
```http
POST /api/analyze
Content-Type: application/json

{
  "text": "对话文本"
}
```

### 更新对话参数
```http
PUT /api/projects/{project_id}/line/{line_id}
Content-Type: application/json

{
  "emotion": "开心",
  "speed_ratio": 1.2
}
```

### 生成音频
```http
POST /api/projects/{project_id}/generate
```

### 生成单句
```http
POST /api/projects/{project_id}/generate-line/{line_id}
```

## 💡 最佳实践

1. **对话文本**: 每句话简短清晰,避免过长
2. **情感选择**: 根据对话内容选择合适的情感标签
3. **上下文**: 系统会自动设置上下文,有助于更自然的语气
4. **参数调节**: 从默认值开始,微调后重新生成
5. **保存工程**: 及时保存,避免丢失编辑内容

## ⚠️ 注意事项

- 确保已配置火山引擎TTS凭证
- DeepSeek API为可选,未配置时使用默认分析
- 音频生成需要时间,请耐心等待
- FFmpeg必须安装才能合并音频

## 🐛 故障排除

### 服务无法启动
- 检查Python版本 (推荐3.9+)
- 确认所有依赖已安装

### AI分析失败
- 检查DeepSeek API密钥
- 查看控制台错误信息

### 音频生成失败
- 验证火山引擎凭证
- 检查网络连接
- 查看控制台日志

### 音频无法合并
- 确认FFmpeg已安装
- 检查PATH环境变量

## 📝 开发计划

- [ ] 支持更多音色
- [ ] 音频波形可视化
- [ ] 导出字幕文件
- [ ] 批量导入对话
- [ ] 预览单句音频
- [ ] 工程分享功能

## 📄 许可证

本项目仅供学习和测试使用。

---

**Enjoy! 🎉**
