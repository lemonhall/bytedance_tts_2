"""
TTS音频生成器
"""
import os
import sys
from pathlib import Path
from typing import List, Optional

# 添加父目录到路径以导入TTS模块
sys.path.append(str(Path(__file__).parent.parent))

from tts_http_v3 import TTSHttpClient
from project_schema import DialogueLine, DialogueProject


class TTSGenerator:
    """TTS音频生成器"""
    
    def __init__(self, output_dir: str = "dialogue_output"):
        """
        初始化
        :param output_dir: 音频输出目录
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # 初始化TTS客户端
        try:
            self.tts_client = TTSHttpClient()
        except Exception as e:
            raise ValueError(f"TTS客户端初始化失败: {e}")
    
    def generate_line(self, line: DialogueLine, voice_type: str, 
                     line_index: int) -> Optional[str]:
        """
        生成单句对话的音频
        :param line: 对话行
        :param voice_type: 音色类型
        :param line_index: 对话索引
        :return: 音频文件路径
        """
        try:
            # 构建输出文件名
            output_file = self.output_dir / f"line_{line_index:03d}.wav"
            
            # 构建请求参数
            kwargs = {
                "speed_ratio": line.speed_ratio,
                "volume_ratio": line.volume_ratio,
                "pitch_ratio": line.pitch_ratio,
            }
            
            # 添加情感参数(如果有)
            if line.emotion:
                kwargs["emotion"] = line.emotion
            
            # 添加上下文参数(如果有)
            if line.context:
                kwargs["pure_text"] = line.context
            
            # 生成音频
            success = self.tts_client.synthesize_speech(
                text=line.text,
                output_file=str(output_file),
                speaker=voice_type,
                audio_format="wav",
                sample_rate=24000,
                **kwargs
            )
            
            if success:
                return str(output_file)
            else:
                print(f"生成失败: {line.text[:20]}...")
                return None
                
        except Exception as e:
            print(f"生成音频时出错: {e}")
            return None
    
    def generate_project(self, project: DialogueProject) -> List[str]:
        """
        生成整个工程的音频
        :param project: 对话工程
        :return: 生成的音频文件列表
        """
        audio_files = []
        
        # 创建说话人ID到音色的映射
        speaker_voices = {
            speaker.id: speaker.voice_type
            for speaker in project.speakers
        }
        
        # 生成每一句对话
        for i, dialogue in enumerate(project.dialogues):
            voice_type = speaker_voices.get(dialogue.speaker_id, "zh_male_wennuanahu_moon_bigtts")
            
            print(f"正在生成 [{i+1}/{len(project.dialogues)}]: {dialogue.text[:30]}...")
            
            audio_file = self.generate_line(dialogue, voice_type, i)
            
            if audio_file:
                audio_files.append(audio_file)
                # 更新对话对象
                dialogue.audio_file = audio_file
            else:
                print(f"跳过第 {i+1} 句")
        
        return audio_files
    
    def merge_audio_files(self, audio_files: List[str], output_file: str) -> bool:
        """
        使用FFmpeg合并音频文件
        :param audio_files: 音频文件列表
        :param output_file: 输出文件路径
        :return: 是否成功
        """
        if not audio_files:
            print("没有音频文件可合并")
            return False
        
        try:
            import subprocess
            
            # 创建临时文件列表
            list_file = self.output_dir / "file_list.txt"
            with open(list_file, "w", encoding="utf-8") as f:
                for audio_file in audio_files:
                    # FFmpeg需要路径格式
                    abs_path = Path(audio_file).absolute()
                    f.write(f"file '{abs_path}'\n")
            
            # 使用FFmpeg合并
            cmd = [
                "ffmpeg",
                "-f", "concat",
                "-safe", "0",
                "-i", str(list_file),
                "-c", "copy",
                "-y",  # 覆盖输出文件
                output_file
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding="utf-8"
            )
            
            if result.returncode == 0:
                print(f"音频合并成功: {output_file}")
                # 清理临时文件
                list_file.unlink()
                return True
            else:
                print(f"FFmpeg错误: {result.stderr}")
                return False
                
        except FileNotFoundError:
            print("未找到FFmpeg,请先安装FFmpeg")
            return False
        except Exception as e:
            print(f"合并音频时出错: {e}")
            return False


if __name__ == "__main__":
    # 测试
    from project_schema import Speaker, DialogueProject
    
    # 创建测试工程
    project = DialogueProject(
        original_text="测试对话",
        speakers=[
            Speaker(
                id="speaker_1",
                name="小明",
                gender="male",
                voice_type="zh_male_wennuanahu_moon_bigtts"
            )
        ],
        dialogues=[
            DialogueLine(
                id="line_1",
                speaker_id="speaker_1",
                text="你好,这是一个测试。",
                emotion="开心"
            )
        ]
    )
    
    generator = TTSGenerator()
    audio_files = generator.generate_project(project)
    
    if audio_files:
        output = "dialogue_output/merged.wav"
        generator.merge_audio_files(audio_files, output)
