#!/usr/bin/env python3
"""
火山引擎TTS V3 MP3格式输出测试
测试不同采样率和比特率的MP3输出效果
"""
from tts_http_v3 import TTSHttpClient
import os
from pathlib import Path

# 默认配置
DEFAULT_SPEAKER = os.getenv("VOLCENGINE_VOICE_TYPE", "zh_female_vv_uranus_bigtts")

# 测试文本
TEST_TEXTS = {
    "short": "你好，这是MP3格式测试。",
    "medium": "欢迎使用火山引擎语音合成服务，这是一段中等长度的测试文本，用于验证MP3音频格式的输出效果。",
    "long": "人工智能技术正在快速发展，语音合成作为其中的重要分支，已经广泛应用于各种场景。火山引擎提供的TTS服务支持多种音频格式输出，包括MP3、WAV、PCM等。MP3格式具有文件小、兼容性好的特点，非常适合在网络传输和存储场景中使用。今天我们来测试一下不同参数设置下的MP3输出效果。"
}

# MP3测试配置
MP3_CONFIGS = [
    {"sample_rate": 16000, "bit_rate": 64000, "desc": "低质量 (16kHz, 64kbps)"},
    {"sample_rate": 22050, "bit_rate": 96000, "desc": "中等质量 (22kHz, 96kbps)"},
    {"sample_rate": 24000, "bit_rate": 128000, "desc": "高质量 (24kHz, 128kbps)"},
    {"sample_rate": 44100, "bit_rate": 160000, "desc": "CD质量 (44kHz, 160kbps)"},
    {"sample_rate": 48000, "bit_rate": 320000, "desc": "超高质量 (48kHz, 320kbps)"}
]


class MP3TTSClient(TTSHttpClient):
    """MP3专用TTS客户端"""
    
    def synthesize_mp3(
        self,
        text: str,
        output_file: str,
        speaker: str = DEFAULT_SPEAKER,
        sample_rate: int = 24000,
        bit_rate: int = 128000,
        speech_rate: int = 0,
        loudness_rate: int = 0,
        emotion: str = None,
        **kwargs
    ) -> bool:
        """
        合成MP3格式语音
        
        Args:
            text: 要合成的文本
            output_file: 输出文件路径（自动添加.mp3后缀）
            speaker: 音色
            sample_rate: 采样率
            bit_rate: 比特率
            speech_rate: 语速
            loudness_rate: 音量
            emotion: 情感
            **kwargs: 其他参数
        
        Returns:
            bool: 是否成功
        """
        # 确保文件名有.mp3后缀
        if not output_file.endswith('.mp3'):
            output_file += '.mp3'
        
        print(f"🎵 开始MP3合成")
        print(f"   文本: {text[:50]}...")
        print(f"   音色: {speaker}")
        print(f"   采样率: {sample_rate}Hz")
        print(f"   比特率: {bit_rate}bps")
        
        return self.synthesize_speech(
            text=text,
            output_file=output_file,
            speaker=speaker,
            audio_format="mp3",
            sample_rate=sample_rate,
            speech_rate=speech_rate,
            loudness_rate=loudness_rate,
            emotion=emotion,
            bit_rate=bit_rate,  # MP3专用参数
            **kwargs
        )


def test_mp3_basic():
    """基础MP3输出测试"""
    client = MP3TTSClient()
    
    try:
        print("🎵 基础MP3输出测试")
        print("=" * 40)
        
        text = TEST_TEXTS["medium"]
        output_file = "mp3_basic_test.mp3"
        
        success = client.synthesize_mp3(
            text=text,
            output_file=output_file,
            sample_rate=24000,
            bit_rate=128000
        )
        
        if success:
            # 检查文件大小
            file_path = Path(output_file)
            if file_path.exists():
                file_size = file_path.stat().st_size
                print(f"✅ MP3文件生成成功")
                print(f"📁 文件: {output_file}")
                print(f"📊 大小: {file_size:,} 字节 ({file_size/1024:.1f} KB)")
            else:
                print("❌ 文件未找到")
        else:
            print("❌ MP3合成失败")
    
    finally:
        client.close()


def test_mp3_quality_comparison():
    """MP3不同质量对比测试"""
    client = MP3TTSClient()
    
    try:
        print("🎵 MP3质量对比测试")
        print("=" * 40)
        
        text = TEST_TEXTS["medium"]
        speaker = input(f"音色 (回车默认 {DEFAULT_SPEAKER}): ").strip() or DEFAULT_SPEAKER
        
        results = []
        
        for i, config in enumerate(MP3_CONFIGS, 1):
            print(f"\n📝 测试 {i}/{len(MP3_CONFIGS)}: {config['desc']}")
            
            output_file = f"mp3_quality_{i}_{config['sample_rate']}Hz_{config['bit_rate']//1000}k.mp3"
            
            success = client.synthesize_mp3(
                text=text,
                output_file=output_file,
                speaker=speaker,
                sample_rate=config['sample_rate'],
                bit_rate=config['bit_rate']
            )
            
            if success:
                # 检查文件大小
                file_path = Path(output_file)
                if file_path.exists():
                    file_size = file_path.stat().st_size
                    results.append({
                        "config": config['desc'],
                        "file": output_file,
                        "size": file_size
                    })
                    print(f"✅ 成功: {file_size/1024:.1f} KB")
                else:
                    print("❌ 文件未生成")
            else:
                print("❌ 合成失败")
        
        # 显示对比结果
        if results:
            print(f"\n📊 MP3质量对比结果:")
            print("-" * 60)
            for result in results:
                print(f"{result['config']:<25} | {result['size']/1024:>8.1f} KB | {result['file']}")
    
    finally:
        client.close()


def test_mp3_different_texts():
    """不同长度文本的MP3测试"""
    client = MP3TTSClient()
    
    try:
        print("🎵 不同长度文本MP3测试")
        print("=" * 40)
        
        speaker = input(f"音色 (回车默认 {DEFAULT_SPEAKER}): ").strip() or DEFAULT_SPEAKER
        
        for text_type, text in TEST_TEXTS.items():
            print(f"\n📝 测试文本类型: {text_type}")
            print(f"   长度: {len(text)} 字符")
            print(f"   内容: {text[:50]}...")
            
            output_file = f"mp3_text_{text_type}.mp3"
            
            success = client.synthesize_mp3(
                text=text,
                output_file=output_file,
                speaker=speaker,
                sample_rate=24000,
                bit_rate=128000
            )
            
            if success:
                file_path = Path(output_file)
                if file_path.exists():
                    file_size = file_path.stat().st_size
                    duration_estimate = len(text) * 0.1  # 粗略估算时长（秒）
                    print(f"✅ 成功: {file_size/1024:.1f} KB (预估时长: {duration_estimate:.1f}秒)")
                else:
                    print("❌ 文件未生成")
            else:
                print("❌ 合成失败")
    
    finally:
        client.close()


def test_mp3_with_emotions():
    """带情感的MP3测试"""
    client = MP3TTSClient()
    
    emotions_to_test = ["neutral", "happy", "sad", "angry", "excited"]
    text = "今天是个美好的日子，让我们一起感受不同的情感表达。"
    
    try:
        print("🎭 带情感的MP3测试")
        print("=" * 40)
        
        speaker = input(f"音色 (回车默认 {DEFAULT_SPEAKER}): ").strip() or DEFAULT_SPEAKER
        
        for emotion in emotions_to_test:
            print(f"\n😊 测试情感: {emotion}")
            
            output_file = f"mp3_emotion_{emotion}.mp3"
            
            success = client.synthesize_mp3(
                text=text,
                output_file=output_file,
                speaker=speaker,
                emotion=emotion,
                sample_rate=24000,
                bit_rate=128000
            )
            
            if success:
                print(f"✅ 成功: {output_file}")
            else:
                print(f"❌ 失败: {emotion}")
    
    finally:
        client.close()


def test_mp3_interactive():
    """交互式MP3测试"""
    client = MP3TTSClient()
    
    try:
        print("🎵 交互式MP3测试")
        print("=" * 40)
        
        while True:
            text = input("\n请输入要合成的文本 (输入'quit'退出): ").strip()
            
            if text.lower() == 'quit':
                break
            
            if not text:
                text = TEST_TEXTS["medium"]
                print(f"使用默认文本: {text[:50]}...")
            
            # 配置选择
            speaker = input(f"音色 (回车默认 {DEFAULT_SPEAKER}): ").strip() or DEFAULT_SPEAKER
            
            # 质量选择
            print("\n质量选项:")
            for i, config in enumerate(MP3_CONFIGS, 1):
                print(f"{i}. {config['desc']}")
            
            quality_choice = input("选择质量 (回车默认3): ").strip()
            try:
                config = MP3_CONFIGS[int(quality_choice) - 1] if quality_choice else MP3_CONFIGS[2]
            except (ValueError, IndexError):
                config = MP3_CONFIGS[2]  # 默认高质量
            
            # 情感选择
            emotion = input("情感 (回车跳过): ").strip() or None
            
            # 生成文件名
            output_file = f"interactive_mp3_{config['sample_rate']}Hz.mp3"
            
            print(f"\n🚀 开始合成MP3...")
            
            success = client.synthesize_mp3(
                text=text,
                output_file=output_file,
                speaker=speaker,
                sample_rate=config['sample_rate'],
                bit_rate=config['bit_rate'],
                emotion=emotion
            )
            
            if success:
                file_path = Path(output_file)
                if file_path.exists():
                    file_size = file_path.stat().st_size
                    print(f"✅ 合成成功!")
                    print(f"📁 文件: {output_file}")
                    print(f"📊 大小: {file_size/1024:.1f} KB")
                else:
                    print("❌ 文件未找到")
            else:
                print("❌ 合成失败")
        
        print("\n👋 交互式测试结束")
    
    finally:
        client.close()


def main():
    """主函数"""
    print("🎵 火山引擎TTS V3 MP3格式测试程序")
    print("=" * 60)
    
    # 检查环境配置
    if not os.getenv("VOLCENGINE_APP_ID") or not os.getenv("VOLCENGINE_ACCESS_TOKEN"):
        print("❌ 请先配置环境变量:")
        print("   VOLCENGINE_APP_ID=你的APP_ID")
        print("   VOLCENGINE_ACCESS_TOKEN=你的访问令牌")
        return
    
    try:
        print("📋 MP3格式特点:")
        print("   ✅ 文件体积小，适合网络传输")
        print("   ✅ 兼容性好，支持所有播放器")
        print("   ✅ 可调节比特率控制质量和大小")
        print("   ⚠️  有损压缩，质量略低于WAV")
        
        print("\n选择测试模式:")
        print("1. 基础MP3测试")
        print("2. 质量对比测试")
        print("3. 不同长度文本测试")
        print("4. 带情感MP3测试")
        print("5. 交互式MP3测试")
        
        choice = input("请选择 (1-5): ").strip()
        
        if choice == "1":
            test_mp3_basic()
        elif choice == "2":
            test_mp3_quality_comparison()
        elif choice == "3":
            test_mp3_different_texts()
        elif choice == "4":
            test_mp3_with_emotions()
        elif choice == "5":
            test_mp3_interactive()
        else:
            print("❌ 无效选择")
    
    except ValueError as e:
        print(f"❌ 配置错误: {e}")
    except KeyboardInterrupt:
        print("\n👋 用户取消操作")
    except Exception as e:
        print(f"❌ 程序错误: {e}")


if __name__ == "__main__":
    main()