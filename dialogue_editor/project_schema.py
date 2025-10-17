"""
对话TTS工程文件的数据模型定义
"""
from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from tts_config import (
    CHINESE_EMOTION_NAMES,
    ENGLISH_EMOTION_NAMES,
    VOICE_TYPES,
    get_voice_type
)


class Speaker(BaseModel):
    """说话人信息"""
    id: str = Field(..., description="说话人唯一标识")
    name: str = Field(default="", description="说话人名称")
    gender: Literal["male", "female", "child"] = Field(..., description="性别")
    age_group: Literal["child", "teenager", "adult", "elder"] = Field(default="adult", description="年龄段")
    voice_type: str = Field(..., description="火山引擎音色ID")
    
    
class DialogueLine(BaseModel):
    """单条对话"""
    id: str = Field(..., description="对话行唯一标识")
    speaker_id: str = Field(..., description="说话人ID")
    text: str = Field(..., description="对话文本内容")
    
    # TTS参数
    emotion: Optional[str] = Field(default=None, description="情感(中文24种/英文10种)")
    speed_ratio: float = Field(default=1.0, ge=0.2, le=3.0, description="语速")
    volume_ratio: float = Field(default=1.0, ge=0.1, le=3.0, description="音量")
    pitch_ratio: float = Field(default=1.0, ge=0.1, le=3.0, description="音调")
    
    # 上下文(前面的对话内容,用于智能调整)
    context: Optional[str] = Field(default=None, description="上下文对话")
    
    # 音频输出
    audio_file: Optional[str] = Field(default=None, description="生成的音频文件路径")
    duration: Optional[float] = Field(default=None, description="音频时长(秒)")


class DialogueProject(BaseModel):
    """对话TTS工程文件"""
    version: str = Field(default="1.0", description="工程文件版本")
    title: str = Field(default="未命名对话", description="工程标题")
    
    # 原始输入
    original_text: str = Field(..., description="原始对话文本")
    
    # 分析结果
    speakers: List[Speaker] = Field(default_factory=list, description="说话人列表")
    dialogues: List[DialogueLine] = Field(default_factory=list, description="对话列表")
    
    # 音频输出
    output_audio: Optional[str] = Field(default=None, description="最终合成的音频文件")
    
    # 元数据
    created_at: Optional[str] = Field(default=None, description="创建时间")
    updated_at: Optional[str] = Field(default=None, description="更新时间")


# 为了向后兼容，导出配置（已从tts_config.py导入）
CHINESE_EMOTIONS = CHINESE_EMOTION_NAMES
ENGLISH_EMOTIONS = ENGLISH_EMOTION_NAMES
# VOICE_TYPES 已从tts_config导入
