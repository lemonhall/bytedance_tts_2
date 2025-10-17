#!/usr/bin/env python3
"""
豆包TTS 2.0 ASMR上下文音频生成脚本
测试各种ASMR场景下的轻柔语音效果
结合context_texts上下文功能，生成更自然的ASMR音频
"""
from tts_http_v3 import TTSHttpClient
import os
from pathlib import Path

# 推荐使用豆包TTS 2.0音色（支持上下文和ASMR）
DEFAULT_SPEAKER = os.getenv("VOLCENGINE_VOICE_TYPE", "zh_female_vv_uranus_bigtts")

# ASMR场景测试用例
ASMR_SCENARIOS = {
    "放松冥想": {
        "context": ["请用最轻柔、最放松的ASMR语气说话", "像耳语一样轻柔", "慢慢地、轻轻地"],
        "texts": [
            "闭上眼睛...深深地吸一口气...慢慢地呼出来...",
            "让所有的紧张和压力...都随着呼吸...慢慢地离开你的身体...",
            "现在你感到非常放松...非常平静...就像漂浮在温暖的云朵上...",
            "听着我的声音...让它带你进入一个宁静祥和的世界..."
        ]
    },
    
    "温柔陪伴": {
        "context": ["用最温柔的ASMR声音", "就像在耳边轻语", "充满爱意和关怀"],
        "texts": [
            "你今天辛苦了...让我陪伴你一会儿...",
            "把头靠在我的肩膀上...感受这份温暖...",
            "你是如此的特别...如此的珍贵...",
            "不用担心任何事情...我会一直在这里..."
        ]
    },
    
    "舒缓助眠": {
        "context": ["用催眠般的ASMR声音", "非常轻柔，适合睡前", "声音要很轻很慢"],
        "texts": [
            "夜已经很深了...是时候让心灵得到休息...",
            "月光洒在你的床边...带来一片宁静...",
            "让我的声音...成为你今夜最温柔的摇篮曲...",
            "慢慢地...慢慢地...进入甜美的梦乡..."
        ]
    },
    
    "自然声响": {
        "context": ["模拟自然环境的ASMR效果", "声音要有层次感", "轻柔但富有质感"],
        "texts": [
            "听...雨滴轻轻地敲打着窗户...滴答...滴答...",
            "微风轻拂过树叶...发出沙沙的声响...",
            "远处传来鸟儿轻柔的歌声...啾啾...啾啾...",
            "小溪缓缓流淌...带着大自然最纯净的声音..."
        ]
    },
    
    "亲密耳语": {
        "context": ["用最亲密的ASMR耳语声", "就像情侣间的悄悄话", "声音要很贴近"],
        "texts": [
            "只有我们两个人的时光...多么美好...",
            "让我轻轻地告诉你...你在我心中的位置...",
            "你的每一个笑容...都让我的心怦怦跳...",
            "这一刻...只属于我们..."
        ]
    },
    
    "疗愈引导": {
        "context": ["用疗愈师般的ASMR声音", "温暖而有力量", "充满正能量"],
        "texts": [
            "你已经很勇敢了...为自己感到骄傲吧...",
            "每一次呼吸...都在治愈着你的心灵...",
            "相信自己...你拥有无限的可能...",
            "明天的太阳...会为你带来全新的希望..."
        ]
    },
    
    "创意触发": {
        "context": ["用神秘而富有创意的ASMR声音", "激发想象力", "声音要有魅力"],
        "texts": [
            "在你的内心深处...隐藏着无限的创意...",
            "让想象的翅膀...带你飞向未知的世界...",
            "每一个念头...都可能成为伟大的开始...",
            "闭上眼睛...看见你内心的光芒..."
        ]
    }
}

# ASMR参数配置
ASMR_CONFIGS = {
    "ultra_soft": {
        "emotion": "ASMR",
        "emotion_scale": 5,
        "speech_rate": -2,  # 更慢的语速
        "loudness_rate": -3  # 更轻的音量
    },
    "gentle": {
        "emotion": "ASMR", 
        "emotion_scale": 4,
        "speech_rate": -1,
        "loudness_rate": -2
    },
    "whisper": {
        "emotion": "ASMR",
        "emotion_scale": 6,
        "speech_rate": -3,
        "loudness_rate": -4
    }
}


def generate_asmr_audio(scenario_name: str, config_name: str = "ultra_soft", output_dir: str = "asmr_output"):
    """
    生成指定场景的ASMR音频
    
    Args:
        scenario_name: ASMR场景名称
        config_name: ASMR配置名称
        output_dir: 输出目录
    """
    if scenario_name not in ASMR_SCENARIOS:
        print(f"❌ 未找到场景: {scenario_name}")
        print(f"可用场景: {list(ASMR_SCENARIOS.keys())}")
        return False
        
    if config_name not in ASMR_CONFIGS:
        print(f"❌ 未找到配置: {config_name}")
        print(f"可用配置: {list(ASMR_CONFIGS.keys())}")
        return False
    
    # 创建输出目录
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    scenario = ASMR_SCENARIOS[scenario_name]
    config = ASMR_CONFIGS[config_name]
    
    client = TTSHttpClient()
    
    try:
        print(f"\n🎧 开始生成ASMR音频")
        print(f"📋 场景: {scenario_name}")
        print(f"📋 配置: {config_name}")
        print(f"📋 音色: {DEFAULT_SPEAKER}")
        print(f"📁 输出目录: {output_path.absolute()}")
        print("=" * 50)
        
        success_count = 0
        total_texts = len(scenario["texts"])
        
        for i, text in enumerate(scenario["texts"], 1):
            # 生成文件名
            safe_name = scenario_name.replace(" ", "_").replace("/", "_")
            output_file = output_path / f"asmr_{safe_name}_{config_name}_{i:02d}.wav"
            
            print(f"\n🎵 生成 {i}/{total_texts}: {text[:40]}...")
            
            # 合成语音
            success = client.synthesize_speech(
                text=text,
                output_file=str(output_file),
                speaker=DEFAULT_SPEAKER,
                context_texts=scenario["context"],  # 使用上下文
                **config  # 使用ASMR配置
            )
            
            if success:
                print(f"✅ 成功: {output_file.name}")
                success_count += 1
            else:
                print(f"❌ 失败: {text[:30]}...")
        
        print(f"\n📊 场景 '{scenario_name}' 完成!")
        print(f"✅ 成功: {success_count}/{total_texts}")
        
        return success_count == total_texts
        
    except Exception as e:
        print(f"❌ 生成过程出错: {e}")
        return False
    finally:
        client.close()


def generate_all_asmr_scenarios(config_name: str = "ultra_soft", output_dir: str = "asmr_output"):
    """
    生成所有ASMR场景的音频
    
    Args:
        config_name: ASMR配置名称
        output_dir: 输出目录
    """
    print(f"\n🎧 批量生成所有ASMR场景音频")
    print(f"📋 使用配置: {config_name}")
    print("=" * 60)
    
    success_scenarios = 0
    total_scenarios = len(ASMR_SCENARIOS)
    
    for scenario_name in ASMR_SCENARIOS.keys():
        print(f"\n🎭 处理场景: {scenario_name}")
        if generate_asmr_audio(scenario_name, config_name, output_dir):
            success_scenarios += 1
        print("-" * 50)
    
    print(f"\n🎉 全部场景处理完成!")
    print(f"✅ 成功场景: {success_scenarios}/{total_scenarios}")


def test_asmr_configs_comparison():
    """
    对比测试不同ASMR配置的效果
    """
    test_text = "轻轻地...慢慢地...让我们一起放松下来..."
    test_context = ["请用最轻柔的ASMR语气说话", "像耳语一样轻柔"]
    
    client = TTSHttpClient()
    
    try:
        print(f"\n🧪 ASMR配置对比测试")
        print(f"📝 测试文本: {test_text}")
        print("=" * 50)
        
        for config_name, config in ASMR_CONFIGS.items():
            output_file = f"asmr_config_test_{config_name}.wav"
            
            print(f"\n🎵 测试配置: {config_name}")
            print(f"   参数: {config}")
            
            success = client.synthesize_speech(
                text=test_text,
                output_file=output_file,
                speaker=DEFAULT_SPEAKER,
                context_texts=test_context,
                **config
            )
            
            if success:
                print(f"✅ 成功: {output_file}")
            else:
                print(f"❌ 失败: {config_name}")
    
    except Exception as e:
        print(f"❌ 测试过程出错: {e}")
    finally:
        client.close()


def interactive_asmr_generator():
    """
    交互式ASMR音频生成器
    """
    print("\n🎧 豆包TTS 2.0 ASMR音频生成器")
    print("=" * 50)
    
    while True:
        print("\n📋 可用选项:")
        print("1. 生成单个ASMR场景")
        print("2. 生成所有ASMR场景")
        print("3. 对比测试ASMR配置")
        print("4. 查看场景列表")
        print("5. 查看配置列表")
        print("0. 退出")
        
        choice = input("\n请选择操作 (0-5): ").strip()
        
        if choice == "0":
            print("👋 再见!")
            break
            
        elif choice == "1":
            # 单个场景生成
            print("\n📋 可用ASMR场景:")
            for i, name in enumerate(ASMR_SCENARIOS.keys(), 1):
                print(f"{i}. {name}")
            
            try:
                scenario_idx = int(input("选择场景编号: ")) - 1
                scenario_names = list(ASMR_SCENARIOS.keys())
                
                if 0 <= scenario_idx < len(scenario_names):
                    scenario_name = scenario_names[scenario_idx]
                    
                    print("\n📋 可用配置:")
                    for i, name in enumerate(ASMR_CONFIGS.keys(), 1):
                        print(f"{i}. {name}")
                    
                    config_idx = int(input("选择配置编号 (默认1): ") or "1") - 1
                    config_names = list(ASMR_CONFIGS.keys())
                    
                    if 0 <= config_idx < len(config_names):
                        config_name = config_names[config_idx]
                        generate_asmr_audio(scenario_name, config_name)
                    else:
                        print("❌ 无效的配置编号")
                else:
                    print("❌ 无效的场景编号")
                    
            except ValueError:
                print("❌ 请输入有效的数字")
                
        elif choice == "2":
            # 批量生成
            print("\n📋 可用配置:")
            for i, name in enumerate(ASMR_CONFIGS.keys(), 1):
                print(f"{i}. {name}")
            
            try:
                config_idx = int(input("选择配置编号 (默认1): ") or "1") - 1
                config_names = list(ASMR_CONFIGS.keys())
                
                if 0 <= config_idx < len(config_names):
                    config_name = config_names[config_idx]
                    generate_all_asmr_scenarios(config_name)
                else:
                    print("❌ 无效的配置编号")
                    
            except ValueError:
                print("❌ 请输入有效的数字")
                
        elif choice == "3":
            # 配置对比测试
            test_asmr_configs_comparison()
            
        elif choice == "4":
            # 查看场景列表
            print("\n📋 ASMR场景列表:")
            for name, info in ASMR_SCENARIOS.items():
                print(f"\n🎭 {name}:")
                print(f"   上下文: {info['context']}")
                print(f"   文本数量: {len(info['texts'])}")
                
        elif choice == "5":
            # 查看配置列表
            print("\n📋 ASMR配置列表:")
            for name, config in ASMR_CONFIGS.items():
                print(f"\n⚙️ {name}: {config}")
                
        else:
            print("❌ 无效选择，请重试")


if __name__ == "__main__":
    # 检查环境配置
    if not os.getenv("VOLCENGINE_APP_ID") or not os.getenv("VOLCENGINE_ACCESS_TOKEN"):
        print("❌ 请先配置火山引擎TTS API密钥!")
        print("请在.env文件中设置:")
        print("VOLCENGINE_APP_ID=你的AppID")
        print("VOLCENGINE_ACCESS_TOKEN=你的AccessToken")
        exit(1)
    
    # 启动交互式生成器
    interactive_asmr_generator()