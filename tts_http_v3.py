#!/usr/bin/env python3
"""
火山引擎TTS V3 HTTP接口实现
支持单向流式HTTP方式，兼容豆包语音合成模型2.0/复刻2.0/混音mix
"""
import base64
import json
import logging
import os
import uuid
from pathlib import Path
from typing import Dict, List, Optional, Union

import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TTSHttpClient:
    """火山引擎TTS V3 HTTP客户端"""
    
    def __init__(self):
        # 从环境变量读取配置
        self.appid = os.getenv("VOLCENGINE_APP_ID")
        self.access_token = os.getenv("VOLCENGINE_ACCESS_TOKEN")
        self.resource_id = os.getenv("TTS_V3_RESOURCE_ID", "seed-tts-2.0")
        self.voice_type = os.getenv("VOLCENGINE_VOICE_TYPE", "zh_female_vv_uranus_bigtts")
        
        # HTTP相关
        self.base_url = "https://openspeech.bytedance.com/api/v3/tts/unidirectional"
        self.session = requests.Session()  # 复用连接
        
        if not self.appid or not self.access_token:
            raise ValueError("❌ 请在.env文件中配置VOLCENGINE_APP_ID和VOLCENGINE_ACCESS_TOKEN")
    
    def get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        return {
            "X-Api-App-Id": self.appid,
            "X-Api-Access-Key": self.access_token,
            "X-Api-Resource-Id": self.resource_id,
            "X-Api-Request-Id": str(uuid.uuid4()),
            "Content-Type": "application/json"
        }
    
    def build_request_payload(
        self,
        text: str,
        speaker: str,
        audio_format: str = "wav",
        sample_rate: int = 24000,
        speech_rate: int = 0,
        loudness_rate: int = 0,
        emotion: Optional[str] = None,
        emotion_scale: int = 4,
        context_texts: Optional[List[str]] = None,
        section_id: Optional[str] = None,
        mix_speakers: Optional[List[Dict]] = None,
        **kwargs
    ) -> Dict:
        """构建请求负载"""
        payload = {
            "user": {
                "uid": kwargs.get("user_uid", "test_user_001")
            },
            "req_params": {
                "text": text,
                "speaker": speaker,
                "audio_params": {
                    "format": audio_format,
                    "sample_rate": sample_rate,
                    "speech_rate": speech_rate,
                    "loudness_rate": loudness_rate
                }
            }
        }
        
        # 添加比特率参数（仅MP3格式）
        if audio_format == "mp3" and kwargs.get("bit_rate"):
            payload["req_params"]["audio_params"]["bit_rate"] = kwargs["bit_rate"]
        
        # 添加情感参数
        if emotion:
            payload["req_params"]["audio_params"]["emotion"] = emotion
            payload["req_params"]["audio_params"]["emotion_scale"] = emotion_scale
        
        # 添加附加参数
        additions = {}
        
        # TTS2.0专用参数
        if context_texts and self.resource_id == "seed-tts-2.0":
            additions["context_texts"] = context_texts
        
        if section_id and self.resource_id == "seed-tts-2.0":
            additions["section_id"] = section_id
        
        # 其他可选参数
        if kwargs.get("enable_timestamp"):
            additions["enable_timestamp"] = True
        
        if kwargs.get("silence_duration"):
            additions["silence_duration"] = kwargs["silence_duration"]
        
        if kwargs.get("enable_language_detector"):
            additions["enable_language_detector"] = True
        
        if kwargs.get("disable_markdown_filter"):
            additions["disable_markdown_filter"] = True
        
        if kwargs.get("explicit_language"):
            additions["explicit_language"] = kwargs["explicit_language"]
        
        if kwargs.get("use_cache"):
            additions["cache_config"] = {
                "text_type": 1,
                "use_cache": True
            }
        
        if additions:
            payload["req_params"]["additions"] = json.dumps(additions, ensure_ascii=False)
        
        # 混音参数
        if mix_speakers:
            payload["req_params"]["speaker"] = "custom_mix_bigtts"
            payload["req_params"]["mix_speaker"] = {
                "speakers": mix_speakers
            }
        
        return payload
    
    def synthesize_speech(
        self,
        text: str,
        output_file: str,
        speaker: Optional[str] = None,
        audio_format: str = "wav",
        sample_rate: int = 24000,
        **kwargs
    ) -> bool:
        """
        合成语音
        
        Args:
            text: 要合成的文本
            output_file: 输出文件路径
            speaker: 语音类型，如不指定则使用默认值
            audio_format: 音频格式 (wav/mp3/pcm/ogg_opus)
            sample_rate: 采样率
            **kwargs: 其他参数
        
        Returns:
            bool: 是否成功
        """
        try:
            # 使用指定speaker或默认值
            voice_type = speaker or self.voice_type
            
            # 构建请求
            headers = self.get_headers()
            payload = self.build_request_payload(
                text=text,
                speaker=voice_type,
                audio_format=audio_format,
                sample_rate=sample_rate,
                **kwargs
            )
            
            logger.info(f"🚀 开始TTS合成: {text[:50]}...")
            logger.info(f"📋 使用音色: {voice_type}")
            logger.info(f"📋 资源ID: {self.resource_id}")
            
            # 发送流式请求
            response = self.session.post(
                self.base_url,
                headers=headers,
                json=payload,
                stream=True,
                timeout=60
            )
            
            # 检查HTTP状态码
            response.raise_for_status()
            
            # 获取logid
            logid = response.headers.get('X-Tt-Logid', 'unknown')
            logger.info(f"✅ 请求成功! LogID: {logid}")
            
            # 处理流式响应
            audio_data = bytearray()
            has_audio = False
            
            for line in response.iter_lines():
                if not line:
                    continue
                
                try:
                    # 解析JSON响应
                    response_data = json.loads(line.decode('utf-8'))
                    
                    # 检查错误
                    code = response_data.get('code', 0)
                    message = response_data.get('message', '')
                    
                    if code == 20000000:
                        # 合成结束
                        logger.info("🏁 音频合成完成")
                        break
                    elif code != 0:
                        # 错误响应
                        logger.error(f"❌ 服务端错误 [Code: {code}]: {message}")
                        return False
                    
                    # 获取音频数据
                    audio_base64 = response_data.get('data')
                    if audio_base64:
                        # 解码base64音频数据
                        audio_chunk = base64.b64decode(audio_base64)
                        audio_data.extend(audio_chunk)
                        has_audio = True
                        logger.info(f"🔊 接收音频数据: {len(audio_chunk)} 字节")
                    
                    # 获取时间戳信息（如果启用）
                    sentence = response_data.get('sentence')
                    if sentence:
                        logger.info(f"📝 时间戳信息: {sentence.get('text', '')}")
                
                except json.JSONDecodeError as e:
                    logger.warning(f"⚠️ 无法解析响应行: {line[:100]}... 错误: {e}")
                    continue
            
            # 保存音频文件
            if has_audio and audio_data:
                output_path = Path(output_file)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(output_path, 'wb') as f:
                    f.write(audio_data)
                
                logger.info(f"💾 音频保存成功: {output_path.absolute()}")
                logger.info(f"📊 文件大小: {len(audio_data):,} 字节 ({len(audio_data)/1024:.1f} KB)")
                return True
            else:
                logger.warning("⚠️ 没有接收到音频数据")
                return False
        
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ HTTP请求失败: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ 合成失败: {e}")
            return False
    
    def synthesize_with_mix(
        self,
        text: str,
        output_file: str,
        mix_speakers: List[Dict[str, Union[str, float]]],
        **kwargs
    ) -> bool:
        """
        混音合成
        
        Args:
            text: 要合成的文本
            output_file: 输出文件路径
            mix_speakers: 混音音色列表，格式: [{"source_speaker": "音色名", "mix_factor": 0.5}, ...]
            **kwargs: 其他参数
        
        Returns:
            bool: 是否成功
        """
        # 验证混音参数
        if not mix_speakers or len(mix_speakers) > 3:
            logger.error("❌ 混音音色数量必须在1-3个之间")
            return False
        
        total_factor = sum(speaker.get("mix_factor", 0) for speaker in mix_speakers)
        if abs(total_factor - 1.0) > 0.001:
            logger.error(f"❌ 混音影响因子总和必须等于1.0，当前为: {total_factor}")
            return False
        
        logger.info(f"🎵 开始混音合成，使用 {len(mix_speakers)} 个音色")
        for i, speaker in enumerate(mix_speakers, 1):
            logger.info(f"   {i}. {speaker['source_speaker']} (权重: {speaker['mix_factor']})")
        
        return self.synthesize_speech(
            text=text,
            output_file=output_file,
            mix_speakers=mix_speakers,
            **kwargs
        )
    
    def close(self):
        """关闭会话"""
        self.session.close()


def test_single_synthesis():
    """单个文本合成测试"""
    client = TTSHttpClient()
    
    try:
        text = input("请输入要转换的文本: ").strip()
        if not text:
            text = "你好，这是火山引擎V3 HTTP语音合成测试，使用豆包2.0模型"
        
        speaker = input("请输入语音类型 (回车使用默认): ").strip()
        if not speaker:
            speaker = None
        
        output_file = input("请输入输出文件名 (默认: test_http.wav): ").strip()
        if not output_file:
            output_file = "test_http.wav"
        
        # 询问是否启用高级选项
        use_advanced = input("是否启用高级选项? (y/n): ").strip().lower() == 'y'
        
        kwargs = {}
        if use_advanced:
            # 语速
            speed = input("语速 (-50到100, 默认0): ").strip()
            if speed:
                kwargs["speech_rate"] = int(speed)
            
            # 音量
            volume = input("音量 (-50到100, 默认0): ").strip()
            if volume:
                kwargs["loudness_rate"] = int(volume)
            
            # 情感（仅部分音色支持）
            emotion = input("情感 (如angry/happy/sad, 回车跳过): ").strip()
            if emotion:
                kwargs["emotion"] = emotion
                emotion_scale = input("情感强度 (1-5, 默认4): ").strip()
                if emotion_scale:
                    kwargs["emotion_scale"] = int(emotion_scale)
            
            # TTS2.0专用功能
            if client.resource_id == "seed-tts-2.0":
                context = input("上下文提示 (如'你可以说慢一点吗？', 回车跳过): ").strip()
                if context:
                    kwargs["context_texts"] = [context]
        
        print(f"\n🚀 开始合成: {text}")
        success = client.synthesize_speech(text, output_file, speaker, **kwargs)
        
        if success:
            print(f"✅ 合成成功! 音频文件: {output_file}")
        else:
            print("❌ 合成失败")
    
    finally:
        client.close()


def test_mix_synthesis():
    """混音合成测试"""
    client = TTSHttpClient()
    
    try:
        text = input("请输入要转换的文本: ").strip()
        if not text:
            text = "这是混音合成测试，多个音色混合效果"
        
        print("\n请输入混音音色配置:")
        mix_speakers = []
        
        while len(mix_speakers) < 3:
            speaker_name = input(f"音色 {len(mix_speakers) + 1} 名称 (回车结束): ").strip()
            if not speaker_name:
                break
            
            while True:
                try:
                    factor = float(input(f"音色 '{speaker_name}' 的权重 (0-1): ").strip())
                    if 0 <= factor <= 1:
                        break
                    else:
                        print("权重必须在0-1之间")
                except ValueError:
                    print("请输入有效的数字")
            
            mix_speakers.append({
                "source_speaker": speaker_name,
                "mix_factor": factor
            })
        
        if not mix_speakers:
            print("❌ 至少需要一个音色")
            return
        
        # 检查权重总和
        total = sum(s["mix_factor"] for s in mix_speakers)
        if abs(total - 1.0) > 0.001:
            print(f"⚠️ 权重总和为 {total:.3f}，将自动调整为1.0")
            for speaker in mix_speakers:
                speaker["mix_factor"] = speaker["mix_factor"] / total
        
        output_file = input("请输入输出文件名 (默认: test_mix.wav): ").strip()
        if not output_file:
            output_file = "test_mix.wav"
        
        print(f"\n🎵 开始混音合成: {text}")
        success = client.synthesize_with_mix(text, output_file, mix_speakers)
        
        if success:
            print(f"✅ 混音合成成功! 音频文件: {output_file}")
        else:
            print("❌ 混音合成失败")
    
    finally:
        client.close()


def test_batch_synthesis():
    """批量合成测试"""
    client = TTSHttpClient()
    
    try:
        texts = [
            "你好世界，欢迎使用火山引擎。",
            "这是HTTP方式的语音合成测试。",
            "今天天气真不错，适合出去走走。",
            "人工智能正在改变我们的生活。",
            "感谢您使用火山引擎语音服务。"
        ]
        
        print("🚀 开始批量合成测试...")
        success_count = 0
        
        for i, text in enumerate(texts, 1):
            print(f"\n📝 合成 {i}/{len(texts)}: {text}")
            output_file = f"batch_test_{i}.wav"
            
            success = client.synthesize_speech(text, output_file)
            
            if success:
                print(f"✅ 成功: {output_file}")
                success_count += 1
            else:
                print(f"❌ 失败: {text}")
        
        print(f"\n📊 批量测试完成! 成功: {success_count}/{len(texts)}")
        
        if success_count == len(texts):
            print("🎉 恭喜！HTTP接口测试全部通过！")
    
    finally:
        client.close()


def main():
    """主函数"""
    print("🎵 火山引擎TTS V3 HTTP接口测试程序")
    print("=" * 60)
    
    try:
        # 显示当前配置
        client = TTSHttpClient()
        print("📋 当前配置:")
        print(f"   - 资源ID: {client.resource_id}")
        print(f"   - 默认音色: {client.voice_type}")
        print(f"   - APP ID: {client.appid[:10]}****")
        print(f"   - 接口地址: {client.base_url}")
        client.close()
        
        print("\n选择测试模式:")
        print("1. 单个文本合成")
        print("2. 混音合成 (Mix)")
        print("3. 批量合成测试")
        
        choice = input("请选择 (1/2/3): ").strip()
        
        if choice == "1":
            test_single_synthesis()
        elif choice == "2":
            test_mix_synthesis()
        elif choice == "3":
            test_batch_synthesis()
        else:
            print("❌ 无效选择")
    
    except ValueError as e:
        print(f"❌ 配置错误: {e}")
        print("💡 请检查 .env 文件中的配置")
    except KeyboardInterrupt:
        print("\n👋 用户取消操作")
    except Exception as e:
        print(f"❌ 程序错误: {e}")


if __name__ == "__main__":
    main()