# 抽象视频视频生成器

本项目完全由ai生成，包括该文档

这是一个 Web 应用程序，允许用户上传一张图片和一个音频文件，服务器会自动分析音频的旋律特征，生成一个图像根据旋律进行“挤压与拉伸”(Squash & Stretch)的动态视频。

。

## 🎬 项目演示


![alt text](966d1bba-0665-4b35-bad3-a7819692caf0.gif)

*最终生成的视频效果示例*

## 📁 文件结构

```
music-video-generator/
├── app.py              # Flask 主应用
├── processing.py         # 核心处理逻辑 (音频分析与视频合成)
├── requirements.txt      # 项目依赖
├── static/
│   └── js/
│       └── script.js     # 前端 JavaScript
├── templates/
│   └── index.html      # 前端 HTML 页面
├── uploads/              # (需手动创建) 存储用户上传的临时文件
├── outputs/              # (需手动创建) 存储生成的视频文件
└── README.md             # 本文档
```

## ⚙️ 环境要求

- Python 3.7+
- pip 包管理器

### 关键依赖：FFmpeg

本项目使用 `librosa` 和 `moviepy` 库，它们都需要 **FFmpeg** 来处理音频和视频文件。**你必须在你的系统上安装 FFmpeg**，否则程序会在分析音频时卡住。

- **Windows 用户**:
  - **推荐**: 使用 [Chocolatey](https://chocolatey.org/) 包管理器:
    ```bash
    choco install ffmpeg
    ```
  - **手动安装**: 前往 [FFmpeg官网下载](https://ffmpeg.org/download.html)，解压后将其 `bin` 目录添加到系统的 `Path` 环境变量中。

- **macOS 用户**:
  - 使用 [Homebrew](https://brew.sh/):
    ```bash
    brew install ffmpeg
    ```

- **Linux (Debian/Ubuntu) 用户**:
  ```bash
  sudo apt update
  sudo apt install ffmpeg
  ```

**验证安装**: 打开一个新的终端窗口，输入 `ffmpeg -version`，如果能看到版本信息，则表示安装成功。

## 🚀 安装与设置


1.  **创建并激活虚拟环境 (推荐)**
    这可以避免与你系统中的其他Python包产生冲突。
    
    - **Windows**:
      ```bash
      python -m venv venv
      .\venv\Scripts\activate
      ```
    - **macOS / Linux**:
      ```bash
      python3 -m venv venv
      source venv/bin/activate
      ```

2.  **创建 `requirements.txt` 文件**
    在项目根目录下创建一个名为 `requirements.txt` 的文件，并将以下内容复制进去。注意，我们指定了 `moviepy` 的版本为 `1.0.3`。
    
    ```txt
    Flask
    librosa
    opencv-python
    numpy
    moviepy==1.0.3
    soundfile
    ```

3.  **安装Python依赖**
    在已激活虚拟环境的终端中，运行以下命令：
    ```bash
    pip install -r requirements.txt
    ```

4.  **创建必要文件夹**
    在项目根目录下，手动创建两个空文件夹：
    - `uploads`
    - `outputs`

## 🏃 运行项目

1.  确保你的终端位于项目根目录，并且虚拟环境已经激活。
2.  运行以下命令启动Flask服务器：
    ```bash
    python app.py
    ```
3.  如果一切正常，你会在终端看到类似以下的输出：
    ```
     * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
    ```

## 📝 如何使用

1.  打开你的网页浏览器，访问 `http://127.0.0.1:5000/`。
2.  点击“选择文件”按钮，上传一张你想要制作动画的图片 (JPG, PNG)。
3.  点击第二个“选择文件”按钮，上传驱动动画的音频文件 (MP3, WAV)。
4.  点击“开始处理”按钮。
5.  等待处理完成。处理时间取决于音频的长度，请耐心等候。
6.  处理成功后，页面上会出现一个“点击下载视频”的链接，点击即可下载生成的MP4视频。

## 🔧 效果自定义

你可以通过修改 `processing.py` 文件开头的参数来调整动画的视觉风格，无需改动其他代码。

```python
# --- processing.py 文件开头的参数设置 ---
base_scale = 0.5         # 基础缩放比例 (静止时图片是原始大小的0.5倍)
max_scale = 2.0          # 允许的最大缩放比例 (节拍最强时可达2倍)
smoothing_factor = 0.15    # 平滑因子 (值越小动画越"柔软"，越大越"清脆")
beat_effect_duration = 0.3 # 每个事件效果的持续时间（秒）

# ... 在 onset_strength 之后 ...
# delta 值决定了旋律检测的灵敏度
event_frames = librosa.util.peak_pick(onset_env, ..., delta=0.2, ...)
```
- `base_scale`: 调整图片在无事件时的默认大小。
- `max_scale`: 调整图片在事件峰值时的最大尺寸。
- `smoothing_factor`: 调整动画的“弹性”感。
- `delta`: 调整旋律检测的灵敏度。**减小**此值可捕捉更多细微音符，**增大**则只对主要音符有反应。

