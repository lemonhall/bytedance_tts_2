"""
对话编辑器Web服务 - FastAPI后端
"""
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from project_schema import DialogueProject, Speaker, DialogueLine, CHINESE_EMOTIONS, ENGLISH_EMOTIONS, VOICE_TYPES
from ai_analyzer import DialogueAnalyzer
from tts_generator import TTSGenerator
from tts_config import (
    VOICE_TYPE_DETAILS, 
    VOICE_TYPES_BY_CATEGORY, 
    TTS_PARAM_RANGES,
    get_all_voice_categories
)


# 项目存储目录
PROJECTS_DIR = Path("projects")
PROJECTS_DIR.mkdir(exist_ok=True)

# 全局实例
analyzer = None
tts_generator = None


# 生命周期管理
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时初始化
    global analyzer, tts_generator
    try:
        analyzer = DialogueAnalyzer()
        tts_generator = TTSGenerator()
        print("✅ 服务初始化成功")
    except Exception as e:
        print(f"⚠️ 初始化警告: {e}")
    
    yield
    
    # 关闭时清理（如果需要）
    print("👋 服务关闭")


# 初始化FastAPI应用
app = FastAPI(title="对话TTS编辑器", version="1.0.0", lifespan=lifespan)


# 请求/响应模型
class AnalyzeRequest(BaseModel):
    text: str


class GenerateLineRequest(BaseModel):
    project_id: str
    line_id: str


class UpdateLineRequest(BaseModel):
    project_id: str
    line_id: str
    updates: dict


# API路由

@app.get("/")
async def root():
    """返回主页"""
    return FileResponse("static/index.html")


@app.get("/api/config")
async def get_config():
    """获取配置信息(情感列表、音色列表等)"""
    return {
        "emotions": {
            "chinese": CHINESE_EMOTIONS,
            "english": ENGLISH_EMOTIONS
        },
        "voice_types": VOICE_TYPES,
        "voice_details": VOICE_TYPE_DETAILS,
        "voice_categories": get_all_voice_categories(),
        "voices_by_category": VOICE_TYPES_BY_CATEGORY,
        "tts_params": TTS_PARAM_RANGES
    }


@app.post("/api/analyze")
async def analyze_text(request: AnalyzeRequest):
    """分析对话文本"""
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="文本不能为空")
    
    try:
        # 使用AI分析
        if analyzer:
            result = analyzer.analyze_dialogue(request.text)
        else:
            # 如果AI不可用,使用默认分析
            result = analyzer._get_default_structure(request.text) if analyzer else {}
        
        # 创建工程对象
        project_id = str(uuid.uuid4())
        now = datetime.now().isoformat()
        
        speakers = [
            Speaker(
                id=s["id"],
                name=s.get("name", "未命名"),
                gender=s["gender"],
                age_group=s.get("age_group", "adult"),
                voice_type=s["voice_type"]
            )
            for s in result.get("speakers", [])
        ]
        
        dialogues = [
            DialogueLine(
                id=f"line_{i}",
                speaker_id=d["speaker_id"],
                text=d["text"],
                emotion=d.get("emotion"),
                context=d.get("context")
            )
            for i, d in enumerate(result.get("dialogues", []))
        ]
        
        project = DialogueProject(
            title=f"对话_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            original_text=request.text,
            speakers=speakers,
            dialogues=dialogues,
            created_at=now,
            updated_at=now
        )
        
        # 保存工程文件
        project_file = PROJECTS_DIR / f"{project_id}.json"
        with open(project_file, "w", encoding="utf-8") as f:
            json.dump(project.model_dump(), f, ensure_ascii=False, indent=2)
        
        return {
            "project_id": project_id,
            "project": project.model_dump()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析失败: {str(e)}")


@app.get("/api/projects/{project_id}")
async def get_project(project_id: str):
    """获取工程详情"""
    project_file = PROJECTS_DIR / f"{project_id}.json"
    
    if not project_file.exists():
        raise HTTPException(status_code=404, detail="工程不存在")
    
    with open(project_file, "r", encoding="utf-8") as f:
        project_data = json.load(f)
    
    return project_data


@app.put("/api/projects/{project_id}/line/{line_id}")
async def update_line(project_id: str, line_id: str, updates: dict = Body(...)):
    """更新单句对话参数"""
    project_file = PROJECTS_DIR / f"{project_id}.json"
    
    if not project_file.exists():
        raise HTTPException(status_code=404, detail="工程不存在")
    
    # 读取工程
    with open(project_file, "r", encoding="utf-8") as f:
        project_data = json.load(f)
    
    # 查找并更新对话行
    found = False
    for dialogue in project_data["dialogues"]:
        if dialogue["id"] == line_id:
            dialogue.update(updates)
            found = True
            break
    
    if not found:
        raise HTTPException(status_code=404, detail="对话行不存在")
    
    # 更新时间戳
    project_data["updated_at"] = datetime.now().isoformat()
    
    # 保存
    with open(project_file, "w", encoding="utf-8") as f:
        json.dump(project_data, f, ensure_ascii=False, indent=2)
    
    return {"success": True, "message": "更新成功"}


@app.post("/api/projects/{project_id}/generate")
async def generate_project(project_id: str):
    """生成整个工程的音频"""
    project_file = PROJECTS_DIR / f"{project_id}.json"
    
    if not project_file.exists():
        raise HTTPException(status_code=404, detail="工程不存在")
    
    try:
        # 读取工程
        with open(project_file, "r", encoding="utf-8") as f:
            project_data = json.load(f)
        
        project = DialogueProject(**project_data)
        
        # 生成音频
        if not tts_generator:
            raise HTTPException(status_code=503, detail="TTS服务未初始化")
        
        audio_files = tts_generator.generate_project(project)
        
        if not audio_files:
            raise HTTPException(status_code=500, detail="音频生成失败")
        
        # 合并音频
        output_file = f"dialogue_output/{project_id}_final.wav"
        success = tts_generator.merge_audio_files(audio_files, output_file)
        
        if success:
            # 更新工程文件
            project.output_audio = output_file
            project.updated_at = datetime.now().isoformat()
            
            with open(project_file, "w", encoding="utf-8") as f:
                json.dump(project.model_dump(), f, ensure_ascii=False, indent=2)
            
            return {
                "success": True,
                "audio_url": f"/audio/{project_id}_final.wav",
                "message": "生成成功"
            }
        else:
            raise HTTPException(status_code=500, detail="音频合并失败")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成失败: {str(e)}")


@app.post("/api/projects/{project_id}/generate-line/{line_id}")
async def generate_single_line(project_id: str, line_id: str):
    """重新生成单句对话"""
    project_file = PROJECTS_DIR / f"{project_id}.json"
    
    if not project_file.exists():
        raise HTTPException(status_code=404, detail="工程不存在")
    
    try:
        # 读取工程
        with open(project_file, "r", encoding="utf-8") as f:
            project_data = json.load(f)
        
        project = DialogueProject(**project_data)
        
        # 查找对话行
        dialogue = None
        line_index = -1
        for i, d in enumerate(project.dialogues):
            if d.id == line_id:
                dialogue = d
                line_index = i
                break
        
        if not dialogue:
            raise HTTPException(status_code=404, detail="对话行不存在")
        
        # 查找说话人音色
        voice_type = None
        for speaker in project.speakers:
            if speaker.id == dialogue.speaker_id:
                voice_type = speaker.voice_type
                break
        
        if not voice_type:
            raise HTTPException(status_code=400, detail="未找到说话人音色")
        
        # 生成音频
        if not tts_generator:
            raise HTTPException(status_code=503, detail="TTS服务未初始化")
        
        audio_file = tts_generator.generate_line(dialogue, voice_type, line_index)
        
        if audio_file:
            # 更新工程文件
            dialogue.audio_file = audio_file
            project.updated_at = datetime.now().isoformat()
            
            with open(project_file, "w", encoding="utf-8") as f:
                json.dump(project.model_dump(), f, ensure_ascii=False, indent=2)
            
            return {
                "success": True,
                "audio_url": f"/audio/{Path(audio_file).name}",
                "message": "生成成功"
            }
        else:
            raise HTTPException(status_code=500, detail="音频生成失败")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成失败: {str(e)}")


@app.get("/api/projects")
async def list_projects():
    """列出所有工程"""
    projects = []
    for project_file in PROJECTS_DIR.glob("*.json"):
        try:
            with open(project_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                projects.append({
                    "id": project_file.stem,
                    "title": data.get("title", "未命名"),
                    "created_at": data.get("created_at"),
                    "updated_at": data.get("updated_at")
                })
        except:
            continue
    
    # 按更新时间倒序排列
    projects.sort(key=lambda x: x.get("updated_at", ""), reverse=True)
    return {"projects": projects}


# 静态文件服务
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/audio", StaticFiles(directory="dialogue_output"), name="audio")


if __name__ == "__main__":
    import uvicorn
    print("🚀 启动对话TTS编辑器服务...")
    print("📍 访问: http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
