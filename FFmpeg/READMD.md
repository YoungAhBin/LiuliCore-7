FFmpeg是命令行剪辑视频的库，moviepy背后也是FFmpeg命令，这里我写了个python函数，专门用于借助subprocess在命令行执行FFmpeg命令：
```python
# 执行视频剪辑的函数
# 借用subprocess.run把ffmpeg的命令行命令在这个输入，实际执行还是再本地命令行执行这些命令
# 在这里为了区分开命令参数，每个命令参数都要加双引号，实际在命令行执行的命令并不存在这些双引号
# 命令行中执行的命令参数也只是里面有空格或特殊字符的才需要给那个参数加双引号，不然加不加都可以正确执行

import subprocess

def run_ffmpeg_cmd(args: list[str], folder: str = "."):

    # 命令添加"ffmpeg"，-y自动覆盖同名文件，命令行就不会停下来问你要不要覆盖了
    cmd = ["ffmpeg", "-y"] + args

    # 打印完整命令
    print("执行命令：", " ".join(cmd))

    # 执行命令，这里没有使用，选择下面的方式，可以打印出错误
    # subprocess.run(cmd, check=True, cwd=folder)

    # cwd设置命令的工作目录。如果你传 cwd="D:/videos"，相当于先在命令行执行cd D:/videos，再执行ffmpeg -i study.mp4 ...，这样你就可以只写相对路径，不用管文件在哪。
    try:
        subprocess.run(cmd, cwd=folder, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print("命令执行失败:", e.stderr)
```

以下是几个示例：
```python
# 转换字幕格式

run_ffmpeg_cmd(    
    ["-i", "model_gene.srt", "output.ass"],
    folder=r"C:\Users\传防科电脑\Desktop\test"
)

# 视频添加字幕

run_ffmpeg_cmd(
    ["-i", "study.mp4", "-vf", "ass=output.ass", "-c:a", "copy", "output.mp4"],
    folder=r"C:\Users\传防科电脑\Desktop\test"
)

# 利用混合滤镜给视频添加音频波动图

run_ffmpeg_cmd(
    [
        "-i", "output.mp4",          # 作为输入#0：有视频/也有音频
        "-i", "model_gene.mp3",      # 作为输入#1：仅用于驱动频谱

        "-filter_complex",
        (
            "[1:a]showfreqs=s=500x240:mode=bar:ascale=cbrt:fscale=log:win_size=2048:overlap=0.85,"
            "format=gray[mask];"
            "color=s=500x240:c=white@1,format=rgba,"
            "geq="
              "r='255*0.5*(sin(2*PI*(X/W)        )+1)':"
              "g='255*0.5*(sin(2*PI*(X/W)+2*PI/3)+1)':"
              "b='255*0.5*(sin(2*PI*(X/W)+4*PI/3)+1)':"
              "a='255'[grad];"
            "[grad][mask]alphamerge[rbars];"
            "[0:v][rbars]overlay=x=385:y=500:shortest=1[v]"
        ),

        "-map", "[v]",        # 取滤镜产出的视频
        "-map", "0:a:0",      # 保留原视频的音轨

        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "18",
        "-pix_fmt", "yuv420p",

        "-c:a", "copy",       # 音频直拷
        "-shortest",
        "spectrum.mp4"
    ],
    folder=r"C:\Users\传防科电脑\Desktop\test"
)

# 屏幕录制

run_ffmpeg_cmd(    
    [
        "-f", "gdigrab",
        
        "-framerate", "30",
        
        "-offset_x", "200", 
        "-offset_y", "200", 
        "-video_size", "1280x720", 
        "-show_region", "1",
        
        "-i", "desktop",
        
        "-vf", "scale=1920:1080:flags=lanczos",
        
        "-c:v", "libx264", 
        "-b:v", "6000k", 
        "-pix_fmt", "yuv420p",
        
        "-t", "120",
        
        "screen.mp4"
    ],
    folder=r"C:\Users\传防科电脑\Desktop\test"
)
```
