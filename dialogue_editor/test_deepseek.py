"""
快速测试 - 验证DeepSeek API配置
"""
import os
import sys
from pathlib import Path

# 添加父目录到路径
sys.path.append(str(Path(__file__).parent.parent))

# 加载.env文件
from dotenv import load_dotenv
load_dotenv()

print("=" * 60)
print("DeepSeek API 配置测试")
print("=" * 60)
print()

# 检查环境变量
api_key = os.getenv("OPENAI_API_KEY")
api_base = os.getenv("OPENAI_BASE_URL")
model = os.getenv("OPENAI_MODEL")

print("📋 环境变量检查:")
print(f"  OPENAI_API_KEY: {'✓ 已设置' if api_key else '✗ 未设置'}")
print(f"  OPENAI_BASE_URL: {api_base or '✗ 未设置'}")
print(f"  OPENAI_MODEL: {model or '✗ 未设置'}")
print()

if not api_key:
    print("❌ 错误: OPENAI_API_KEY 未设置")
    sys.exit(1)

# 测试AI分析器
print("🧪 测试AI对话分析...")
print()

try:
    from ai_analyzer import DialogueAnalyzer
    
    analyzer = DialogueAnalyzer()
    
    test_text = """
    你好,最近怎么样?
    挺好的,就是工作有点累。
    那要注意休息啊!
    """
    
    print(f"测试文本:")
    print(test_text)
    print()
    print("正在分析...")
    
    result = analyzer.analyze_dialogue(test_text)
    
    import json
    print()
    print("✅ 分析成功!")
    print()
    print("分析结果:")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print()
    print("=" * 60)
    print("✅ DeepSeek API 配置正确,可以正常使用!")
    print("=" * 60)
    
except Exception as e:
    print()
    print("❌ 分析失败!")
    print(f"错误信息: {e}")
    print()
    import traceback
    traceback.print_exc()
    print()
    print("=" * 60)
    print("请检查:")
    print("1. OPENAI_API_KEY 是否正确")
    print("2. 网络连接是否正常")
    print("3. DeepSeek API 余额是否充足")
    print("=" * 60)
    sys.exit(1)
