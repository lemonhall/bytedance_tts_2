#!/usr/bin/env python3
"""
火山引擎TTS 2.0 上下文功能测试
测试context_texts参数对语音合成的影响
仅适用于豆包语音合成模型2.0
"""
from tts_http_v3 import TTSHttpClient
import os

# 推荐使用TTS 2.0的音色
DEFAULT_SPEAKER = os.getenv("VOLCENGINE_VOICE_TYPE", "zh_female_vv_uranus_bigtts")

# 上下文测试用例 - 语速调整
SPEED_CONTEXTS = {
    "正常语速": {
        "context": None,
        "text": "这是一段正常语速的测试文本，用来对比语速的变化效果。"
    },
    "慢速语音": {
        "context": ["你可以说慢一点吗？"],
        "text": "这是一段慢速语音的测试文本，应该比正常语速更慢一些。"
    },
    "快速语音": {
        "context": ["你能说快一点吗？"],
        "text": "这是一段快速语音的测试文本，应该比正常语速更快一些。"
    }
}

# 上下文测试用例 - 情绪/语气调整
EMOTION_CONTEXTS = {
    "正常语气": {
        "context": None,
        "text": "今天天气真不错，适合出门散步。"
    },
    "痛心语气": {
        "context": ["你可以用特别特别痛心的语气说话吗？"],
        "text": "今天发生了一件让人很难过的事情。"
    },
    "欢乐语气": {
        "context": ["嗯，你的语气再欢乐一点"],
        "text": "太好了！今天是个值得庆祝的日子！"
    },
    "骄傲语气": {
        "context": ["你能用骄傲的语气来说话吗？"],
        "text": "我们团队取得了非常出色的成绩。"
    },
    "温柔语气": {
        "context": ["请用温柔一点的语气说话"],
        "text": "宝贝，该睡觉了，妈妈给你讲个故事。"
    },
    "严肃语气": {
        "context": ["请用严肃认真的语气说话"],
        "text": "这是一个非常重要的决定，需要慎重考虑。"
    }
}

# 上下文测试用例 - 音量调整
VOLUME_CONTEXTS = {
    "正常音量": {
        "context": None,
        "text": "这是正常音量的语音测试。"
    },
    "小声说话": {
        "context": ["你嗓门再小点。"],
        "text": "这是小声说话的语音测试，声音应该更轻柔。"
    },
    "大声说话": {
        "context": ["请大声一点说话"],
        "text": "这是大声说话的语音测试，声音应该更响亮。"
    }
}

# 上下文测试用例 - 特殊场景
SPECIAL_CONTEXTS = {
    "播音员风格": {
        "context": ["请用播音员的风格说话"],
        "text": "欢迎收听今天的新闻节目，我是您的主播。"
    },
    "讲故事风格": {
        "context": ["请用讲故事的语气"],
        "text": "很久很久以前，在一个美丽的森林里，住着一只善良的小兔子。"
    },
    "客服风格": {
        "context": ["请用客服的专业语气说话"],
        "text": "您好，感谢您的来电，请问有什么可以帮助您的吗？"
    },
    "朗读风格": {
        "context": ["请用朗读课文的语气"],
        "text": "春天来了，大地苏醒，万物复苏，到处充满了生机和活力。"
    }
}


def test_context_category(client, category_name, contexts, speaker):
    """测试特定类别的上下文效果"""
    print(f"\n🎭 开始测试: {category_name}")
    print("=" * 50)
    
    success_count = 0
    
    for i, (name, data) in enumerate(contexts.items(), 1):
        context = data["context"]
        text = data["text"]
        output_file = f"context_{category_name}_{i}_{name}.wav"
        
        print(f"\n📝 测试 {i}/{len(contexts)}: {name}")
        print(f"   上下文: {context}")
        print(f"   文本: {text[:50]}...")
        
        success = client.synthesize_speech(
            text=text,
            output_file=output_file,
            speaker=speaker,
            context_texts=context,
            audio_format="wav"
        )
        
        if success:
            print(f"✅ 成功: {output_file}")
            success_count += 1
        else:
            print(f"❌ 失败: {name}")
    
    print(f"\n📊 {category_name}测试完成! 成功: {success_count}/{len(contexts)}")
    return success_count


def test_all_contexts():
    """测试所有上下文类别"""
    client = TTSHttpClient()
    
    # 确保使用TTS 2.0
    if client.resource_id != "seed-tts-2.0":
        print("⚠️ 警告: 当前资源ID不是seed-tts-2.0，上下文功能可能不可用")
        print(f"当前资源ID: {client.resource_id}")
        choice = input("是否继续测试? (y/n): ").strip().lower()
        if choice != 'y':
            client.close()
            return
    
    try:
        speaker = input(f"请输入音色 (回车默认 {DEFAULT_SPEAKER}): ").strip() or DEFAULT_SPEAKER
        
        print(f"\n🚀 开始TTS 2.0上下文功能全面测试")
        print(f"🎤 使用音色: {speaker}")
        print(f"📋 资源ID: {client.resource_id}")
        
        total_success = 0
        total_tests = 0
        
        # 测试各个类别
        categories = [
            ("语速调整", SPEED_CONTEXTS),
            ("情绪语气", EMOTION_CONTEXTS),
            ("音量调整", VOLUME_CONTEXTS),
            ("特殊场景", SPECIAL_CONTEXTS)
        ]
        
        for category_name, contexts in categories:
            success_count = test_context_category(client, category_name, contexts, speaker)
            total_success += success_count
            total_tests += len(contexts)
        
        print(f"\n🎉 全部测试完成!")
        print(f"📊 总体成功率: {total_success}/{total_tests} ({total_success/total_tests*100:.1f}%)")
        
    finally:
        client.close()


def test_single_context():
    """测试单个上下文效果"""
    client = TTSHttpClient()
    
    # 确保使用TTS 2.0
    if client.resource_id != "seed-tts-2.0":
        print("⚠️ 警告: 当前资源ID不是seed-tts-2.0，上下文功能可能不可用")
        print(f"当前资源ID: {client.resource_id}")
    
    try:
        print("\n🎭 单个上下文测试")
        print("=" * 40)
        
        # 输入自定义上下文
        context_input = input("请输入上下文提示 (如'你可以说慢一点吗？'): ").strip()
        context_texts = [context_input] if context_input else None
        
        # 输入测试文本
        text = input("请输入要合成的文本: ").strip()
        if not text:
            text = "这是一段用于测试上下文效果的语音合成文本。"
        
        # 选择音色
        speaker = input(f"音色 (回车默认 {DEFAULT_SPEAKER}): ").strip() or DEFAULT_SPEAKER
        
        print(f"\n🚀 开始合成")
        print(f"📝 文本: {text}")
        print(f"🎭 上下文: {context_texts}")
        print(f"🎤 音色: {speaker}")
        
        output_file = "custom_context_test.wav"
        
        success = client.synthesize_speech(
            text=text,
            output_file=output_file,
            speaker=speaker,
            context_texts=context_texts,
            audio_format="wav"
        )
        
        if success:
            print(f"✅ 合成成功: {output_file}")
        else:
            print("❌ 合成失败")
    
    finally:
        client.close()


def test_context_comparison():
    """对比测试 - 有无上下文的效果对比"""
    client = TTSHttpClient()
    
    try:
        print("\n🎭 上下文效果对比测试")
        print("=" * 40)
        
        test_cases = [
            {
                "name": "语速对比",
                "text": "这是一段用来测试语速变化的文本内容。",
                "contexts": [None, ["你可以说慢一点吗？"], ["你能说快一点吗？"]],
                "labels": ["正常", "慢速", "快速"]
            },
            {
                "name": "情感对比", 
                "text": "今天发生了一件让人印象深刻的事情。",
                "contexts": [None, ["你可以用开心的语气说话吗？"], ["你可以用悲伤的语气说话吗？"]],
                "labels": ["正常", "开心", "悲伤"]
            }
        ]
        
        speaker = input(f"音色 (回车默认 {DEFAULT_SPEAKER}): ").strip() or DEFAULT_SPEAKER
        
        for case in test_cases:
            print(f"\n🔍 {case['name']}测试:")
            
            for i, (context, label) in enumerate(zip(case['contexts'], case['labels'])):
                output_file = f"compare_{case['name']}_{label}.wav"
                print(f"   📝 生成{label}版本: {output_file}")
                
                success = client.synthesize_speech(
                    text=case['text'],
                    output_file=output_file,
                    speaker=speaker,
                    context_texts=context,
                    audio_format="wav"
                )
                
                if success:
                    print(f"   ✅ 成功")
                else:
                    print(f"   ❌ 失败")
        
        print(f"\n💡 请播放生成的音频文件，对比不同上下文的效果差异")
        
    finally:
        client.close()


def main():
    """主函数"""
    print("🎭 火山引擎TTS 2.0上下文功能测试")
    print("=" * 60)
    
    # 检查环境配置
    if not os.getenv("VOLCENGINE_APP_ID") or not os.getenv("VOLCENGINE_ACCESS_TOKEN"):
        print("❌ 请先配置环境变量:")
        print("   VOLCENGINE_APP_ID=你的APP_ID")
        print("   VOLCENGINE_ACCESS_TOKEN=你的访问令牌")
        print("   TTS_V3_RESOURCE_ID=seed-tts-2.0  # 必须使用2.0以支持上下文功能")
        return
    
    try:
        print("选择测试模式:")
        print("1. 全面测试所有上下文类别")
        print("2. 测试单个自定义上下文")
        print("3. 效果对比测试")
        
        choice = input("请选择 (1/2/3): ").strip()
        
        if choice == "1":
            test_all_contexts()
        elif choice == "2":
            test_single_context()
        elif choice == "3":
            test_context_comparison()
        else:
            print("❌ 无效选择")
    
    except KeyboardInterrupt:
        print("\n👋 用户取消操作")
    except Exception as e:
        print(f"❌ 程序错误: {e}")


if __name__ == "__main__":
    main()