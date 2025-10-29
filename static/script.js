// 配置 - 使用相对路径
const API_BASE_URL = '';

// DOM元素
const uploadForm = document.getElementById('uploadForm');
const audioFile = document.getElementById('audioFile');
const uploadBtn = document.getElementById('uploadBtn');
const resultDiv = document.getElementById('result');
const progressDiv = document.getElementById('progress');
const progressBar = document.getElementById('progressBar');

// 上传处理
if (uploadForm) {
    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const file = audioFile.files[0];
        if (!file) {
            showError('请选择音频文件');
            return;
        }
        
        // 文件大小检查
        if (file.size > 50 * 1024 * 1024) {
            showError('文件太大，请选择小于50MB的音频文件');
            return;
        }
        
        // 文件类型检查
        const allowedTypes = ['audio/mp3', 'audio/wav', 'audio/mpeg', 'audio/m4a', 'audio/ogg'];
        if (!allowedTypes.includes(file.type) && !file.name.toLowerCase().match(/\.(mp3|wav|m4a|ogg)$/)) {
            showError('请选择音频文件 (MP3, WAV, M4A, OGG 格式)');
            return;
        }
        
        await uploadAudio(file);
    });
}

async function uploadAudio(file) {
    try {
        showProgress(0, '准备上传...');
        uploadBtn.disabled = true;
        
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch('/api/upload-audio', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const data = await response.json();
            showResult(data);
        } else {
            let errorMsg = '上传失败';
            if (response.status === 413) {
                errorMsg = '文件太大，请选择小于50MB的文件';
            } else {
                try {
                    const errorData = await response.json();
                    errorMsg = errorData.detail || errorMsg;
                } catch (e) {
                    errorMsg = `服务器错误: ${response.status}`;
                }
            }
            showError(errorMsg);
        }
        
    } catch (error) {
        console.error('上传错误:', error);
        showError(`网络错误: ${error.message}`);
    } finally {
        uploadBtn.disabled = false;
    }
}

function showProgress(percent, message) {
    if (progressDiv && progressBar) {
        progressDiv.style.display = 'block';
        progressBar.style.width = `${percent}%`;
        progressBar.textContent = message;
        if (resultDiv) resultDiv.style.display = 'none';
    }
}

function showResult(data) {
    if (progressDiv) progressDiv.style.display = 'none';
    if (resultDiv) {
        resultDiv.style.display = 'block';
        resultDiv.innerHTML = `
            <div class="success-message">
                <h3>✅ 上传成功！</h3>
                <p><strong>文件名:</strong> ${data.filename}</p>
                <p><strong>文件大小:</strong> ${(data.size / 1024 / 1024).toFixed(2)} MB</p>
                <div class="analysis-result">
                    <h4>🎵 分析结果</h4>
                    <p><strong>综合评分:</strong> ${data.analysis.score}/100</p>
                    <p><strong>反馈:</strong> ${data.analysis.feedback}</p>
                    <div class="details">
                        <h5>详细分析:</h5>
                        <ul>
                            <li>音准准确率: ${data.analysis.details.pitch_accuracy}</li>
                            <li>节奏稳定性: ${data.analysis.details.rhythm_stability}</li>
                            <li>音域范围: ${data.analysis.details.vocal_range}</li>
                        </ul>
                        <h5>改进建议:</h5>
                        <ul>
                            ${data.analysis.details.recommendations.map(rec => `<li>${rec}</li>`).join('')}
                        </ul>
                    </div>
                </div>
            </div>
        `;
    }
}

function showError(message) {
    if (progressDiv) progressDiv.style.display = 'none';
    if (resultDiv) {
        resultDiv.style.display = 'block';
        resultDiv.innerHTML = `
            <div class="error-message">
                <h3>❌ 上传失败</h3>
                <p>${message}</p>
                <button onclick="retryUpload()">重新上传</button>
            </div>
        `;
    }
}

function retryUpload() {
    if (resultDiv) resultDiv.style.display = 'none';
    if (audioFile) audioFile.value = '';
}
