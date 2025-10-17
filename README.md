# 火山引擎TTS测试指南

## 🚀 快速开始

### 1. 环境准备
这个项目使用 `uv` 进行依赖管理，已经自动安装了所需依赖：
- ✅ websockets
- ✅ volc-speech-python-sdk (本地版本)

### 2. 配置API凭证
#### 方法一：使用环境变量文件 (推荐)
1. 复制环境变量模板：
   ```bash
   cp .env.example .env
   ```
2. 编辑 `.env` 文件，填入你从火山引擎获取的：
   - `VOLCENGINE_APP_ID`: 应用ID  
   - `VOLCENGINE_ACCESS_TOKEN`: 访问令牌

#### 方法二：交互式输入
程序运行时会提示你输入凭证信息。

### 3. 测试方式

#### 方式一：交互式测试 (推荐新手)
```bash
uv run python test_tts.py
```
程序会引导你输入必要的信息。

#### 方式二：配置文件测试 (推荐批量测试)
1. 编辑 `simple_test.py` 文件
2. 将 `CONFIG` 中的 `YOUR_APP_ID` 和 `YOUR_ACCESS_TOKEN` 替换为真实值
3. 运行:
```bash
uv run python simple_test.py
```

#### 方式三：直接调用 (适合集成)
```python
import asyncio
from test_tts import test_tts

async def my_test():
    success = await test_tts(
        appid="你的APP_ID",
        access_token="你的ACCESS_TOKEN", 
        text="要转换的文本",
        voice_type="zh_female_shuangkuaisisi_moon_bigtts",
        output_file="output.wav"
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