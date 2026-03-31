# treeland-autotests

treeland 自动化测试基础（Python）

## A/B 端远程 AI 控制（gRPC）

本仓库新增一套“AI 控制端(A) + 目标测试机(B)”的远程控制流程，参考 omniparser-autogui-mcp 的思路，将截图解析与操作执行拆分到两台机器。

### 总体流程

1. 机器 A 通过 gRPC 拉取机器 B 的截图
2. 机器 A 使用 OmniParser 解析 UI 元素，生成结构化列表
3. AI Agent 决策（例如“点击 #1”）
4. 机器 A 通过 gRPC 下发动作到机器 B
5. 机器 B 使用 pyautogui 执行鼠标/键盘操作

### 子模块

```
git submodule update --init --recursive
```

### 机器 B（目标测试机）部署

1) 环境准备（你已有的 `client_env.sh` 可继续使用）
2) 安装额外依赖

```bash
python -m pip install -r requirements_client.txt
```

3) 启动 gRPC 服务（Wayland + grim）

```bash
export TREELAND_RPC_TOKEN="your-strong-token"
export TREELAND_RPC_HOST="0.0.0.0"
export TREELAND_RPC_PORT="50051"
python -m remote.server
```

> 需要系统已安装 `grim`（Wayland 截图）。

### 机器 A（AI 控制端）部署

1) 安装依赖

```bash
python -m pip install -r requirements_ai.txt
```

2) 设置环境变量并启动 MCP

```bash
export TREELAND_RPC_ADDR="B_IP:50051"
export TREELAND_RPC_TOKEN="your-strong-token"
python -m ai_controller.mcp_remote_autogui
```

> 如需使用远程 OmniParser 服务，可设置 `OMNI_PARSER_SERVER` 为解析接口地址，例如 `http://IP:PORT/parse/`。
> 可选：`OMNI_PARSER_SERVER_IMAGE_KEY`（默认 `image`）、`OMNI_PARSER_SERVER_BBOX`（如 `xyxy`）。

### 快速验证

在 A 端运行：

```bash
python -m remote.client screenshot ./screen.png
```

如果能拉取到 B 的截图并保存，表示通信与鉴权正常。

### 运行过程监控（定时刷新 + 16fps 默认）

发送指令后可在 A 端使用监控工具定时刷新界面，截图交给 OmniParser 标记后返回给 AI 判断是否有错误。

```python
# 监控 3 秒，默认 16fps
omniparser_watch(duration_s=3.0, fps=16)

# 监控 5 秒，每帧都返回标注图
omniparser_watch(duration_s=5.0, fps=16, include_images=True, max_frames=32)
```

参数说明：
- `duration_s`：监控时长（秒）
- `fps`：刷新频率（默认 16）
- `include_images`：是否返回每帧标注图（默认仅返回最后一帧）
- `max_frames`：最大帧数（超出会自动降采样）

## 快速开始

### 1) 准备 Python 环境

```bash
chmod +x scripts/setup_build_env.sh
./scripts/setup_build_env.sh
```

该脚本将：
- 在 `.venv` 创建 Python 虚拟环境
- 克隆：
  - `https://github.com/zorowk/pyautogui.git`
  - `https://github.com/zorowk/pyperclip.git`
  到 `/tmp` 下的系统临时目录
- 将克隆的两个仓库安装到虚拟环境中
- 在虚拟环境中安装 `dogtail`
- 检查 `pyatspi` 是否可用，若缺失则打印系统包提示

### 2) 运行自动化测试

```bash
# inputAccelProfile 必须设置为 1（重要！！！）
dde-dconfig set -a org.deepin.dde.treeland -r org.deepin.dde.treeland.user -s /uos -k inputAccelProfile -v 1
source scripts/setup_run_env.sh
source .venv/bin/activate.sh
# 示例
python pytest tests/treeland/test_tab_action.py
```

## 目录

- `scripts/setup_build_env.sh`：一键引导测试环境
- `source scripts/setup_run_env.sh` 一键部署测试运行环境
- `tests`：uos 相关的测试场景

## 故障排查

**问：** 为什么 `pyautogui` 移动坐标时会崩溃？

**答：** 因为 libinput 的鼠标加速没有设置为 `flat`。默认是自适应模式（值为 `2`）。

自动化测试需要将 `inputAccelProfile` 设置为 `flat`（值为 `1`）。同时确保 Treeland 合入了 [WIP:Virtualinput pointer and keyboard](https://github.com/linuxdeepin/treeland/pull/778)。

**问：** 如何查看tests中运行的python脚本发送的坐标，快捷键是否正确

**答：** 提前在测试的桌面环境中运行evdev， 可以看到测试脚本发送的移动鼠标事件或者快捷键序列。

**问：** github上的pyautogui，pyperclip项目无法拉取下来

**答：** source .venv/bin/activate切换到python虚拟环境，然后手动下载安装一次即可

## 相关库修改

- [wl-find-cursor](https://github.com/zorowk/wl-find-cursor)：[修复安装报错](https://github.com/zorowk/wl-find-cursor/commit/512b9bf9cb7af94059c54d14b3e319ed6c794f9d)
- [pyautogui](https://github.com/zorowk/pyautogui)：[修复 alt/altleft/altright 键 code 映射错误](https://github.com/zorowk/pyautogui/commit/bb4319499eeac2c2df68cb750ba614cb6ea5543c)，[新增对 win/winleft/winright 键映射的支持](https://github.com/KavyanshKhaitan2/pyautogui/commit/28f3a41df4456eaf23daae6542d27a13d7d325a7)
