#!/usr/bin/env python3
"""
火山引擎TTS V3 HTTP接口使用示例
简单的调用示例和配置说明
"""
from tts_http_v3 import TTSHttpClient
import os

#https://www.volcengine.com/docs/6561/1598757

def example_basic_usage():
    """基础使用示例"""
    client = TTSHttpClient()
    
    try:
        # 基础合成
        success = client.synthesize_speech(
            text="你好，这是一个简单的测试",
            output_file="example_basic.wav"
        )
        
        if success:
            print("✅ 基础合成成功")
        
        # 带参数的合成
        success = client.synthesize_speech(
            text="这是一个快速语音测试",
            output_file="example_fast.wav",
            speech_rate=50,  # 加快语速
            loudness_rate=20,  # 增加音量
            audio_format="mp3"  # MP3格式
        )
        
        if success:
            print("✅ 快速语音合成成功")
        
        # TTS2.0 上下文合成（需要使用seed-tts-2.0资源）
        if client.resource_id == "seed-tts-2.0":
            success = client.synthesize_speech(
                text="今天天气真不错",
                output_file="example_context.wav",
                context_texts=["你可以用开心的语气说话吗？"]
            )
            
            if success:
                print("✅ 上下文合成成功")
    
    finally:
        client.close()


def example_mix_usage():
    """混音使用示例"""
    client = TTSHttpClient()
    
    try:
        # 混音合成
        mix_speakers = [
            {"source_speaker": "zh_male_bvlazysheep", "mix_factor": 0.4},
            {"source_speaker": "zh_female_shuangkuaisisi_moon_bigtts", "mix_factor": 0.6}
        ]
        
        success = client.synthesize_with_mix(
            text="这是混音效果测试",
            output_file="example_mix.wav",
            mix_speakers=mix_speakers
        )
        
        if success:
            print("✅ 混音合成成功")
    
    finally:
        client.close()


def example_batch_usage():
    """批量合成示例"""
    client = TTSHttpClient()
    
    try:
        texts = [
            "第一段文本",
            "第二段文本", 
            "第三段文本"
        ]
        
        for i, text in enumerate(texts, 1):
            success = client.synthesize_speech(
                text=text,
                output_file=f"batch_{i}.wav",
                speech_rate=0,
                use_cache=True  # 启用缓存
            )
            
            if success:
                print(f"✅ 批量合成 {i} 成功")
    
    finally:
        client.close()


if __name__ == "__main__":
    print("🎵 火山引擎TTS V3 HTTP接口使用示例")
    print("=" * 50)
    
    # 检查环境变量配置
    if not os.getenv("VOLCENGINE_APP_ID") or not os.getenv("VOLCENGINE_ACCESS_TOKEN"):
        print("❌ 请先配置环境变量:")
        print("   VOLCENGINE_APP_ID=你的APP_ID")
        print("   VOLCENGINE_ACCESS_TOKEN=你的访问令牌")
        print("   TTS_V3_RESOURCE_ID=seed-tts-2.0  # 可选，默认seed-tts-2.0")
        print("   VOLCENGINE_VOICE_TYPE=你的音色  # 可选")
        exit(1)
    
    print("运行基础示例...")
    example_basic_usage()
    
    print("\n运行混音示例...")  
    example_mix_usage()
    
    print("\n运行批量示例...")
    example_batch_usage()
    
    print("\n✅ 所有示例运行完成！")