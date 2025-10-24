from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import os
import sys

print("=== 应用启动日志 ===")
print(f"Python路径: {sys.path}")
print(f"工作目录: {os.getcwd()}")
print("环境变量:")
for key in ['ALIYUN_ACCESS_KEY_ID', 'ALIYUN_ASR_API_KEY']:
    value = os.getenv(key)
    print(f"  {key}: {'已设置' if value else '未设置'}")

app = FastAPI(title="AI唱歌分析")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态文件服务
static_dir = "static"
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    print("✅ 静态文件服务已挂载")
else:
    print("❌ 静态文件目录不存在")

@app.get("/")
async def root():
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    else:
        return JSONResponse({"message": "AI唱歌分析API", "status": "后端服务运行中"})

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "AI唱歌分析"}

@app.get("/debug")
async def debug():
    return {
        "status": "running",
        "static_files": os.path.exists("static/index.html"),
        "env_vars": {
            "ALIYUN_ACCESS_KEY_ID": bool(os.getenv('ALIYUN_ACCESS_KEY_ID')),
            "ALIYUN_ASR_API_KEY": bool(os.getenv('ALIYUN_ASR_API_KEY'))
        }
    }

# 尝试导入API路由
try:
    from app.api.endpoints import router as api_router
    app.include_router(api_router, prefix="/api/v1")
    print("✅ API路由注册成功")
except Exception as e:
    print(f"❌ API路由注册失败: {e}")
    
    @app.post("/api/v1/analyze")
    async def analyze_fallback():
        return {"status": "fallback", "message": "API服务准备中"}

print("🎉 应用启动完成")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
