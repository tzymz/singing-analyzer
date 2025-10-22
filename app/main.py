from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.core.config import settings
from app.api.endpoints import router as api_router

# 创建FastAPI应用
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI唱歌分析应用",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加静态文件服务
app.mount("/static", StaticFiles(directory="static"), name="static")

# 注册API路由
app.include_router(api_router, prefix=settings.API_V1_STR)

# 根路由返回首页
@app.get("/")
async def read_root():
    return FileResponse("static/index.html")

# 健康检查路由
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# 备用根路由（如果静态文件服务失败）
@app.get("/api")
async def root():
    return {
        "message": "欢迎使用AI唱歌分析API",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
