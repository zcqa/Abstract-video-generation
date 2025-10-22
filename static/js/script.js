document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('upload-form');
    const imageInput = document.getElementById('image-input');
    const audioInput = document.getElementById('audio-input');
    const submitBtn = document.getElementById('submit-btn');
    const statusDiv = document.getElementById('status');
    const resultDiv = document.getElementById('result');

    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const imageFile = imageInput.files[0];
        const audioFile = audioInput.files[0];

        if (!imageFile || !audioFile) {
            statusDiv.textContent = '请确保同时选择了图片和音频文件。';
            return;
        }

        const formData = new FormData();
        formData.append('image', imageFile);
        formData.append('audio', audioFile);

        // 更新UI，表示正在处理
        submitBtn.disabled = true;
        submitBtn.textContent = '正在处理中，请稍候...';
        statusDiv.textContent = '文件已上传，服务器正在生成视频。这可能需要几分钟时间，具体取决于音频长度。';
        resultDiv.innerHTML = '';

        try {
            const response = await fetch('/process', {
                method: 'POST',
                body: formData,
            });

            const data = await response.json();

            if (response.ok) {
                if (data.status === 'success') {
                    statusDiv.textContent = '视频生成成功！';
                    const downloadLink = document.createElement('a');
                    downloadLink.href = data.video_url;
                    downloadLink.textContent = '点击下载视频';
                    downloadLink.setAttribute('download', ''); // 提示浏览器下载
                    resultDiv.appendChild(downloadLink);
                } else {
                    // 处理后端返回的业务逻辑错误
                    statusDiv.textContent = `错误: ${data.error}`;
                }
            } else {
                // 处理HTTP错误
                statusDiv.textContent = `服务器错误: ${data.error || response.statusText}`;
            }

        } catch (error) {
            console.error('上传失败:', error);
            statusDiv.textContent = '上传或处理失败，请检查网络连接或联系管理员。';
        } finally {
            // 恢复按钮状态
            submitBtn.disabled = false;
            submitBtn.textContent = '开始处理';
        }
    });
});