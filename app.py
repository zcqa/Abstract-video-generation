import os
import uuid
from flask import Flask, request, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename
from processing import generate_video

# 初始化 Flask 应用
app = Flask(__name__)

# 配置上传和输出文件夹
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# 确保文件夹存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# 允许的文件扩展名
ALLOWED_EXTENSIONS_IMG = {'png', 'jpg', 'jpeg'}
ALLOWED_EXTENSIONS_AUDIO = {'mp3', 'wav'}

def allowed_file(filename, allowed_extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

@app.route('/')
def index():
    """渲染主页面"""
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_files():
    """接收文件，调用处理逻辑，并返回视频URL"""
    if 'image' not in request.files or 'audio' not in request.files:
        return jsonify({'error': '缺少图片或音频文件'}), 400

    image_file = request.files['image']
    audio_file = request.files['audio']

    if image_file.filename == '' or audio_file.filename == '':
        return jsonify({'error': '未选择文件'}), 400

    if not (allowed_file(image_file.filename, ALLOWED_EXTENSIONS_IMG) and \
            allowed_file(audio_file.filename, ALLOWED_EXTENSIONS_AUDIO)):
        return jsonify({'error': '文件类型不支持'}), 400

    # 生成安全且唯一的文件名
    image_ext = image_file.filename.rsplit('.', 1)[1].lower()
    audio_ext = audio_file.filename.rsplit('.', 1)[1].lower()
    unique_id = str(uuid.uuid4())
    
    image_filename = f"{unique_id}.{image_ext}"
    audio_filename = f"{unique_id}.{audio_ext}"
    output_filename = f"{unique_id}.mp4"

    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
    audio_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_filename)
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

    # 保存上传的文件
    image_file.save(image_path)
    audio_file.save(audio_path)

    try:
        # 调用核心处理函数
        generate_video(image_path, audio_path, output_path)
        
        # 返回成功信息和下载链接
        return jsonify({
            'status': 'success',
            'video_url': f'/download/{output_filename}'
        })
    except Exception as e:
        # 记录错误并返回错误信息
        print(f"处理过程中发生错误: {e}")
        return jsonify({'error': f'处理失败: {str(e)}'}), 500
    finally:
        # 清理上传的临时文件
        if os.path.exists(image_path):
            os.remove(image_path)
        if os.path.exists(audio_path):
            os.remove(audio_path)

@app.route('/download/<filename>')
def download_file(filename):
    """提供生成视频的下载"""
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    # 添加 use_reloader=False 参数
    app.run(debug=True, use_reloader=False)