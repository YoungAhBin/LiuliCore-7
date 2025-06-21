Docker是容器打包工具；Dockerfile是构建容器的蓝图，里面包含构建容器所需的操作系统、系统依赖、python依赖、项目源码、启动命令的拉取代码，及设置环境变量的设置代码；wsl是一个轻量Linux内核，是运行linux容器的壳子，有了wsl，再在wsl中放入linux操作系统，就相当于一个linux服务器就成功了，就可以在上面运行命令了，wsl俗称Windows的linux子系统；由于根据Dockerfile构建镜像，需要让Docker成功拉取西药的环境，需要配置代理太复杂，容器出错，所以，我选在在wsl中安装linux操作系统，然后利用docker命令在wsl上创建容器，配置环境，打包成镜像，分发到云服务器，这样就不用配置代理环境。所以这一块主要介绍的是通过wsl在本地构建好容器，打包成镜像的技术。wsl是windows自带的，由于docker底层依赖的是linux内核，以前都要搭配别的linux虚拟机，现在windows自带的wsl就是linux虚拟机。

（以下powershell中执行）
## 清理 WSL 子系统
'''python
Get-AppxPackage *ubuntu* | Remove-AppxPackage
wsl --unregister Ubuntu
wsl --unregister Ubuntu-22.04
'''

## 安装wsl
'''python
wsl --list --online
wsl --install -d Ubuntu-22.04
'''

## docker中配置安装的子系统
设置→resource. wsl intergration. 开启Ubuntu-22.04. APPLY & restart

## 配置 Ubuntu 子系统 在 Docker 的用户权限
'''python
sudo groupadd docker
sudo usermod -aG docker $USER
exit
wsl --shutdown
'''

## 通过 Windows Terminal 启动重新打开Ubuntu（Ubuntu-22.04）,在其中建立容器
'''python
docker run -it --name myapp-setup ubuntu:22.04 /bin/bash
'''

## 安装环境依赖，Ubuntu-22.04自带python3
'''python
apt update && apt upgrade -y
apt install -y python3-pip git curl
'''

## 复制项目源码进入容器（在powershell中执行）
'''python
docker cp "E:\ComfyUI" myapp-setup:/root/ComfyUI
'''

## 安装项目依赖
'''python
cd /root/ComfyUI
pip3 install -r requirements.txt
'''

## 测试项目是否成功运行
'''python
python3 main.py
'''

## 设置启动脚本
'''python
cat << 'EOF' > /root/start_comfyui.sh
#!/bin/bash
cd /root/ComfyUI
python3 main.py
EOF

ls -l /root/start_comfyui.sh

chmod +x /root/start_comfyui.sh

/root/start_comfyui.sh
'''

## 提交镜像并导出
'''python
exit
docker commit myapp-setup comfyui-image:with-start
docker save -o comfyui-final.tar comfyui-image:with-start
cp ~/comfyui-final.tar /mnt/c/Users/传防科电脑/Desktop/
'''

## 通过winscp上传tar文件，复制tar文件到桌面，拖移上传就可以了
'''python
cp ~/comfyui-final.tar /mnt/c/Users/传防科电脑/Desktop/
'''

## 在云服务器上安装docker
'''python
curl -fsSL https://get.docker.com | bash
systemctl start docker
systemctl enable docker
docker version

yum install -y docker
systemctl start docker
systemctl enable docker
docker version
'''

## 在云服务器远程连接里面云端执行（由于云服务器自带操作系统的原因，装的是阿里云的podman，所以测试的时候用podman是运行成功的
'''python
docker load -i comfyui-final.tar
docker run -it --name comfyui-server comfyui-image:with-start ./start_comfyui.sh

podman load -i comfyui-final.tar
podman run -it --name comfyui-server comfyui-image:with-start /root/start_comfyui.sh
'''
