#!/usr/bin/env python3
"""
MP3格式快速测试
简单验证MP3输出功能
"""
from test_mp3_output import MP3TTSClient

def quick_mp3_test():
    """快速MP3测试"""
    client = MP3TTSClient()
    
    print("🎵 MP3格式快速测试")
    print("=" * 30)
    
    text = "你好，这是MP3格式的语音合成测试。MP3格式文件更小，更适合网络传输。"
    
    try:
        # 测试标准质量MP3
        print("🔄 正在生成MP3文件...")
        success = client.synthesize_mp3(
            text=text,
            output_file="quick_test.mp3",
            sample_rate=24000,
            bit_rate=128000
        )
        
        if success:
            print("✅ MP3文件生成成功!")
            print("📁 文件: quick_test.mp3")
            print("🎵 请用音频播放器播放检查效果")
        else:
            print("❌ MP3生成失败")
    
    finally:
        client.close()

if __name__ == "__main__":
    quick_mp3_test()