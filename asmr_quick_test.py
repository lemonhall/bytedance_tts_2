#!/usr/bin/env python3
"""
ASMR快速测试脚本 - 豆包TTS 2.0
快速测试不同ASMR设置的轻柔语音效果
"""
from tts_http_v3 import TTSHttpClient
import os

# 推荐使用豆包TTS 2.0音色
DEFAULT_SPEAKER = os.getenv("VOLCENGINE_VOICE_TYPE", "zh_female_vv_uranus_bigtts")

def quick_asmr_test():
    """快速ASMR效果测试"""
    client = TTSHttpClient()
    
    # 测试文本
    test_text = "轻轻地...慢慢地...让我们一起放松下来...感受这份宁静与美好..."
    
    # 不同的ASMR上下文设置
    asmr_tests = [
        {
            "name": "无上下文_ASMR情感",
            "context": None,
            "emotion": "ASMR",
            "emotion_scale": 5,
            "speech_rate": -2,
            "loudness_rate": -3
        },
        {
            "name": "轻柔耳语",
            "context": ["请用最轻柔的ASMR语气说话", "像耳语一样轻柔"],
            "emotion": "ASMR",
            "emotion_scale": 6,
            "speech_rate": -3,
            "loudness_rate": -4
        },
        {
            "name": "温柔陪伴",
            "context": ["用最温柔的声音", "充满爱意和关怀", "就像在耳边轻语"],
            "emotion": "ASMR",
            "emotion_scale": 5,
            "speech_rate": -2,
            "loudness_rate": -2
        },
        {
            "name": "催眠助眠",
            "context": ["用催眠般的ASMR声音", "非常轻柔，适合睡前", "声音要很轻很慢"],
            "emotion": "ASMR",
            "emotion_scale": 7,
            "speech_rate": -4,
            "loudness_rate": -3
        }
    ]
    
    try:
        print(f"\n🎧 ASMR快速测试开始")
        print(f"📋 测试文本: {test_text}")
        print(f"📋 使用音色: {DEFAULT_SPEAKER}")
        print("=" * 60)
        
        for i, test_config in enumerate(asmr_tests, 1):
            output_file = f"asmr_quick_test_{i:02d}_{test_config['name']}.wav"
            
            print(f"\n🎵 测试 {i}/4: {test_config['name']}")
            print(f"   上下文: {test_config['context']}")
            
            # 提取参数
            context_texts = test_config.pop('context')
            name = test_config.pop('name')
            
            success = client.synthesize_speech(
                text=test_text,
                output_file=output_file,
                speaker=DEFAULT_SPEAKER,
                context_texts=context_texts,
                **test_config
            )
            
            if success:
                print(f"✅ 成功生成: {output_file}")
            else:
                print(f"❌ 生成失败: {name}")
        
        print(f"\n🎉 快速测试完成!")
        print(f"💡 建议使用音频播放器对比不同设置的ASMR效果")
        
    except Exception as e:
        print(f"❌ 测试过程出错: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    # 检查环境配置
    if not os.getenv("VOLCENGINE_APP_ID") or not os.getenv("VOLCENGINE_ACCESS_TOKEN"):
        print("❌ 请先配置火山引擎TTS API密钥!")
        print("请在.env文件中设置:")
        print("VOLCENGINE_APP_ID=你的AppID") 
        print("VOLCENGINE_ACCESS_TOKEN=你的AccessToken")
        exit(1)
    
    quick_asmr_test()