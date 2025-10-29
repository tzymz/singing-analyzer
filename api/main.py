from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import aiofiles
import os
import uuid
from typing import Optional
import tempfile

# 创建FastAPI应用
app = FastAPI(title="AI唱歌分析API")

# 重要：CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "AI唱歌分析API服务运行中"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "AI唱歌分析API"}

@app.post("/api/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    try:
        print(f"开始处理文件: {file.filename}")
        
        # 检查文件类型
        allowed_extensions = ['.mp3', '.wav', '.m4a', '.ogg', '.mpeg']
        file_ext = os.path.splitext(file.filename.lower())[1]
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"不支持的文件格式 {file_ext}，请上传MP3、WAV、M4A格式"
            )
        
        # 读取文件内容并检查大小
        content = await file.read()
        file_size = len(content)
        print(f"文件大小: {file_size} bytes")
        
        # 50MB限制
        if file_size > 50 * 1024 * 1024:
            raise HTTPException(
                status_code=413, 
                detail=f"文件太大 ({file_size/1024/1024:.1f}MB)，请选择小于50MB的文件"
            )
        
        # 生成唯一文件名
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        
        # 保存文件到临时目录
        temp_file_path = os.path.join(tempfile.gettempdir(), unique_filename)
        
        async with aiofiles.open(temp_file_path, 'wb') as temp_file:
            await temp_file.write(content)
        
        print(f"文件已保存到: {temp_file_path}")
        
        # 这里可以添加您的音频处理逻辑
        # 例如调用阿里云OSS和FunASR服务
        
        # 模拟处理结果
        analysis_result = {
            "status": "success",
            "score": 85,
            "feedback": "音准良好，节奏稳定，建议加强情感表达",
            "details": {
                "pitch_accuracy": "82%",
                "rhythm_stability": "88%",
                "vocal_range": "C3-G5",
                "recommendations": ["练习气息控制", "注意尾音处理"]
            }
        }
        
        return JSONResponse({
            "status": "success",
            "message": "文件上传和分析成功",
            "filename": file.filename,
            "size": file_size,
            "analysis": analysis_result
        })
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"上传错误: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": f"文件处理失败: {str(e)}"
            }
        )

# Vercel需要这个handler
handler = app
