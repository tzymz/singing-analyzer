import oss2
import uuid
import asyncio
from typing import Dict, Any, Optional
from app.core.config import settings

class CloudServiceManager:
    def __init__(self, settings):
        self.settings = settings
        self.fallback_mode = True
        
        print("🔄 正在初始化阿里云服务...")
        
        # OSS连接
        if (settings.ALIYUN_ACCESS_KEY_ID and 
            settings.ALIYUN_ACCESS_KEY_SECRET and
            "test" not in settings.ALIYUN_ACCESS_KEY_ID.lower()):
            
            try:
                print("📡 尝试连接阿里云OSS...")
                self.oss_auth = oss2.Auth(
                    settings.ALIYUN_ACCESS_KEY_ID,
                    settings.ALIYUN_ACCESS_KEY_SECRET
                )
                self.oss_bucket = oss2.Bucket(
                    self.oss_auth,
                    settings.ALIYUN_OSS_ENDPOINT,
                    settings.ALIYUN_OSS_BUCKET
                )
                
                # 测试连接
                bucket_info = self.oss_bucket.get_bucket_info()
                self.fallback_mode = False
                print(f"✅ 阿里云OSS连接成功！")
                
                # 初始化ASR服务
                if hasattr(settings, 'ALIYUN_ASR_API_KEY') and settings.ALIYUN_ASR_API_KEY:
                    from app.core.real_asr_service import RealASRService
                    self.asr_service = RealASRService(api_key=settings.ALIYUN_ASR_API_KEY)
                    print("🎤 Fun-ASR服务初始化完成 - 准备真实AI分析")
                else:
                    print("⚠️ 未找到ASR API Key，使用模拟模式")
                
            except Exception as e:
                print(f"❌ 连接失败: {e}")
        else:
            print("ℹ️ 使用模拟模式运行")
    
    async def upload_audio(self, audio_data: bytes) -> str:
        """上传音频到OSS并返回签名URL（自动压缩优化）"""
        if self.fallback_mode:
            print(f"📤 模拟上传音频，大小: {len(audio_data)} 字节")
            return f"https://example.com/audio-{uuid.uuid4()}.wav"
        else:
            try:
                print(f"📦 原始音频大小: {len(audio_data)} 字节 ({len(audio_data)/1024/1024:.1f} MB)")
                
                # 音频预处理：转换为WAV并压缩
                processed_data = await self._preprocess_audio(audio_data)
                
                file_name = f"audios/{uuid.uuid4()}.wav"
                print(f"📤 正在上传到阿里云OSS: {file_name}")
                
                # 上传到OSS
                result = self.oss_bucket.put_object(file_name, processed_data)
                if result.status == 200:
                    # 生成签名URL（1小时有效期）
                    signed_url = self.oss_bucket.sign_url('GET', file_name, 3600)
                    print("✅ 上传成功，生成签名URL")
                    return signed_url
                else:
                    raise Exception(f"OSS上传失败: {result.status}")
                    
            except Exception as e:
                print(f"❌ 上传失败: {e}")
                # 回退到模拟模式
                return f"https://example.com/audio-{uuid.uuid4()}.wav"
    
    async def analyze_singing(self, audio_url: str) -> Dict[str, Any]:
        """分析唱歌音频"""
        if self.fallback_mode or not hasattr(self, 'asr_service'):
            print("🔄 使用模拟分析")
            return await self._simulate_analysis()
        else:
            try:
                print(f"🔍 开始真实AI分析: {audio_url}")
                result = await self.asr_service.analyze_singing(audio_url)
                return result
            except Exception as e:
                print(f"❌ 真实API分析失败: {e}")
                print("🔄 回退到增强模拟分析")
                return await self._simulate_analysis()
    
    async def _preprocess_audio(self, audio_data: bytes) -> bytes:
        """高质量音频预处理（使用ffmpeg）"""
        try:
            print("🔧 开始高质量音频预处理...")
            
            from pydub import AudioSegment
            import io
            
            # 从字节数据创建音频对象
            audio = AudioSegment.from_file(io.BytesIO(audio_data))
            
            print(f"🎵 原始音频信息: {len(audio)/1000:.1f}秒, {audio.channels}声道, {audio.frame_rate}Hz")
            
            # 如果音频过长，截取前45秒
            max_duration = 45 * 1000  # 45秒
            if len(audio) > max_duration:
                print(f"⏰ 音频过长 ({len(audio)/1000:.1f}秒)，截取前45秒")
                audio = audio[:max_duration]
            
            # 优化设置（语音识别最佳参数）
            audio = audio.set_frame_rate(16000)  # 16kHz
            audio = audio.set_channels(1)        # 单声道
            audio = audio.set_sample_width(2)    # 16位
            
            # 导出为WAV格式
            buffer = io.BytesIO()
            audio.export(buffer, format="wav")
            processed_data = buffer.getvalue()
            
            print(f"✅ 预处理完成: {len(processed_data)} 字节 ({len(processed_data)/1024/1024:.1f} MB)")
            print(f"📊 压缩率: {len(audio_data)/len(processed_data)*100:.1f}%, 时长: {len(audio)/1000:.1f}秒")
            
            return processed_data
            
        except Exception as e:
            print(f"⚠️ 高质量预处理失败: {e}")
            print("🔄 使用原始数据继续处理...")
            return audio_data
    
    async def _simulate_analysis(self) -> Dict[str, Any]:
        """模拟分析（回退方案）"""
        print("🔄 使用增强模拟分析")
        
        # 模拟分析结果
        return {
            "transcription": {
                "text": "模拟转写结果：这是一段测试音频",
                "confidence": 0.85,
                "source": "simulated"
            },
            "analysis": {
                "score": 82,
                "feedback": "🎵 模拟分析完成 - 音准良好，节奏稳定",
                "details": [
                    {"aspect": "音准", "score": 85, "comment": "音准表现优秀"},
                    {"aspect": "节奏", "score": 80, "comment": "节奏感良好"},
                    {"aspect": "音色", "score": 79, "comment": "音色温暖自然"}
                ],
                "source": "simulated"
            },
            "source": "simulated"
        }
