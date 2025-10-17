"""
测试脚本 - 验证基本功能
"""
import asyncio
import json
from project_schema import DialogueProject, Speaker, DialogueLine


def test_project_schema():
    """测试数据模型"""
    print("🧪 测试数据模型...")
    
    # 创建测试工程
    project = DialogueProject(
        title="测试对话",
        original_text="你好\n很高兴见到你",
        speakers=[
            Speaker(
                id="speaker_1",
                name="小明",
                gender="male",
                age_group="adult",
                voice_type="zh_male_wennuanahu_moon_bigtts"
            ),
            Speaker(
                id="speaker_2",
                name="小红",
                gender="female",
                age_group="adult",
                voice_type="zh_female_shuangkuaisisi_moon_bigtts"
            )
        ],
        dialogues=[
            DialogueLine(
                id="line_1",
                speaker_id="speaker_1",
                text="你好",
                emotion="开心"
            ),
            DialogueLine(
                id="line_2",
                speaker_id="speaker_2",
                text="很高兴见到你",
                emotion="温柔",
                context="你好"
            )
        ]
    )
    
    # 序列化
    json_str = json.dumps(project.model_dump(), ensure_ascii=False, indent=2)
    print(json_str)
    
    print("✅ 数据模型测试通过\n")


def test_ai_analyzer():
    """测试AI分析器"""
    print("🧪 测试AI分析器...")
    
    from ai_analyzer import DialogueAnalyzer
    
    analyzer = DialogueAnalyzer()
    
    test_text = """
    你好,最近怎么样?
    挺好的,就是工作有点累。
    那要注意休息啊!别太拼命了。
    """
    
    # 测试默认分析(不需要API)
    result = analyzer._get_default_structure(test_text)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    print("✅ AI分析器测试通过\n")


async def test_tts_generator():
    """测试TTS生成器"""
    print("🧪 测试TTS生成器...")
    
    import os
    
    # 检查环境变量
    if not os.getenv("VOLCENGINE_APP_ID") or not os.getenv("VOLCENGINE_ACCESS_TOKEN"):
        print("⚠️  跳过: 未配置TTS凭证")
        return
    
    from tts_generator import TTSGenerator
    
    generator = TTSGenerator()
    
    # 创建简单测试
    line = DialogueLine(
        id="test_1",
        speaker_id="speaker_1",
        text="这是一个测试",
        emotion="中性"
    )
    
    audio_file = await generator.generate_line(
        line,
        voice_type="zh_male_wennuanahu_moon_bigtts",
        line_index=0
    )
    
    if audio_file:
        print(f"✅ 音频生成成功: {audio_file}\n")
    else:
        print("❌ 音频生成失败\n")


def main():
    """运行所有测试"""
    print("=" * 50)
    print("对话TTS编辑器 - 功能测试")
    print("=" * 50)
    print()
    
    try:
        # 测试数据模型
        test_project_schema()
        
        # 测试AI分析
        test_ai_analyzer()
        
        # 测试TTS生成(异步)
        # asyncio.run(test_tts_generator())
        print("⚠️  TTS生成测试已跳过(需要配置凭证)")
        
        print("=" * 50)
        print("✅ 所有基础测试通过!")
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
