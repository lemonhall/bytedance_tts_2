#!/usr/bin/env python3
"""
长时间ASMR音频生成器 - 豆包TTS 2.0
基于最佳参数配置，生成长时间的MP3格式ASMR音频
使用"亲密耳语"场景的ultra_soft配置
"""
from tts_http_v3 import TTSHttpClient
import os
from pathlib import Path
import time

# 推荐使用豆包TTS 2.0音色
DEFAULT_SPEAKER = os.getenv("VOLCENGINE_VOICE_TYPE", "zh_female_vv_uranus_bigtts")

# 最佳ASMR参数配置（基于亲密耳语场景的ultra_soft配置）
BEST_ASMR_CONFIG = {
    "emotion": "ASMR",
    "emotion_scale": 5,
    "speech_rate": -2,  # 更慢的语速
    "loudness_rate": -3,  # 更轻的音量
    "audio_format": "mp3",  # 输出MP3格式
    "sample_rate": 24000,
    "bit_rate": 128  # MP3比特率
}

# 最佳ASMR上下文设置
BEST_ASMR_CONTEXT = ["用最亲密的ASMR耳语声", "就像情侣间的悄悄话", "声音要很贴近"]

# 长时间ASMR文案 - 适合10分钟音频
LONG_ASMR_SCRIPTS = {
    "深度放松冥想": [
        "闭上你的眼睛...深深地吸一口气...慢慢地呼出来...",
        "让所有的紧张和压力...都随着呼吸...慢慢地离开你的身体...",
        "感受你的肌肉...从头部开始...慢慢地放松下来...",
        "你的额头...变得平滑...没有任何紧张...",
        "你的眼皮...轻轻地合拢...感受这份宁静...",
        "你的脸颊...柔软而温暖...所有的表情都消失了...",
        "你的嘴唇...微微分开...呼吸变得更加深沉...",
        "现在让这份放松...延伸到你的肩膀...",
        "感受肩膀的重量...慢慢地沉下去...",
        "你的手臂...变得越来越重...越来越放松...",
        "手指...轻轻地摊开...没有任何紧张...",
        "这份放松...现在流向你的胸部...",
        "你的呼吸...变得更加缓慢...更加深沉...",
        "感受每一次呼吸...都带来更深的宁静...",
        "你的背部...贴着舒适的表面...完全地放松...",
        "腰部...臀部...也都加入了这场放松的旅程...",
        "现在...让这份宁静...流向你的双腿...",
        "大腿...小腿...都变得沉重而放松...",
        "你的脚踝...脚趾...也都完全地放松了...",
        "现在...你的整个身体...都沉浸在这份深深的宁静中...",
        "你就像漂浮在温暖的云朵上...无忧无虑...",
        "感受这份完美的平静...让它充满你的整个存在...",
        "在这个安全的空间里...你可以完全地释放自己...",
        "没有什么需要你担心...没有什么需要你思考...",
        "只需要享受这份纯粹的宁静...和深深的放松...",
        "让我的声音...成为你内心平静的锚点...",
        "每当你听到这个声音...你就会想起这份宁静...",
        "这份平静...将会伴随你很久很久...",
        "即使在你睁开眼睛之后...这份宁静仍然在那里...",
        "现在...让我们一起...在这份美好中...安静地停留一会儿..."
    ],
    
    "温柔陪伴夜语": [
        "夜已经很深了...外面的世界都安静下来了...",
        "只有我们两个人的时光...多么珍贵...",
        "你今天一定很辛苦吧...让我陪伴你一会儿...",
        "把你的头...轻轻地靠在我的肩膀上...",
        "感受这份温暖...这份安全感...",
        "你知道吗...你在我心中有多么特别...",
        "你的每一个微笑...都像星星一样闪亮...",
        "你的每一次呼吸...都让我感到安心...",
        "在这个宁静的夜晚...我想告诉你一些秘密...",
        "我喜欢你专注时的样子...那么认真...那么美丽...",
        "我喜欢你笑起来的声音...像银铃一样清脆...",
        "我喜欢你安静时的模样...那么平和...那么动人...",
        "月光透过窗帘...洒在你的脸上...",
        "就像天使身上的光环...那么柔和...",
        "你知道吗...有你在身边...我就不怕黑夜...",
        "因为你就是我心中最亮的那颗星...",
        "在这个世界上...能遇到你...是我最大的幸运...",
        "让我轻轻地抚摸你的头发...感受它的柔软...",
        "让我轻轻地亲吻你的额头...表达我的爱意...",
        "不要担心明天会发生什么...今晚我们就在这里...",
        "静静地享受这份美好...这份只属于我们的时光...",
        "听着我的心跳...它在为你而跳动...",
        "听着我的呼吸...它在和你同步...",
        "我们就这样...紧紧地拥抱着...",
        "让爱意...在这个安静的夜晚...慢慢地流淌...",
        "直到我们一起...在这份甜蜜中...进入梦乡..."
    ],
    
    "疗愈心灵花园": [
        "想象你正在走进一个美丽的花园...",
        "这里有你见过的最美丽的花朵...最绿的草地...",
        "空气中飘散着淡淡的花香...那么清新...那么怡人...",
        "你赤脚走在柔软的草地上...感受大地的温度...",
        "每一步都让你感到更加放松...更加平静...",
        "在花园的中央...有一个清澈的小池塘...",
        "池水像镜子一样...倒映着蓝天白云...",
        "你慢慢地坐在池边...感受水的宁静...",
        "微风轻拂过你的脸颊...带来花朵的香气...",
        "鸟儿在树梢上轻声歌唱...那么悦耳...那么和谐...",
        "在这个花园里...所有的烦恼都不存在了...",
        "这里只有美好...只有平静...只有爱...",
        "你感到心中的那些创伤...正在慢慢地愈合...",
        "就像花朵在阳光下绽放一样...自然而美丽...",
        "你内心的小孩...在这里找到了安全感...",
        "它可以自由地奔跑...自由地笑...自由地哭...",
        "所有被压抑的情感...都可以在这里得到释放...",
        "你不需要坚强...不需要完美...不需要讨好任何人...",
        "在这个花园里...你只需要做真实的自己...",
        "感受阳光洒在你的肩膀上...温暖而治愈...",
        "感受这份无条件的接纳...无条件的爱...",
        "你是值得被爱的...你是珍贵的...你是独一无二的...",
        "让这份爱...慢慢地充满你的心房...",
        "让它治愈你的每一个细胞...每一个念头...",
        "现在...深深地呼吸...吸入这份爱和光明...",
        "呼出所有的恐惧和痛苦...",
        "你已经准备好...带着这份新的能量...重新开始...",
        "这个花园...永远为你开放...你随时可以回来..."
    ]
}


def generate_long_asmr_mp3(script_name: str, output_filename: str = None):
    """
    生成长时间的ASMR MP3音频
    
    Args:
        script_name: 脚本名称
        output_filename: 输出文件名（可选）
    """
    if script_name not in LONG_ASMR_SCRIPTS:
        print(f"❌ 未找到脚本: {script_name}")
        print(f"可用脚本: {list(LONG_ASMR_SCRIPTS.keys())}")
        return False
    
    if not output_filename:
        output_filename = f"long_asmr_{script_name}.mp3"
    
    script_texts = LONG_ASMR_SCRIPTS[script_name]
    client = TTSHttpClient()
    
    try:
        print(f"\n🎧 开始生成长时间ASMR音频")
        print(f"📋 脚本: {script_name}")
        print(f"📝 段落数: {len(script_texts)}")
        print(f"📁 输出文件: {output_filename}")
        print(f"🎵 音色: {DEFAULT_SPEAKER}")
        print("=" * 60)
        
        # 估算总时长（每个段落大约15-25秒）
        estimated_duration = len(script_texts) * 20 / 60
        print(f"⏱️ 预估时长: {estimated_duration:.1f} 分钟")
        
        success_count = 0
        total_segments = len(script_texts)
        
        for i, text in enumerate(script_texts, 1):
            # 为每个段落生成临时文件
            temp_filename = f"temp_asmr_segment_{i:03d}.mp3"
            
            print(f"\n🎵 生成段落 {i}/{total_segments}: {text[:30]}...")
            
            success = client.synthesize_speech(
                text=text,
                output_file=temp_filename,
                speaker=DEFAULT_SPEAKER,
                context_texts=BEST_ASMR_CONTEXT,
                **BEST_ASMR_CONFIG
            )
            
            if success:
                print(f"✅ 段落 {i} 成功")
                success_count += 1
            else:
                print(f"❌ 段落 {i} 失败")
                
            # 添加延迟避免请求过快
            time.sleep(0.5)
        
        print(f"\n📊 音频生成完成!")
        print(f"✅ 成功段落: {success_count}/{total_segments}")
        
        if success_count > 0:
            print(f"\n💡 接下来需要手动合并MP3文件:")
            print(f"1. 使用音频编辑软件（如Audacity）")
            print(f"2. 或使用命令行工具合并所有 temp_asmr_segment_*.mp3")
            print(f"3. 最终输出为: {output_filename}")
            
            # 生成合并脚本
            generate_merge_script(success_count, output_filename)
        
        return success_count == total_segments
        
    except Exception as e:
        print(f"❌ 生成过程出错: {e}")
        return False
    finally:
        client.close()


def generate_merge_script(segment_count: int, output_filename: str):
    """生成音频合并脚本"""
    
    # PowerShell脚本
    ps_script = f"""# ASMR音频合并脚本 - PowerShell版本
# 需要先安装ffmpeg: https://ffmpeg.org/

$segments = @()
for ($i = 1; $i -le {segment_count}; $i++) {{
    $filename = "temp_asmr_segment_" + $i.ToString("000") + ".mp3"
    if (Test-Path $filename) {{
        $segments += "file '$filename'"
    }}
}}

# 创建文件列表
$segments | Out-File -FilePath "filelist.txt" -Encoding UTF8

# 使用ffmpeg合并
ffmpeg -f concat -safe 0 -i filelist.txt -c copy "{output_filename}"

# 清理临时文件
Remove-Item "filelist.txt"
Write-Host "合并完成: {output_filename}"
"""
    
    with open("merge_asmr_audio.ps1", "w", encoding="utf-8") as f:
        f.write(ps_script)
    
    # 批处理脚本
    bat_script = f"""@echo off
REM ASMR音频合并脚本 - 批处理版本
REM 需要先安装ffmpeg

echo 正在创建文件列表...
(
"""
    
    for i in range(1, segment_count + 1):
        bat_script += f'echo file "temp_asmr_segment_{i:03d}.mp3"\n'
    
    bat_script += f""") > filelist.txt

echo 正在合并音频...
ffmpeg -f concat -safe 0 -i filelist.txt -c copy "{output_filename}"

echo 清理临时文件...
del filelist.txt

echo 合并完成: {output_filename}
pause
"""
    
    with open("merge_asmr_audio.bat", "w", encoding="gbk") as f:
        f.write(bat_script)
    
    print(f"\n📜 已生成合并脚本:")
    print(f"   - merge_asmr_audio.ps1 (PowerShell版本)")
    print(f"   - merge_asmr_audio.bat (批处理版本)")
    print(f"💡 运行其中任一脚本即可合并音频")


def interactive_long_asmr_generator():
    """交互式长时间ASMR生成器"""
    print("\n🎧 长时间ASMR音频生成器")
    print("=" * 50)
    
    while True:
        print(f"\n📋 可用ASMR脚本:")
        for i, script_name in enumerate(LONG_ASMR_SCRIPTS.keys(), 1):
            script_texts = LONG_ASMR_SCRIPTS[script_name]
            estimated_duration = len(script_texts) * 20 / 60
            print(f"{i}. {script_name} (约 {estimated_duration:.1f} 分钟)")
        
        print("0. 退出")
        
        choice = input("\n请选择脚本 (0-3): ").strip()
        
        if choice == "0":
            print("👋 再见!")
            break
            
        try:
            script_idx = int(choice) - 1
            script_names = list(LONG_ASMR_SCRIPTS.keys())
            
            if 0 <= script_idx < len(script_names):
                script_name = script_names[script_idx]
                
                # 询问输出文件名
                output_name = input(f"输出文件名 (默认: long_asmr_{script_name}.mp3): ").strip()
                if not output_name:
                    output_name = f"long_asmr_{script_name}.mp3"
                
                # 确认生成
                script_texts = LONG_ASMR_SCRIPTS[script_name]
                estimated_duration = len(script_texts) * 20 / 60
                print(f"\n📝 即将生成:")
                print(f"   脚本: {script_name}")
                print(f"   段落数: {len(script_texts)}")
                print(f"   预估时长: {estimated_duration:.1f} 分钟")
                print(f"   输出文件: {output_name}")
                
                confirm = input("确认生成? (y/N): ").strip().lower()
                if confirm in ['y', 'yes']:
                    generate_long_asmr_mp3(script_name, output_name)
                else:
                    print("❌ 已取消")
            else:
                print("❌ 无效的脚本编号")
                
        except ValueError:
            print("❌ 请输入有效的数字")


if __name__ == "__main__":
    # 检查环境配置
    if not os.getenv("VOLCENGINE_APP_ID") or not os.getenv("VOLCENGINE_ACCESS_TOKEN"):
        print("❌ 请先配置火山引擎TTS API密钥!")
        print("请在.env文件中设置:")
        print("VOLCENGINE_APP_ID=你的AppID")
        print("VOLCENGINE_ACCESS_TOKEN=你的AccessToken")
        exit(1)
    
    # 启动交互式生成器
    interactive_long_asmr_generator()