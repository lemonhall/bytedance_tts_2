#!/usr/bin/env python3
"""
TTS 2.0上下文功能快速测试
简单演示上下文对语音合成的影响
"""
from tts_http_v3 import TTSHttpClient

def quick_context_test():
    """快速上下文测试"""
    client = TTSHttpClient()
    
    try:
        print("🎭 TTS 2.0上下文功能快速测试")
        print("=" * 40)
        
        # 确保使用TTS 2.0
        if client.resource_id != "seed-tts-2.0":
            print(f"⚠️ 当前资源ID: {client.resource_id}")
            print("💡 建议设置 TTS_V3_RESOURCE_ID=seed-tts-2.0 以获得最佳效果")
        
        # 测试相同文本在不同上下文下的效果
        base_text = "今天是个美好的日子，我感到很开心。"
        
        test_cases = [
            {
                "name": "无上下文",
                "context": None,
                "file": "context_none.wav"
            },
            {
                "name": "慢速语音",
                "context": ["你可以说慢一点吗？"],
                "file": "context_slow.wav"
            },
            {
                "name": "开心语气",
                "context": ["你可以用特别开心的语气说话吗？"],
                "file": "context_happy.wav"
            },
            {
                "name": "温柔语气",
                "context": ["请用温柔一点的语气说话"],
                "file": "context_gentle.wav"
            }
        ]
        
        print(f"📝 测试文本: {base_text}")
        print("🔄 正在生成不同上下文的音频...")
        
        success_count = 0
        
        for i, case in enumerate(test_cases, 1):
            print(f"\n{i}. 生成 {case['name']} 版本...")
            
            success = client.synthesize_speech(
                text=base_text,
                output_file=case['file'],
                context_texts=case['context'],
                audio_format="wav"
            )
            
            if success:
                print(f"   ✅ 成功: {case['file']}")
                success_count += 1
            else:
                print(f"   ❌ 失败")
        
        print(f"\n📊 测试完成! 成功生成 {success_count}/{len(test_cases)} 个文件")
        print("🎵 请播放音频文件，对比不同上下文的效果差异：")
        
        for case in test_cases:
            print(f"   - {case['file']}: {case['name']}")
        
    finally:
        client.close()

if __name__ == "__main__":
    quick_context_test()