# 音乐驱动的图像扭曲视频生成器

这是一个 Web 应用程序，允许用户上传一张图片和一个音频文件，服务器会自动分析音频的旋律特征，生成一个图像根据旋律进行“挤压与拉伸”(Squash & Stretch)的动态视频。

## ✨ 项目特色

- **简洁的Web界面**: 通过浏览器即可轻松上传文件并生成视频。
- **高级音频分析**: 采用**谐波-打击乐分离(HPSS)**技术，能精确地从音乐中分离出主旋律，并根据旋律的音符变化来驱动动画，而非简单的节拍。
- **生动的视觉效果**:
    - 实现经典的**挤压与拉伸**动画，视觉效果充满弹性。
    - **右下角锚点**缩放，符合常见Meme视频的风格。
    - **连续平滑动画**，效果自然不生硬。
- **高度可定制**: 核心处理脚本中的参数可以轻松调整，以改变动画的基础大小、最大幅度、平滑度等。

## 🎬 项目演示

（在这里可以放置一张展示最终效果的GIF动图）

![项目演示GIF](https://user-images.githubusercontent.com/path/to/your_demo.gif)

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

1.  **下载项目代码**
    ```bash
    git clone https://your-repository-url.git
    cd music-video-generator
    ```
    或者直接下载ZIP压缩包并解压。

2.  **创建并激活虚拟环境 (推荐)**
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

3.  **创建 `requirements.txt` 文件**
    在项目根目录下创建一个名为 `requirements.txt` 的文件，并将以下内容复制进去。注意，我们指定了 `moviepy` 的版本为 `1.0.3`。
    
    ```txt
    Flask
    librosa
    opencv-python
    numpy
    moviepy==1.0.3
    soundfile
    ```

4.  **安装Python依赖**
    在已激活虚拟环境的终端中，运行以下命令：
    ```bash
    pip install -r requirements.txt
    ```

5.  **创建必要文件夹**
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

## ❓ 常见问题排查

1.  **程序卡在 "正在分析音频..."**
    - **原因**: 99% 的可能是因为你没有安装 **FFmpeg**，或者没有将其正确添加到系统环境变量中。
    - **解决**: 请返回 `环境要求` 部分，确保 FFmpeg 已正确安装并可以被系统找到。

2.  **服务器在我上传文件后自动重启**
    - **原因**: 这是Flask的Debug模式下的自动重载(Reloader)功能导致的。它检测到 `librosa` 在处理音频时生成了缓存文件(`.pyc`)，误以为代码被修改，于是重启了服务，中断了视频生成过程。
    - **解决**: 打开 `app.py` 文件，找到最后一行 `app.run(debug=True)`，将其修改为 `app.run(debug=True, use_reloader=False)`，然后重启服务。