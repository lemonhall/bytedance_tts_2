#!/usr/bin/env python3
"""
火山引擎TTS 2.0 情感参数批量测试
测试所有常见情感参数对音色的影响
"""
from tts_http_v3 import TTSHttpClient
import os

# 推荐使用支持多情感的2.0精品音色
DEFAULT_SPEAKER = os.getenv("VOLCENGINE_VOICE_TYPE", "zh_female_vv_uranus_bigtts")

# 中文情感参数及对应的测试文本
CHINESE_EMOTIONS = {
    "happy": "太好了！今天是个美好的日子，我感到非常开心和兴奋！",
    "sad": "今天下雨了，我的心情很低落，感觉有些悲伤。",
    "angry": "这实在太过分了！我真的很生气，无法忍受这种行为！",
    "surprised": "哇！这真是太令人惊讶了，我完全没有想到会是这样！",
    "fear": "天哪，这里好黑好安静，我感到有些害怕和紧张。",
    "hate": "我真的很讨厌这样的情况，让人感到厌恶。",
    "excited": "太棒了！我等这一刻已经很久了，现在终于实现了！",
    "coldness": "哦，是这样吗。我知道了，没什么特别的。",
    "neutral": "今天的天气不错，适合出门散步。",
    "depressed": "唉，最近总是感觉很沮丧，什么都提不起精神。",
    "lovey-dovey": "亲爱的，你真是太可爱了，我好喜欢你呀～",
    "shy": "嗯...那个...我有点不好意思说...你能听我说完吗？",
    "comfort": "别担心，一切都会好起来的，我会陪在你身边的。",
    "tension": "快点！时间不够了！我们必须马上行动！",
    "tender": "宝贝，妈妈爱你，你是妈妈最珍贵的礼物。",
    "storytelling": "很久很久以前，在一个美丽的王国里，住着一位善良的公主。",
    "radio": "欢迎收听今天的节目，我是您的主播，为您带来最新资讯。",
    "magnetic": "夜色如水，月光如诗，让我们一起感受这美妙的时光。",
    "advertising": "限时特惠！超值优惠！机会难得，不容错过！",
    "vocal-fry": "这个声音效果...真的很特别...有种独特的质感...",
    "ASMR": "轻轻地...慢慢地...让我们一起放松下来...",
    "news": "据最新消息报道，今天的重要新闻如下。",
    "entertainment": "哇，这个明星的八卦真是太劲爆了！你们听说了吗？",
    "dialect": "哎呀，这个事儿啊，咱们老家那边也有这样的说法呢。"
}

# 英文情感参数及对应的测试文本
ENGLISH_EMOTIONS = {
    "neutral": "The weather is nice today. It's a good day for a walk.",
    "happy": "I'm so excited! This is absolutely wonderful and amazing!",
    "angry": "This is completely unacceptable! I'm really upset about this!",
    "sad": "I feel so disappointed and heartbroken about what happened.",
    "excited": "Oh my goodness! I can't believe this is really happening!",
    "chat": "Hey there! How's it going? I hope you're having a great day!",
    "ASMR": "Let's take a moment to relax... breathe slowly... and feel calm...",
    "warm": "Welcome home, my dear. I've missed you so much today.",
    "affectionate": "You mean the world to me, and I love you more than words can say.",
    "authoritative": "Listen carefully. This is important information that you need to understand."
}


def test_emotions(speaker=DEFAULT_SPEAKER, lang="zh"):
    client = TTSHttpClient()
    try:
        if lang == "zh":
            emotions = CHINESE_EMOTIONS
        else:
            emotions = ENGLISH_EMOTIONS
        
        print(f"\n🎭 开始{lang.upper()}情感参数批量测试，音色: {speaker}")
        success_count = 0
        
        for i, (emotion, text) in enumerate(emotions.items(), 1):
            output_file = f"emotion_{lang}_{emotion}.wav"
            print(f"\n📝 测试 {i}/{len(emotions)}: {emotion}")
            print(f"   文本: {text[:50]}...")
            
            success = client.synthesize_speech(
                text=text,
                output_file=output_file,
                speaker=speaker,
                emotion=emotion,
                emotion_scale=4  # 设置情感强度
            )
            
            if success:
                print(f"✅ 成功: {output_file}")
                success_count += 1
            else:
                print(f"❌ 失败: {emotion}")
        
        print(f"\n📊 测试完成! 成功: {success_count}/{len(emotions)}")
    finally:
        client.close()


def test_single_emotion():
    """测试单个情感参数"""
    client = TTSHttpClient()
    
    try:
        print("\n🎭 单个情感参数测试")
        print("=" * 40)
        
        # 选择语言
        lang = input("选择语言 (1.中文 2.英文): ").strip()
        emotions = CHINESE_EMOTIONS if lang != "2" else ENGLISH_EMOTIONS
        lang_code = "zh" if lang != "2" else "en"
        
        # 显示可用情感
        print(f"\n可用的情感参数:")
        for i, emotion in enumerate(emotions.keys(), 1):
            print(f"{i:2d}. {emotion}")
        
        # 选择情感
        choice = input("\n请输入情感编号: ").strip()
        try:
            emotion_list = list(emotions.keys())
            emotion = emotion_list[int(choice) - 1]
            text = emotions[emotion]
        except (ValueError, IndexError):
            print("❌ 无效选择")
            return
        
        # 选择音色
        speaker = input(f"音色 (回车默认 {DEFAULT_SPEAKER}): ").strip() or DEFAULT_SPEAKER
        
        # 选择情感强度
        scale_input = input("情感强度 (1-5, 回车默认4): ").strip()
        emotion_scale = int(scale_input) if scale_input else 4
        
        print(f"\n🚀 开始合成情感: {emotion}")
        print(f"📝 文本: {text}")
        print(f"� 音色: {speaker}")
        print(f"💪 强度: {emotion_scale}")
        
        output_file = f"single_emotion_{lang_code}_{emotion}.wav"
        
        success = client.synthesize_speech(
            text=text,
            output_file=output_file,
            speaker=speaker,
            emotion=emotion,
            emotion_scale=emotion_scale
        )
        
        if success:
            print(f"✅ 合成成功: {output_file}")
        else:
            print("❌ 合成失败")
    
    finally:
        client.close()


def main():
    print("�🎭 火山引擎TTS 2.0情感参数测试")
    print("=" * 50)
    
    print("选择测试模式:")
    print("1. 批量测试所有情感")
    print("2. 测试单个情感")
    
    mode = input("请选择 (1/2): ").strip()
    
    if mode == "2":
        test_single_emotion()
    else:
        speaker = input(f"请输入要测试的音色 (回车默认: {DEFAULT_SPEAKER}): ").strip() or DEFAULT_SPEAKER
        print("1. 中文情感测试\n2. 英文情感测试")
        choice = input("请选择 (1/2): ").strip()
        if choice == "2":
            test_emotions(speaker, lang="en")
        else:
            test_emotions(speaker, lang="zh")

if __name__ == "__main__":
    main()
