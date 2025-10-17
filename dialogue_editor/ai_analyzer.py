"""
使用AI分析对话文本
"""
import json
import os
from typing import Dict, Any
import requests
from tts_config import CHINESE_EMOTION_NAMES, VOICE_TYPES, get_voice_type


class DialogueAnalyzer:
    """对话分析器,使用DeepSeek或其他LLM"""
    
    def __init__(self, api_key: str = None, api_base: str = None, model: str = None):
        """
        初始化
        :param api_key: API密钥,默认从环境变量读取
        :param api_base: API基础URL,默认从环境变量读取
        :param model: 模型名称,默认从环境变量读取
        """
        # 兼容多种环境变量名称
        self.api_key = api_key or os.getenv("OPENAI_API_KEY") or os.getenv("DEEPSEEK_API_KEY")
        self.api_base = api_base or os.getenv("OPENAI_BASE_URL") or "https://api.deepseek.com"
        self.model = model or os.getenv("OPENAI_MODEL") or "deepseek-chat"
        
    def analyze_dialogue(self, text: str) -> Dict[str, Any]:
        """
        分析对话文本,返回结构化结果
        :param text: 原始对话文本
        :return: 分析结果字典
        """
        prompt = self._build_prompt(text)
        
        try:
            response = self._call_llm(prompt)
            result = self._parse_response(response)
            return result
        except Exception as e:
            print(f"AI分析失败: {e}")
            # 返回默认结构
            return self._get_default_structure(text)
    
    def _build_prompt(self, text: str) -> str:
        """构建提示词"""
        emotions_str = ", ".join(CHINESE_EMOTION_NAMES)
        
        return f"""你是一个对话分析专家。请分析下面的对话文本,识别说话人并推理每句话的参数。

对话文本:
{text}

请按照以下JSON格式返回分析结果(只返回JSON,不要其他内容):

{{
  "speakers": [
    {{
      "id": "speaker_1",
      "name": "说话人A",
      "gender": "male/female/child",
      "age_group": "child/teenager/adult/elder"
    }}
  ],
  "dialogues": [
    {{
      "speaker_id": "speaker_1",
      "text": "具体对话内容",
      "emotion": "情感标签(必须从列表中选择)",
      "context": "前一句对话内容(如果有)"
    }}
  ]
}}

要求:
1. 识别2-3个说话人
2. 为每个说话人分配性别和年龄段
3. 分离每一句对话
4. 为每句话推理情感(只能从这些选项中选: {emotions_str})
5. context是前一个人说的话,用于TTS上下文理解
6. 如果文本没有标记说话人,请根据内容智能推断

只返回JSON,不要任何解释文字。"""

    def _call_llm(self, prompt: str) -> str:
        """调用LLM API"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "你是一个专业的对话分析助手,只返回JSON格式的结果。"},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "response_format": {"type": "json_object"}
        }
        
        response = requests.post(
            f"{self.api_base}/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        response.raise_for_status()
        
        result = response.json()
        return result["choices"][0]["message"]["content"]
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        """解析LLM返回的JSON"""
        try:
            data = json.loads(response)
            
            # 验证和修正数据
            if "speakers" not in data or "dialogues" not in data:
                raise ValueError("返回格式不正确")
            
            # 为说话人分配音色
            for speaker in data["speakers"]:
                gender = speaker.get("gender", "male")
                age = speaker.get("age_group", "adult")
                
                if age == "child":
                    voice_key = f"{gender}_child"
                else:
                    voice_key = f"{gender}_adult"
                
                # 使用辅助函数获取音色
                speaker["voice_type"] = get_voice_type(gender, age)
            
            # 验证情感标签
            for dialogue in data["dialogues"]:
                emotion = dialogue.get("emotion")
                if emotion and emotion not in CHINESE_EMOTION_NAMES:
                    dialogue["emotion"] = "中性"  # 默认情感
                    
            return data
            
        except json.JSONDecodeError as e:
            print(f"JSON解析失败: {e}")
            raise
    
    def _get_default_structure(self, text: str) -> Dict[str, Any]:
        """当AI分析失败时,返回默认结构"""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        return {
            "speakers": [
                {
                    "id": "speaker_1",
                    "name": "说话人A",
                    "gender": "male",
                    "age_group": "adult",
                    "voice_type": get_voice_type("male", "adult")
                },
                {
                    "id": "speaker_2", 
                    "name": "说话人B",
                    "gender": "female",
                    "age_group": "adult",
                    "voice_type": get_voice_type("female", "adult")
                }
            ],
            "dialogues": [
                {
                    "speaker_id": f"speaker_{i % 2 + 1}",
                    "text": line,
                    "emotion": "中性",
                    "context": lines[i-1] if i > 0 else None
                }
                for i, line in enumerate(lines)
            ]
        }


if __name__ == "__main__":
    # 测试
    analyzer = DialogueAnalyzer()
    
    test_text = """
    你好,最近怎么样?
    挺好的,就是工作有点累。
    那要注意休息啊!
    """
    
    result = analyzer.analyze_dialogue(test_text)
    print(json.dumps(result, ensure_ascii=False, indent=2))
