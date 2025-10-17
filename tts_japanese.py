#!/usr/bin/env python3
"""
火山引擎TTS V3 日文语音合成专用程序
支持日文文本转语音，使用explicit_language参数指定日文语种
"""
from tts_http_v3 import TTSHttpClient
import os
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class JapaneseTTSClient(TTSHttpClient):
    """日文TTS客户端，继承自TTSHttpClient"""
    
    def __init__(self):
        super().__init__()
        # 日文音色需要使用TTS1.0资源ID
        if self.resource_id == "seed-tts-2.0":
            logger.info("🔄 日文音色需要TTS1.0支持，自动切换到seed-tts-1.0资源ID")
            self.resource_id = "seed-tts-1.0"
        elif self.resource_id not in ["seed-tts-1.0", "seed-tts-1.0-concurr"]:
            logger.info("🔄 日文音色需要TTS1.0支持，自动切换到seed-tts-1.0资源ID") 
            self.resource_id = "seed-tts-1.0"
    
    def synthesize_japanese(
        self,
        text: str,
        output_file: str,
        speaker: str = "multi_female_sophie_conversation_wvae_bigtts",  # 实际可用的日文音色 - さとみ（智美）
        audio_format: str = "wav",
        sample_rate: int = 24000,
        speech_rate: int = 0,
        loudness_rate: int = 0,
        **kwargs
    ) -> bool:
        """
        合成日文语音
        
        Args:
            text: 日文文本
            output_file: 输出文件路径
            speaker: 日文音色
            audio_format: 音频格式
            sample_rate: 采样率
            speech_rate: 语速 (-50到100)
            loudness_rate: 音量 (-50到100)
            **kwargs: 其他参数
        
        Returns:
            bool: 是否成功
        """
        logger.info(f"🗾 开始日文语音合成: {text[:30]}...")
        logger.info(f"🎤 使用音色: {speaker}")
        
        # 设置日文语种参数
        kwargs["explicit_language"] = "ja"  # 仅日文
        
        return self.synthesize_speech(
            text=text,
            output_file=output_file,
            speaker=speaker,
            audio_format=audio_format,
            sample_rate=sample_rate,
            speech_rate=speech_rate,
            loudness_rate=loudness_rate,
            **kwargs
        )


def test_japanese_basic():
    """基础日文合成测试"""
    client = JapaneseTTSClient()
    
    # 日文测试文本
    japanese_texts = [
        "こんにちは、世界！",
        "今日はいい天気ですね。",
        "火山エンジンの音声合成サービスへようこそ。",
        "人工知能技術が世界を変えています。",
        "ありがとうございます。"
    ]
    
    try:
        print("🗾 开始日文TTS基础测试...")
        success_count = 0
        
        for i, text in enumerate(japanese_texts, 1):
            print(f"\n📝 合成 {i}/{len(japanese_texts)}: {text}")
            output_file = f"japanese_test_{i}.wav"
            
            success = client.synthesize_japanese(
                text=text,
                output_file=output_file
            )
            
            if success:
                print(f"✅ 成功: {output_file}")
                success_count += 1
            else:
                print(f"❌ 失败: {text}")
        
        print(f"\n📊 日文测试完成! 成功: {success_count}/{len(japanese_texts)}")
        
        if success_count == len(japanese_texts):
            print("🎉 恭喜！日文TTS测试全部通过！")
    
    finally:
        client.close()


def test_japanese_advanced():
    """高级日文合成测试"""
    client = JapaneseTTSClient()
    
    try:
        # 不同类型的日文文本测试
        test_cases = [
            {
                "text": "おはようございます。今日も一日頑張りましょう！",
                "file": "japanese_greeting.wav",
                "description": "问候语"
            },
            {
                "text": "桜の花が美しく咲いています。春がやってきました。",
                "file": "japanese_poetry.wav",  
                "description": "诗意表达"
            },
            {
                "text": "コンピューターとインターネットの技術が急速に発展しています。",
                "file": "japanese_tech.wav",
                "description": "技术相关"
            },
            {
                "text": "明日の会議は午後2時から始まります。よろしくお願いします。",
                "file": "japanese_business.wav",
                "description": "商务用语"
            },
            {
                "text": "美味しいラーメンを食べに行きませんか？",
                "file": "japanese_casual.wav",
                "description": "日常对话"
            }
        ]
        
        print("🗾 开始高级日文TTS测试...")
        success_count = 0
        
        for i, case in enumerate(test_cases, 1):
            print(f"\n📝 测试 {i}/{len(test_cases)} - {case['description']}")
            print(f"   文本: {case['text']}")
            
            success = client.synthesize_japanese(
                text=case['text'],
                output_file=case['file'],
                speech_rate=0,  # 正常语速
                audio_format="wav"
            )
            
            if success:
                print(f"✅ 成功生成: {case['file']}")
                success_count += 1
            else:
                print(f"❌ 失败")
        
        print(f"\n📊 高级测试完成! 成功: {success_count}/{len(test_cases)}")
    
    finally:
        client.close()


def test_japanese_different_voices():
    """不同日文音色测试"""
    client = JapaneseTTSClient()
    
    # 实际可用的日文音色列表
    japanese_voices = [
        "multi_zh_male_youyoujunzi_moon_bigtts",     # ひかる（光） - 男声
        "multi_female_sophie_conversation_wvae_bigtts",  # さとみ（智美） - 女声
        "multi_male_xudong_conversation_wvae_bigtts",    # まさお（正男） - 男声
        "multi_female_maomao_conversation_wvae_bigtts",  # つき（月） - 女声
        "multi_female_gaolengyujie_moon_bigtts"         # あけみ（朱美） - 女声
    ]
    
    test_text = "こんにちは。私は火山エンジンの音声合成です。"
    
    # 音色对应的日文名称
    voice_names = [
        "ひかる（光）",
        "さとみ（智美）", 
        "まさお（正男）",
        "つき（月）",
        "あけみ（朱美）"
    ]
    
    try:
        print("🎤 开始不同日文音色测试...")
        
        for i, voice in enumerate(japanese_voices, 1):
            voice_name = voice_names[i-1] if i <= len(voice_names) else "未知"
            print(f"\n🎵 测试音色 {i}: {voice_name}")
            print(f"   ID: {voice}")
            output_file = f"japanese_voice_{i}_{voice_name.replace('（', '_').replace('）', '')}.wav"
            
            success = client.synthesize_japanese(
                text=test_text,
                output_file=output_file,
                speaker=voice
            )
            
            if success:
                print(f"✅ 音色测试成功: {output_file}")
            else:
                print(f"❌ 音色测试失败: {voice}")
                print("💡 提示: 可能是音色权限问题或音色名称错误")
    
    finally:
        client.close()


def test_japanese_interactive():
    """交互式日文合成"""
    client = JapaneseTTSClient()
    
    try:
        print("🗾 日文TTS交互式测试")
        print("=" * 50)
        
        while True:
            text = input("\n请输入日文文本 (输入'quit'退出): ").strip()
            
            if text.lower() == 'quit':
                break
            
            if not text:
                text = "こんにちは、世界！これは日本語のテストです。"
                print(f"使用默认文本: {text}")
            
            # 音色选择
            voice = input("音色 (回车使用默认): ").strip()
            if not voice:
                voice = "multi_female_sophie_conversation_wvae_bigtts"
            
            # 语速
            speed_input = input("语速 (-50到100, 回车默认0): ").strip()
            speech_rate = int(speed_input) if speed_input else 0
            
            # 输出文件
            output_file = input("输出文件名 (回车默认japanese_interactive.wav): ").strip()
            if not output_file:
                output_file = "japanese_interactive.wav"
            
            print(f"\n🚀 开始合成日文: {text}")
            
            success = client.synthesize_japanese(
                text=text,
                output_file=output_file,
                speaker=voice,
                speech_rate=speech_rate
            )
            
            if success:
                print(f"✅ 合成成功! 文件: {output_file}")
            else:
                print("❌ 合成失败")
        
        print("\n👋 交互式测试结束")
    
    finally:
        client.close()


def main():
    """主函数"""
    print("🗾 火山引擎日文TTS专用程序")
    print("=" * 60)
    
    # 检查环境配置
    if not os.getenv("VOLCENGINE_APP_ID") or not os.getenv("VOLCENGINE_ACCESS_TOKEN"):
        print("❌ 请先配置环境变量:")
        print("   VOLCENGINE_APP_ID=你的APP_ID")
        print("   VOLCENGINE_ACCESS_TOKEN=你的访问令牌")
        print("   TTS_V3_RESOURCE_ID=seed-tts-2.0  # 推荐使用2.0以获得更好的日文效果")
        return
    
    try:
        # 显示当前配置
        client = JapaneseTTSClient()
        print("📋 当前配置:")
        print(f"   - 资源ID: {client.resource_id}")
        print(f"   - APP ID: {client.appid[:10]}****")
        
        if client.resource_id == "seed-tts-2.0":
            print("   ✅ 使用TTS2.0，日文效果更佳")
        else:
            print("   ⚠️  建议使用seed-tts-2.0以获得更好的日文效果")
        
        client.close()
        
        print("\n选择测试模式:")
        print("1. 基础日文合成测试")
        print("2. 高级日文合成测试") 
        print("3. 不同音色测试")
        print("4. 交互式日文合成")
        
        choice = input("请选择 (1/2/3/4): ").strip()
        
        if choice == "1":
            test_japanese_basic()
        elif choice == "2":
            test_japanese_advanced()
        elif choice == "3":
            test_japanese_different_voices()
        elif choice == "4":
            test_japanese_interactive()
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