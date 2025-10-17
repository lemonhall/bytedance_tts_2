#!/usr/bin/env python3
"""
火山引擎TTS V3接口测试程序 - 豆包语音合成模型2.0
专注于V3单向流式WebSocket实现
"""
import asyncio
import json
import logging
import os
import struct
import uuid
from dataclasses import dataclass
from enum import IntEnum
from pathlib import Path
from typing import Optional

import websockets
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class V3MsgType(IntEnum):
    """V3消息类型"""
    FullClientRequest = 0b0001
    AudioOnlyResponse = 0b1011
    FullServerResponse = 0b1001
    Error = 0b1111


class V3EventType(IntEnum):
    """V3事件类型"""
    # 下行事件
    SessionFinished = 152
    TTSSentenceStart = 350
    TTSSentenceEnd = 351
    TTSResponse = 352
    
    # 上行事件
    FinishConnection = 2
    ConnectionFinished = 52


@dataclass
class V3Message:
    """V3协议消息"""
    version: int = 0b0001
    header_size: int = 0b0001  # 4字节
    msg_type: int = 0
    flags: int = 0
    serialization: int = 0b0001  # JSON
    compression: int = 0b0000  # 无压缩
    event: Optional[int] = None
    session_id: str = ""
    payload: bytes = b""


class V3TTSClient:
    """火山引擎V3 TTS客户端"""
    
    def __init__(self):
        # 从环境变量读取配置
        self.appid = os.getenv("VOLCENGINE_APP_ID")
        self.access_token = os.getenv("VOLCENGINE_ACCESS_TOKEN")
        self.resource_id = os.getenv("TTS_V3_RESOURCE_ID", "seed-tts-1.0")
        self.voice_type = os.getenv("VOLCENGINE_VOICE_TYPE", "zh_female_vv_uranus_bigtts")
        
        self.websocket = None
        self.session_id = ""
        
        if not self.appid or not self.access_token:
            raise ValueError("❌ 请在.env文件中配置VOLCENGINE_APP_ID和VOLCENGINE_ACCESS_TOKEN")


    def _encode_message(self, msg: V3Message) -> bytes:
        """编码V3消息为二进制"""
        # 构建header (4字节)
        header = bytearray(4)
        header[0] = (msg.version << 4) | msg.header_size
        header[1] = (msg.msg_type << 4) | msg.flags
        header[2] = (msg.serialization << 4) | msg.compression
        header[3] = 0x00  # Reserved
        
        # 添加可选字段
        optional_data = bytearray()
        
        if msg.flags == 0b0100:  # 有事件号
            if msg.event is not None:
                optional_data.extend(struct.pack(">I", msg.event))
            
            # session_id长度和内容
            session_bytes = msg.session_id.encode('utf-8')
            optional_data.extend(struct.pack(">I", len(session_bytes)))
            optional_data.extend(session_bytes)
        
        # payload长度和内容
        payload_data = bytearray()
        payload_data.extend(struct.pack(">I", len(msg.payload)))
        payload_data.extend(msg.payload)
        
        return bytes(header + optional_data + payload_data)
    
    def _decode_message(self, data: bytes) -> V3Message:
        """解码V3消息"""
        if len(data) < 4:
            raise ValueError("消息太短")
        
        msg = V3Message()
        
        # 解析header
        msg.version = (data[0] >> 4) & 0x0F
        msg.header_size = data[0] & 0x0F
        msg.msg_type = (data[1] >> 4) & 0x0F
        msg.flags = data[1] & 0x0F
        msg.serialization = (data[2] >> 4) & 0x0F
        msg.compression = data[2] & 0x0F
        
        offset = 4
        
        # 解析可选字段
        if msg.flags == 0b0100:  # 有事件号
            if offset + 4 <= len(data):
                msg.event = struct.unpack(">I", data[offset:offset+4])[0]
                offset += 4
            
            # session_id
            if offset + 4 <= len(data):
                session_len = struct.unpack(">I", data[offset:offset+4])[0]
                offset += 4
                if offset + session_len <= len(data):
                    msg.session_id = data[offset:offset+session_len].decode('utf-8')
                    offset += session_len
        
        # payload
        if offset + 4 <= len(data):
            payload_len = struct.unpack(">I", data[offset:offset+4])[0]
            offset += 4
            if offset + payload_len <= len(data):
                msg.payload = data[offset:offset+payload_len]
        
        return msg


async def test_tts(text: str, output_file: str, speaker: Optional[str] = None) -> bool:
    """测试V3 TTS"""
    client = V3TTSClient()
    
    try:
        # 连接
        endpoint = "wss://openspeech.bytedance.com/api/v3/tts/unidirectional/stream"
        
        headers = {
            "X-Api-App-Id": client.appid,
            "X-Api-Access-Key": client.access_token,
            "X-Api-Resource-Id": client.resource_id,
            "X-Api-Request-Id": str(uuid.uuid4()),
        }
        
        logger.info(f"� 连接V3端点: {endpoint}")
        logger.info(f"� 使用资源ID: {client.resource_id}")
        
        client.websocket = await websockets.connect(
            endpoint,
            additional_headers=headers,
            max_size=10 * 1024 * 1024
        )
        
        logid = client.websocket.response.headers.get('X-Tt-Logid', 'unknown')
        logger.info(f"✅ V3连接成功! LogID: {logid}")
        
        # 使用传入的speaker或默认值
        voice_type = speaker or client.voice_type
        
        # 构建V3请求数据
        request_data = {
            "user": {
                "uid": "test_user_001"
            },
            "req_params": {
                "text": text,
                "speaker": voice_type,
                "audio_params": {
                    "format": "wav",
                    "sample_rate": 24000
                }
            }
        }
        
        # 构建V3消息
        msg = V3Message(
            msg_type=V3MsgType.FullClientRequest,
            flags=0b0000,
            payload=json.dumps(request_data, ensure_ascii=False).encode('utf-8')
        )
        
        message_bytes = client._encode_message(msg)
        await client.websocket.send(message_bytes)
        logger.info(f"📤 发送V3文本请求: {text[:50]}...")
        
        # 接收响应
        audio_data = bytearray()
        
        while True:
            raw_message = await asyncio.wait_for(client.websocket.recv(), timeout=30.0)
            
            if isinstance(raw_message, str):
                logger.warning(f"⚠️  收到文本消息: {raw_message}")
                continue
            
            # 解码V3消息
            msg = client._decode_message(raw_message)
            
            logger.info(f"📨 收到V3消息: Type={msg.msg_type}, Event={msg.event}")
            
            if msg.event == V3EventType.TTSSentenceStart:
                logger.info("🎬 开始合成句子")
                client.session_id = msg.session_id
                
            elif msg.event == V3EventType.TTSResponse:
                # 音频数据
                audio_data.extend(msg.payload)
                logger.info(f"� 接收音频数据: {len(msg.payload)} 字节")
                
            elif msg.event == V3EventType.TTSSentenceEnd:
                logger.info("🏁 句子合成结束")
                
            elif msg.event == V3EventType.SessionFinished:
                # 会话结束
                if msg.payload:
                    try:
                        response = json.loads(msg.payload.decode('utf-8'))
                        logger.info(f"📋 会话结束响应: {response}")
                        
                        # 检查是否有明确的错误状态码
                        status_code = response.get('status_code')
                        if status_code is not None and status_code != 20000000:
                            logger.error(f"❌ 服务端错误: {response}")
                            return False
                    except json.JSONDecodeError:
                        logger.warning("⚠️  无法解析会话结束响应")
                else:
                    logger.info("📋 会话正常结束（无额外信息）")
                
                logger.info("✅ TTS处理完成")
                break
                
            elif msg.msg_type == V3MsgType.Error:
                error_msg = msg.payload.decode('utf-8') if msg.payload else "未知错误"
                logger.error(f"❌ V3服务端错误: {error_msg}")
                return False
        
        # 保存音频文件
        if audio_data:
            output_path = Path(output_file)
            with open(output_path, 'wb') as f:
                f.write(audio_data)
            logger.info(f"💾 音频保存成功: {output_path.absolute()}")
            logger.info(f"📊 文件大小: {len(audio_data):,} 字节 ({len(audio_data)/1024:.1f} KB)")
            return True
        else:
            logger.warning("⚠️  没有接收到音频数据")
            return False
        
    except Exception as e:
        logger.error(f"❌ V3测试失败: {e}")
        return False
    finally:
        if client.websocket:
            await client.websocket.close()


async def single_test():
    """单个文本测试"""
    text = input("请输入要转换的文本: ").strip()
    if not text:
        text = "你好，这是火山引擎V3语音合成测试，使用豆包2.0模型"
    
    speaker = input("请输入语音类型 (回车使用默认): ").strip()
    if not speaker:
        speaker = None
    
    output_file = input("请输入输出文件名 (默认: test.wav): ").strip()
    if not output_file:
        output_file = "test.wav"
    
    print(f"\n🚀 开始TTS测试: {text}")
    
    success = await test_tts(text, output_file, speaker)
    
    if success:
        print(f"✅ 测试成功! 音频文件: {output_file}")
    else:
        print("❌ 测试失败")


async def batch_test():
    """批量测试"""
    texts = [
        "你好世界",
        "这是火山引擎V3语音合成测试，使用豆包2.0模型",
        "今天天气真不错",
        "人工智能技术正在改变世界",
        "欢迎使用火山引擎语音合成服务"
    ]
    
    print("🚀 开始批量测试...")
    success_count = 0
    
    for i, text in enumerate(texts, 1):
        print(f"\n📝 测试 {i}/{len(texts)}: {text}")
        output_file = f"test_v3_{i}.wav"
        
        success = await test_tts(text, output_file)
        
        if success:
            print(f"✅ 成功: {output_file}")
            success_count += 1
        else:
            print(f"❌ 失败: {text}")
    
    print(f"\n📊 批量测试完成! 成功: {success_count}/{len(texts)}")
    
    if success_count == len(texts):
        print("🎉 恭喜！V3接口测试全部通过！")


async def main():
    """主函数"""
    print("🎵 火山引擎V3 TTS测试程序")
    print("=" * 50)
    
    try:
        # 显示当前配置
        client = V3TTSClient()
        print("📋 当前配置:")
        print(f"   - 资源ID: {client.resource_id}")
        print(f"   - 语音类型: {client.voice_type}")
        print(f"   - APP ID: {client.appid[:10]}****")
        
        print("\n选择测试模式:")
        print("1. 单个文本测试")
        print("2. 批量测试")
        
        choice = input("请选择 (1/2): ").strip()
        
        if choice == "1":
            await single_test()
        else:
            await batch_test()
            
    except ValueError as e:
        print(f"❌ 配置错误: {e}")
        print("💡 请检查 .env 文件中的配置")


if __name__ == "__main__":
    asyncio.run(main())