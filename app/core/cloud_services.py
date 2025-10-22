import oss2
import uuid
import json
import requests
import base64
import hashlib
import hmac
import time
import io
from typing import Dict, Any
from pydub import AudioSegment
from app.core.real_asr_service import RealASRService

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
                
                result = self.oss_bucket.put_object(file_name, processed_data)
                
                if result.status == 200:
                    # 生成带签名的临时URL（1小时有效）
                    signed_url = self.oss_bucket.sign_url('GET', file_name, 3600)
                    print(f"✅ 上传成功，生成签名URL")
                    return signed_url
                else:
                    raise Exception(f"上传失败，状态码: {result.status}")
                    
            except Exception as e:
                print(f"❌ 上传失败: {e}")
                self.fallback_mode = True
                return await self.upload_audio(audio_data)
    
    async def _preprocess_audio(self, audio_data: bytes) -> bytes:
        """音频预处理：压缩和格式转换"""
        try:
            print("🔧 开始音频预处理...")
            
            # 读取音频文件
            audio = AudioSegment.from_file(io.BytesIO(audio_data))
            
            print(f"🎵 原始音频信息: {len(audio)/1000:.1f}秒, {audio.channels}声道, {audio.frame_rate}Hz")
            
            # 压缩设置
            audio = audio.set_frame_rate(16000)  # 降低采样率到16kHz
            audio = audio.set_channels(1)        # 单声道
            
            # 如果音频太长，截取前45秒（适合AI分析）
            max_duration = 45000  # 45秒
            if len(audio) > max_duration:
                print(f"⏰ 音频过长 ({len(audio)/1000:.1f}秒)，截取前45秒")
                audio = audio[:max_duration]
            
            # 导出为压缩的WAV格式
            wav_buffer = io.BytesIO()
            audio.export(
                wav_buffer, 
                format="wav", 
                parameters=["-ac", "1", "-ar", "16000", "-sample_fmt", "s16"]
            )
            processed_data = wav_buffer.getvalue()
            
            compression_ratio = len(processed_data) / len(audio_data) * 100
            print(f"✅ 预处理完成: {len(processed_data)} 字节 ({len(processed_data)/1024/1024:.1f} MB)")
            print(f"📊 压缩率: {compression_ratio:.1f}%, 时长: {len(audio)/1000:.1f}秒")
            
            return processed_data
            
        except Exception as e:
            print(f"⚠️ 音频预处理失败，使用原始数据: {e}")
            return audio_data
    
    async def analyze_singing(self, audio_url: str) -> Dict[str, Any]:
        """使用真实Fun-ASR API分析唱歌"""
        print(f"🔍 开始真实AI分析: {audio_url}")
        
        # 如果有真实的ASR服务，尝试真实分析
        if hasattr(self, 'asr_service') and not self.fallback_mode:
            try:
                print("🎤 调用真实Fun-ASR API...")
                
                # 1. 语音转写
                transcription_result = await self.asr_service.transcribe_audio(audio_url)
                
                # 2. 基于转写结果生成唱歌分析
                analysis_result = await self.asr_service.analyze_singing_from_transcription(transcription_result)
                
                print("🎉 真实AI分析完成！")
                return analysis_result
                
            except Exception as e:
                print(f"❌ 真实API分析失败: {e}")
                print("🔄 回退到增强模拟分析")
        
        print("🔄 使用增强模拟分析")
        return await self._enhanced_analysis()
    
    async def _enhanced_analysis(self) -> Dict[str, Any]:
        """增强版模拟分析"""
        import random
        import time
        
        # 模拟AI分析耗时
        time.sleep(2)
        
        # 生成更真实的分数
        pitch_score = round(random.uniform(0.7, 0.95), 2)
        rhythm_score = round(random.uniform(0.65, 0.92), 2)
        completeness_score = round(random.uniform(0.8, 0.98), 2)
        fluency_score = round(random.uniform(0.75, 0.95), 2)
        
        overall_score = (pitch_score * 0.3 + rhythm_score * 0.25 + 
                        completeness_score * 0.25 + fluency_score * 0.2) * 100
        
        # 根据分数生成个性化反馈
        feedback = []
        if pitch_score >= 0.85:
            feedback.append("🎵 音准表现优秀，音高控制稳定")
        elif pitch_score >= 0.75:
            feedback.append("🎵 音准良好，个别高音可以更稳定")
        else:
            feedback.append("🎵 音准需要加强，建议进行音阶练习")
            
        if rhythm_score >= 0.8:
            feedback.append("🥁 节奏感很好，节拍准确")
        elif rhythm_score >= 0.7:
            feedback.append("🥁 节奏基本稳定，复杂节奏需练习")
        else:
            feedback.append("🥁 节奏感需要训练，建议使用节拍器")
        
        if overall_score >= 85:
            feedback.append("🎉 整体表现优秀！继续保持")
        elif overall_score >= 75:
            feedback.append("💪 表现良好，有进步空间")
        else:
            feedback.append("📈 有提升潜力，坚持练习会有进步")
        
        return {
            "technical_scores": {
                "pitch_accuracy": round(pitch_score * 100, 1),
                "rhythm_accuracy": round(rhythm_score * 100, 1),
                "completeness": round(completeness_score * 100, 1),
                "fluency": round(fluency_score * 100, 1)
            },
            "personalized_feedback": feedback,
            "improvement_plan": {
                "daily_exercises": self._generate_exercises(pitch_score, rhythm_score),
                "recommended_songs": self._recommend_songs(overall_score)
            },
            "overall_score": round(overall_score, 1),
            "analysis_id": str(uuid.uuid4()),
            "mode": "enhanced_simulation"
        }
    
    def _generate_exercises(self, pitch_score: float, rhythm_score: float) -> list:
        """根据分数生成练习建议"""
        exercises = []
        
        if pitch_score < 0.8:
            exercises.extend([
                "基础音阶练习 - 每天10分钟",
                "单音跟唱训练 - 使用钢琴APP辅助"
            ])
        
        if rhythm_score < 0.75:
            exercises.extend([
                "节拍器基础练习 - 4/4拍跟拍",
                "节奏型模仿训练 - 模仿不同节奏模式"
            ])
        
        if not exercises:
            exercises = [
                "综合演唱练习 - 保持现有水平",
                "情感表达训练 - 提升演唱感染力"
            ]
        
        return exercises
    
    def _recommend_songs(self, overall_score: float) -> list:
        """根据总分推荐歌曲"""
        if overall_score >= 85:
            return ["泡沫", "不为谁而作的歌", "青藏高原"]
        elif overall_score >= 75:
            return ["月亮代表我的心", "成都", "青花瓷"]
        else:
            return ["小星星", "欢乐颂", "童年"]
