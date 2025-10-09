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
