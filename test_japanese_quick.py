#!/usr/bin/env python3
"""
日文TTS快速测试示例
包含常用的日文短语和句子
"""
from tts_japanese import JapaneseTTSClient

def quick_japanese_test():
    """快速日文测试"""
    client = JapaneseTTSClient()
    
    # 精选日文测试文本
    test_text = "おはようございます。今日はとても良い天気ですね。火山エンジンの日本語音声合成サービスをお試しいただき、ありがとうございます。"
    
    print("🗾 日文TTS快速测试")
    print("=" * 40)
    print(f"📝 测试文本: {test_text}")
    print("🔄 正在合成...")
    
    try:
        success = client.synthesize_japanese(
            text=test_text,
            output_file="japanese_quick_test.wav",
            speech_rate=0  # 正常语速
        )
        
        if success:
            print("✅ 日文合成成功!")
            print("📁 输出文件: japanese_quick_test.wav")
            print("🎵 请播放文件检查日文发音效果")
        else:
            print("❌ 日文合成失败")
            
    finally:
        client.close()

if __name__ == "__main__":
    quick_japanese_test()