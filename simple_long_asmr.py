#!/usr/bin/env python3
"""
简化版长ASMR生成器 - 分段生成+拼接
基于最佳参数配置，生成单个长时间MP3文件
支持分段生成，保持上下文一致性
"""
from tts_http_v3 import TTSHttpClient
import os
import subprocess

# 推荐使用豆包TTS 2.0音色
DEFAULT_SPEAKER = os.getenv("VOLCENGINE_VOICE_TYPE", "zh_female_vv_uranus_bigtts")

# 最佳ASMR参数配置
BEST_ASMR_CONFIG = {
    "emotion": "ASMR",
    "emotion_scale": 5,
    "speech_rate": -2,
    "loudness_rate": -3,
    "audio_format": "mp3",
    "sample_rate": 24000,
    "bit_rate": 128
}

# 最佳上下文设置
BEST_ASMR_CONTEXT = ["用最亲密的ASMR耳语声", "就像情侣间的悄悄话", "声音要很贴近"]

def split_text_into_segments(text, num_segments=5):
    """
    将文本分成指定数量的段落
    尽量保证每段的长度均匀
    """
    # 按照中文句号、感叹号、问号等标点分割
    import re
    # 替换常见的句子结尾标点
    text = text.strip()
    
    # 按标点符号分割成句子
    sentences = re.split(r'([。！？，、；：])', text)
    
    # 重新组合句子（保留标点）
    combined_sentences = []
    i = 0
    while i < len(sentences):
        if i + 1 < len(sentences) and sentences[i + 1] in '。！？，、；：':
            combined_sentences.append(sentences[i] + sentences[i + 1])
            i += 2
        elif sentences[i].strip():
            combined_sentences.append(sentences[i])
            i += 1
        else:
            i += 1
    
    if not combined_sentences:
        # 如果没有分割出句子，直接按字符长度分割
        char_count = len(text)
        segment_len = char_count // num_segments
        segments = []
        for i in range(num_segments):
            start = i * segment_len
            if i == num_segments - 1:
                segments.append(text[start:].strip())
            else:
                segments.append(text[start:start + segment_len].strip())
        return segments
    
    # 根据句子数量分段
    total_sentences = len(combined_sentences)
    sentences_per_segment = max(1, total_sentences // num_segments)
    
    segments = []
    for i in range(num_segments):
        start_idx = i * sentences_per_segment
        if i == num_segments - 1:
            # 最后一段包含所有剩余的句子
            segment_text = ''.join(combined_sentences[start_idx:]).strip()
        else:
            end_idx = start_idx + sentences_per_segment
            segment_text = ''.join(combined_sentences[start_idx:end_idx]).strip()
        
        if segment_text:
            segments.append(segment_text)
    
    return segments


def merge_audio_files(audio_files, output_file):
    """
    使用ffmpeg将多个MP3文件合并成一个
    """
    try:
        # 创建ffmpeg的concat demuxer列表文件
        concat_file = "concat_list.txt"
        
        print(f"  📝 创建合并列表...")
        with open(concat_file, 'w', encoding='utf-8') as f:
            for audio_file in audio_files:
                if os.path.exists(audio_file):
                    # Windows路径需要转义
                    f.write(f"file '{os.path.abspath(audio_file)}'\n")
        
        print(f"  🔗 使用ffmpeg合并音频...")
        # 使用ffmpeg的concat demuxer合并
        cmd = [
            'ffmpeg',
            '-f', 'concat',
            '-safe', '0',
            '-i', concat_file,
            '-c', 'copy',  # 复制编码，不重新编码
            '-y',  # 覆盖输出文件
            output_file
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"  ✅ 合并完成: {output_file}")
            
            # 清理临时文件
            for audio_file in audio_files:
                if os.path.exists(audio_file) and audio_file != output_file:
                    try:
                        os.remove(audio_file)
                        print(f"  🗑️  清理临时文件: {audio_file}")
                    except:
                        pass
            
            # 清理concat列表文件
            try:
                os.remove(concat_file)
                print(f"  🗑️  清理合并列表: {concat_file}")
            except:
                pass
            
            return True
        else:
            print(f"  ❌ ffmpeg执行失败")
            print(f"  错误: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"  ❌ 合并失败: {e}")
        return False


def generate_single_long_asmr(num_segments=5):
    """生成单个长时间ASMR音频"""
    
    # 长文案 - 约10分钟助眠内容
    long_asmr_text = """
    轻轻地闭上你的眼睛...深深地吸一口气...慢慢地呼出来...让所有的紧张和压力...都随着呼吸...慢慢地离开你的身体...

    夜已经很深了...外面的世界都安静下来了...这是属于你的宁静时光...让心灵得到真正的休息...

    现在...让我们开始一段放松的旅程...感受你的身体...从头部开始...慢慢地放松下来...你的额头...变得平滑...没有任何紧张...

    你的眼皮...轻轻地合拢...感受这份安宁...你的脸颊...柔软而温暖...所有的表情都消失了...你的嘴唇...微微分开...呼吸变得更加深沉...

    现在让这份放松...延伸到你的肩膀...感受肩膀的重量...慢慢地沉下去...就像卸下了一天的负担...你的手臂...变得越来越重...越来越放松...

    手指...轻轻地摊开...没有任何紧张...这份放松...现在流向你的胸部...你的呼吸...变得更加缓慢...更加深沉...

    感受每一次呼吸...都带来更深的宁静...你的心跳...也变得平缓而规律...像大自然最温柔的节拍...

    想象你正在走进一个宁静的森林...这里有高大的树木...茂密的绿叶...空气清新而纯净...每一次呼吸...都让你感到更加放松...

    你沿着一条小径慢慢地走着...脚下是柔软的落叶...发出轻微的沙沙声...这声音让你感到无比的平静...

    在森林的深处...有一个清澈的小溪...水声潺潺...像最温柔的摇篮曲...你坐在溪边的一块平滑的石头上...感受大自然的宁静...

    微风轻拂过树梢...带来花草的清香...鸟儿偶尔传来轻柔的鸣叫声...一切都是那么和谐...那么宁静...

    在这个森林里...时间仿佛停止了...没有任何压力...没有任何烦恼...只有纯粹的宁静和放松...

    你的背部...现在完全地贴着舒适的表面...所有的肌肉都放松了...腰部...臀部...也都加入了这场放松的旅程...

    现在...让这份宁静...流向你的双腿...大腿...小腿...都变得沉重而放松...你的脚踝...脚趾...也都完全地放松了...

    现在...你的整个身体...都沉浸在这份深深的宁静中...就像漂浮在温暖的云朵上...无忧无虑...

    月光透过树叶的缝隙...洒在你的身上...带来一种温和的光辉...这光辉有治愈的力量...慢慢地渗透到你的每一个细胞...

    感受这份完美的平静...让它充满你的整个存在...在这个安全的空间里...你可以完全地释放自己...

    没有什么需要你担心...没有什么需要你思考...只需要享受这份纯粹的宁静...和深深的放松...

    你的呼吸...现在变得非常缓慢...非常深沉...每一次呼气...都带走更多的紧张...每一次吸气...都带来更深的平静...

    让你的意识...慢慢地沉入这份宁静之中...就像沉入温暖的海洋...感受那种被轻柔地包围的感觉...

    在这个宁静的森林里...你找到了内心的平衡...所有的焦虑都消散了...所有的疲惫都消失了...

    你感到前所未有的轻松...前所未有的平静...这种感觉会伴随你进入梦乡...让你的睡眠变得深沉而甜美...

    现在...让你的呼吸...成为通往梦境的桥梁...每一次呼吸...都让你更接近那个宁静的梦乡...

    在那里...有最美好的风景...最温柔的声音...最舒适的环境...你将在那里得到最充分的休息...

    让这份宁静...深深地印在你的记忆里...每当你需要放松的时候...你都可以回到这个森林...回到这份宁静...

    现在...慢慢地...让你的意识...沉入更深的宁静之中...感受那种被温柔包围的感觉...让它带你进入甜美的梦乡...

    愿这份宁静...伴随你整个夜晚...愿你的梦境...充满美好和平静...愿你醒来时...感到精神焕发...充满活力...

    现在...安心地睡吧...在这份深深的宁静中...进入最甜美的梦乡...晚安...
    """
    
    client = TTSHttpClient()
    
    try:
        print(f"\n🎧 生成长时间助眠ASMR音频（分段模式）")
        print(f"📝 文本长度: {len(long_asmr_text)} 字符")
        print(f"� 分段数: {num_segments}")
        print(f"�📁 输出文件: long_asmr_sleep_relaxation.mp3")
        print(f"🎵 使用音色: {DEFAULT_SPEAKER}")
        print(f"⚙️ 参数配置: {BEST_ASMR_CONFIG}")
        print(f"📌 上下文: {BEST_ASMR_CONTEXT}")
        print("=" * 60)
        
        # 分段文本
        print("\n📖 正在分段文本...")
        segments = split_text_into_segments(long_asmr_text.strip(), num_segments)
        
        print(f"✅ 分段完成，共{len(segments)}段：")
        for i, segment in enumerate(segments, 1):
            print(f"  第{i}段: {len(segment)}字符")
        
        # 为每段生成音频
        print("\n🎵 正在生成各段音频...")
        audio_files = []
        
        for i, segment in enumerate(segments, 1):
            segment_file = f"asmr_segment_{i}.mp3"
            print(f"\n  【第 {i}/{num_segments} 段】")
            print(f"  📝 文本长度: {len(segment)} 字符")
            
            success = client.synthesize_speech(
                text=segment,
                output_file=segment_file,
                speaker=DEFAULT_SPEAKER,
                context_texts=BEST_ASMR_CONTEXT,  # 每段都使用相同的上下文
                **BEST_ASMR_CONFIG
            )
            
            if success:
                print(f"  ✅ 第{i}段生成成功: {segment_file}")
                audio_files.append(segment_file)
            else:
                print(f"  ❌ 第{i}段生成失败")
                return False
        
        # 合并所有音频
        print("\n🔗 正在合并音频文件...")
        if merge_audio_files(audio_files, "long_asmr_sleep_relaxation.mp3"):
            print(f"\n✅ 长时间助眠ASMR音频生成成功!")
            print(f"📁 文件: long_asmr_sleep_relaxation.mp3")
            print(f"💡 建议睡前使用耳机聆听，有助于放松入眠")
            print(f"📊 生成方式: 分{num_segments}段生成，相同上下文约束保证一致性")
            return True
        else:
            print(f"❌ 音频合并失败")
            return False
            
    except Exception as e:
        print(f"❌ 生成过程出错: {e}")
        import traceback
        traceback.print_exc()
        return False
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
    
    generate_single_long_asmr(num_segments=5)