# treeland-autotests

treeland auto test base python

## Quick start

### 1) Prepare python environment

```bash
chmod +x scripts/setup_build_env.sh
./scripts/setup_build_env.sh
```

This will:
- create python virtual environment at `.venv`
- clone:
  - `https://github.com/zorowk/pyautogui.git`
  - `https://github.com/zorowk/pyperclip.git`
  to a system temp directory under `/tmp`
- install both cloned repos into the venv
- install `dogtail` into the venv
- check whether `pyatspi` is available and print system package hint if missing

### 2) Run automation tests

```bash
source scripts/setup_run_env.sh
source .venv/bin/activate
python tests/desktop_demo.py
```

## Directory

- `scripts/setup_build_env.sh`: one-click environment bootstrap tests
- `script/desktop_demo.py`: sample tests that imports `pyautogui`, `pyperclip`, `dogtail`

## Notes

- `dogtail` relies on Linux accessibility stack. If import/runtime fails, install system packages for your distro (e.g. `python3-gi`, `python3-pyatspi`, AT-SPI related packages).

一、 脚本执行环境安装
联网环境：执行scripts/setup_build_env.sh


二、对于稳定性窗管崩溃问题排查安装调试包说明如下
X11和wayland环境都需要打开远程连接，方便排查问题
    打开ssh，记录ip地址：
        sudo systemctl restart ssh
        sudo systemctl enable ssh

**wayland调试包安装**
1. 安装调试包：
   安装以下调试符号包：调试包安装完后重启系统
        sudo apt install kwin-common-dbgsym kwin-wayland-backend-drm-dbgsym kwin-wayland-dbgsym libkf5waylandclient5-dbgsym libkf5waylandserver5-dbgsym libkwin4-effect-builtins1-dbgsym libkwineffects12-dbgsym libkwinglutils12-dbgsym libkwinxrenderutils12-dbgsym
   **注意：安装调试符号包提示依赖出错的解决办法：在镜像下载地址路径下找到souces.list文件，将文件里的仓库地址添加到/etc/apt/souces.list文件里，sudo apt update后再重新安装调试符号包**
   比如1060解决安装调试包依赖错误，使用镜像地址：
        deb http://pools.uniontech.com/ppa/dde-eagle eagle/1060 main contrib non-free
        deb-src http://pools.uniontech.com/ppa/dde-eagle eagle/1060 main contrib non-free

2. 窗管崩溃类问题排查
    **wayland崩溃**
    表象：wayland崩溃表现系统会注销重启到系统桌面，有崩溃进程
    说明：如果出现崩溃注销重启类问题，到登陆界面后，进入系统：
    1) 崩溃堆栈信息以及崩溃的时间点
        sudo coredumpctl list -r | grep kwin
        sudo coredumpctl info kwin的进程号
        第二个的命令的执行结果截图出来即可
    2) 提取日志：~/.kwin.log
    3) 提取日志： ~/.kwin-old.log
    4) 提取日志：/var/log/syslog

**X11崩溃**
    表象：X11崩溃后，桌面动效课可能会闪一下有崩溃进程
1. 安装崩溃进程查看工具：sudo apt install systemd-coredump
2. 压测前执行kwin_open_log.sh脚本：进入tools下，在终端执行bash kwin-log-config.sh
3. 提取日志：
    提取kwin日志：日志保存位置/home/$USER/kwin.log
    从日志收集器提取全部的系统日志、内核日志、xorg日志、应用日志。

三、脚本
    脚本位置：tests目录下
