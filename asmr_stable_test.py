#!/usr/bin/env python3
"""
稳定的ASMR测试脚本 - 豆包TTS 2.0
专门针对ASMR效果进行优化，避免参数冲突
"""
from tts_http_v3 import TTSHttpClient
import os
import time

# 推荐使用豆包TTS 2.0音色
DEFAULT_SPEAKER = os.getenv("VOLCENGINE_VOICE_TYPE", "zh_female_vv_uranus_bigtts")

def stable_asmr_test():
    """稳定的ASMR效果测试"""
    client = TTSHttpClient()
    
    # 经过优化的ASMR测试配置 - 避免过于极端的参数
    asmr_tests = [
        {
            "name": "基础ASMR",
            "text": "轻轻地...慢慢地...让我们一起放松下来...",
            "context": None,
            "emotion": "ASMR",
            "emotion_scale": 4,
            "speech_rate": -1,
            "loudness_rate": -1
        },
        {
            "name": "温柔ASMR_简单上下文",
            "text": "闭上眼睛，深深地吸一口气，慢慢地呼出来。",
            "context": ["请用温柔的声音说话"],
            "emotion": "ASMR", 
            "emotion_scale": 4,
            "speech_rate": -1,
            "loudness_rate": -2
        },
        {
            "name": "轻柔ASMR_耳语效果",
            "text": "你今天辛苦了，让我陪伴你一会儿。",
            "context": ["用轻柔的耳语声音"],
            "emotion": "ASMR",
            "emotion_scale": 5, 
            "speech_rate": -2,
            "loudness_rate": -2
        },
        {
            "name": "深度ASMR_放松引导", 
            "text": "让所有的紧张和压力，都随着呼吸慢慢离开你的身体。",
            "context": ["用最放松的ASMR声音", "像催眠一样轻柔"],
            "emotion": "ASMR",
            "emotion_scale": 5,
            "speech_rate": -2,
            "loudness_rate": -3
        },
        {
            "name": "tender情感_对比测试",
            "text": "宝贝，你是如此的特别，如此的珍贵。",
            "context": ["用最温柔的声音说话"],
            "emotion": "tender", 
            "emotion_scale": 4,
            "speech_rate": -1,
            "loudness_rate": -1
        },
        {
            "name": "comfort情感_舒缓效果",
            "text": "别担心，一切都会好起来的，我会陪在你身边。",
            "context": ["用安慰的声音"],
            "emotion": "comfort",
            "emotion_scale": 4,
            "speech_rate": -1,
            "loudness_rate": -1
        }
    ]
    
    try:
        print(f"\n🎧 稳定ASMR测试开始")
        print(f"📋 使用音色: {DEFAULT_SPEAKER}")
        print("=" * 60)
        
        success_count = 0
        
        for i, test_config in enumerate(asmr_tests, 1):
            output_file = f"stable_asmr_{i:02d}_{test_config['name']}.wav"
            
            print(f"\n🎵 测试 {i}/{len(asmr_tests)}: {test_config['name']}")
            print(f"   文本: {test_config['text'][:40]}...")
            print(f"   上下文: {test_config['context']}")
            print(f"   情感: {test_config['emotion']} (强度: {test_config['emotion_scale']})")
            
            success = client.synthesize_speech(
                text=test_config['text'],
                output_file=output_file,
                speaker=DEFAULT_SPEAKER,
                context_texts=test_config['context'],
                emotion=test_config['emotion'],
                emotion_scale=test_config['emotion_scale'],
                speech_rate=test_config['speech_rate'],
                loudness_rate=test_config['loudness_rate']
            )
            
            if success:
                print(f"✅ 成功生成: {output_file}")
                success_count += 1
            else:
                print(f"❌ 生成失败: {test_config['name']}")
            
            # 添加短暂延迟，避免请求过于频繁
            time.sleep(1)
        
        print(f"\n🎉 稳定测试完成!")
        print(f"✅ 成功率: {success_count}/{len(asmr_tests)} ({success_count/len(asmr_tests)*100:.1f}%)")
        
        if success_count > 0:
            print(f"\n💡 ASMR效果对比建议:")
            print(f"1. 基础ASMR vs 温柔ASMR - 对比上下文的影响")
            print(f"2. ASMR情感 vs tender/comfort情感 - 对比不同情感参数")
            print(f"3. 注意语速和音量参数对轻柔度的影响")
        
    except Exception as e:
        print(f"❌ 测试过程出错: {e}")
    finally:
        client.close()


def test_asmr_progressive():
    """渐进式ASMR参数测试 - 从保守到激进"""
    client = TTSHttpClient()
    
    # 测试文本
    base_text = "让我们一起放松下来，感受这份宁静与美好。"
    
    # 渐进式参数配置
    progressive_configs = [
        {
            "name": "保守设置",
            "emotion_scale": 3,
            "speech_rate": 0,
            "loudness_rate": 0
        },
        {
            "name": "轻度ASMR", 
            "emotion_scale": 4,
            "speech_rate": -1,
            "loudness_rate": -1
        },
        {
            "name": "中度ASMR",
            "emotion_scale": 5, 
            "speech_rate": -2,
            "loudness_rate": -2
        },
        {
            "name": "深度ASMR",
            "emotion_scale": 6,
            "speech_rate": -3,
            "loudness_rate": -3
        }
    ]
    
    try:
        print(f"\n🔬 渐进式ASMR参数测试")
        print(f"📝 测试文本: {base_text}")
        print("=" * 50)
        
        for i, config in enumerate(progressive_configs, 1):
            output_file = f"progressive_asmr_{i:02d}_{config['name']}.wav"
            
            print(f"\n🎵 测试 {i}/4: {config['name']}")
            print(f"   参数: emotion_scale={config['emotion_scale']}, "
                  f"speech_rate={config['speech_rate']}, "
                  f"loudness_rate={config['loudness_rate']}")
            
            success = client.synthesize_speech(
                text=base_text,
                output_file=output_file,
                speaker=DEFAULT_SPEAKER,
                context_texts=["用ASMR的声音说话"],
                emotion="ASMR",
                **config
            )
            
            if success:
                print(f"✅ 成功: {output_file}")
            else:
                print(f"❌ 失败: {config['name']}")
                
            time.sleep(1)
            
    except Exception as e:
        print(f"❌ 渐进式测试出错: {e}")
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
    
    print("🎧 豆包TTS 2.0 稳定ASMR测试")
    print("=" * 40)
    
    choice = input("选择测试类型:\n1. 稳定ASMR测试\n2. 渐进式参数测试\n3. 两个都测试\n请选择 (1-3): ").strip()
    
    if choice == "1":
        stable_asmr_test()
    elif choice == "2": 
        test_asmr_progressive()
    elif choice == "3":
        stable_asmr_test()
        print("\n" + "="*60)
        test_asmr_progressive()
    else:
        print("❌ 无效选择，运行稳定测试")
        stable_asmr_test()