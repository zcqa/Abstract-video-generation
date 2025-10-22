import librosa
import numpy as np
import cv2
import moviepy.editor as mpe
import math

def generate_video(image_path, audio_path, output_path, fps=30):
    """
    通过“谐波-打击乐分离”技术，精确捕捉主旋律来驱动动画。
    - 基础缩放 0.5 倍，最大可达 2.0 倍。
    - 锚点为右下角，效果连续平滑。
    - 对旋律音符变化极为敏感。
    """
    # --- 参数设置 ---
    base_scale = 0.5
    max_scale = 2.0
    smoothing_factor = 0.15
    beat_effect_duration = 0.3
    
    max_stretch = max_scale - base_scale

    # 1. 音频分析 (采用HPSS高级技术)
    print("正在分析音频...")
    y, sr = librosa.load(audio_path, sr=None)
    duration = librosa.get_duration(y=y, sr=sr)
    
    # --- 核心改动：进行谐波-打击乐分离 ---
    print("正在分离谐波(旋律)与打击乐(节奏)...")
    y_harmonic, y_percussive = librosa.effects.hpss(y)
    
    # --- 现在，我们只在“谐波”部分寻找事件 ---
    print("正在从旋律部分提取音乐事件...")
    onset_env = librosa.onset.onset_strength(y=y_harmonic, sr=sr)
    
    # 从旋律的包络中挑选峰值点
    # 对于旋律，delta可以设置得更低，以捕捉更细微的音高变化
    event_frames = librosa.util.peak_pick(onset_env, pre_max=3, post_max=3, pre_avg=3, post_avg=5, delta=0.6, wait=4)
    
    event_times = librosa.frames_to_time(event_frames, sr=sr)
    print(f"从旋律中检测到 {len(event_times)} 个关键事件。")

    # 响度仍然使用原始音频，以反映整体能量
    rms = librosa.feature.rms(y=y, frame_length=2048, hop_length=512)[0]
    rms_normalized = (rms - np.min(rms)) / (np.max(rms) - np.min(rms) + 1e-6)

    # 2. 图像和视频设置
    print("正在设置图像和视频参数...")
    original_image = cv2.imread(image_path)
    h, w, _ = original_image.shape
    total_frames = int(duration * fps)
    
    frames = []
    current_scale_x = base_scale
    current_scale_y = base_scale

    print(f"开始生成 {total_frames} 帧视频...")
    for i in range(total_frames):
        current_time = i / float(fps)
        
        rms_frame_index = min(int(librosa.time_to_frames(current_time, sr=sr)), len(rms_normalized) - 1)
        loudness = rms_normalized[rms_frame_index]

        target_scale_x, target_scale_y = base_scale, base_scale

        current_event_index = np.searchsorted(event_times, current_time, side='right') - 1

        if current_event_index >= 0:
            time_since_event = current_time - event_times[current_event_index]
            if time_since_event < beat_effect_duration:
                decay_factor = (math.cos(time_since_event * math.pi / beat_effect_duration) + 1) / 2
                stretch_amount = max_stretch * loudness * decay_factor

                if (current_event_index + 1) % 2 != 0:
                    target_scale_y = base_scale + stretch_amount
                    target_scale_x = base_scale - stretch_amount * 0.5
                else:
                    target_scale_x = base_scale + stretch_amount
                    target_scale_y = base_scale - stretch_amount * 0.5
        
        current_scale_x += (target_scale_x - current_scale_x) * smoothing_factor
        current_scale_y += (target_scale_y - current_scale_y) * smoothing_factor
        
        current_scale_x = max(0.05, current_scale_x)
        current_scale_y = max(0.05, current_scale_y)
        
        # 3. 应用变换
        new_w = int(w * current_scale_x)
        new_h = int(h * current_scale_y)
        
        # 增加一个健壮性检查，防止尺寸变为0
        if new_w <= 0 or new_h <= 0:
            continue

        resized_frame = cv2.resize(original_image, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
        
        canvas = np.zeros((h, w, 3), dtype=np.uint8)
        x_offset, y_offset = w - new_w, h - new_h

        src_h, src_w, _ = resized_frame.shape
        dst_x_start, dst_y_start = max(0, x_offset), max(0, y_offset)
        dst_x_end, dst_y_end = min(w, x_offset + src_w), min(h, y_offset + src_h)

        src_x_start, src_y_start = max(0, -x_offset), max(0, -y_offset)
        src_x_end, src_y_end = src_x_start + (dst_x_end - dst_x_start), src_y_start + (dst_y_end - dst_y_start)
        
        if dst_x_end > dst_x_start and dst_y_end > dst_y_start:
            canvas[dst_y_start:dst_y_end, dst_x_start:dst_x_end] = \
                resized_frame[src_y_start:src_y_end, src_x_start:src_x_end]
        
        frames.append(cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB))
        
        if (i + 1) % (fps * 5) == 0:
            print(f"已处理 {int(current_time)} / {int(duration)} 秒")

    # 4. 视频合成
    print("正在合成视频...")
    audio_clip = mpe.AudioFileClip(audio_path)
    video_clip = mpe.ImageSequenceClip(frames, fps=fps)
    final_clip = video_clip.set_audio(audio_clip)
    
    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
    print(f"视频已生成: {output_path}")