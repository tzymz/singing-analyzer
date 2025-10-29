from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional

from app.services.analysis_service import AnalysisService
from app.core.cloud_services import CloudServiceManager
from app.core.config import settings

router = APIRouter()

# 初始化服务
cloud_manager = CloudServiceManager(settings)
analysis_service = AnalysisService(cloud_manager)

@router.post("/analyze")
async def analyze_singing(
    audio_file: UploadFile = File(..., description="音频文件 (支持 wav, mp3)"),
    user_level: str = Form("beginner", description="用户水平: beginner, intermediate, advanced")
):
    """
    分析唱歌音频，返回详细报告
    """
    try:
        # 验证文件类型
        if not audio_file.content_type.startswith('audio/'):
            raise HTTPException(status_code=400, detail="请上传音频文件")
        
        # 读取文件
        audio_data = await audio_file.read()
        print(f"收到音频文件: {audio_file.filename}, 大小: {len(audio_data)} 字节")
        
        # 分析
        result = await analysis_service.comprehensive_analysis(audio_data, user_level)
        
        return {
            "success": True,
            "data": result,
            "message": "分析完成"
        }
        
    except Exception as e:
        print(f"分析错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"分析失败: {str(e)}")

@router.get("/")
async def root():
    return {"message": "AI唱歌分析API服务运行中"}

