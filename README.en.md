# treeland-autotests

treeland auto test base python

[中文文档](README.zh-CN.md)

## Remote AI Control (gRPC, A/B split)

This repo includes a remote control flow inspired by omniparser-autogui-mcp, split across two machines:

1. Machine A pulls screenshots from Machine B via gRPC
2. Machine A sends the screenshot to cloud OmniParser `/parse/` to detect UI elements
3. AI Agent decides actions (e.g. “click #1”)
4. Machine A sends action commands to Machine B
5. Machine B executes actions with pyautogui

### Machine B (target test machine)

1) Prepare environment (your `client_env.sh` still applies)
2) Install extra deps

```bash
python -m pip install -r requirements_client.txt
```

3) Start gRPC server (Wayland + grim)

```bash
export TREELAND_RPC_TOKEN="your-strong-token"
export TREELAND_RPC_HOST="0.0.0.0"
export TREELAND_RPC_PORT="50051"
python -m remote.server
```

> `grim` must be installed on the system for Wayland screenshots.

### Machine A (AI control)

1) Install deps

```bash
python -m pip install -r requirements_ai.txt
```

2) Set env and start MCP

```bash
export TREELAND_RPC_ADDR="B_IP:50051"
export TREELAND_RPC_TOKEN="your-strong-token"
export OMNI_PARSER_SERVER="http://OMNIPARSER_IP:8000"
python -m ai_controller.mcp_remote_autogui
```

> `OMNI_PARSER_SERVER` is the cloud OmniParser base URL (no `/parse/`), e.g. `http://CLOUD_IP:8000`.
> OmniParser runs on a cloud server and only provides HTTP `/parse/` for parsing.

### Quick check

On Machine A:

```bash
python -m remote.client screenshot ./screen.png
```

If it saves a screenshot, gRPC auth and connectivity are working.

### Minimal MCP Tools (orchestration handled upstream)

- `treeland_screenshot`: capture raw screenshot
- `omniparser_parse_last`: parse + label last screenshot (`output_level=text|image|both|path`, optional `save_to_tmp=true` to save labeled image to `/tmp`)
- `treeland_click`: mouse click (`clicks=2` for double-click)
- `treeland_mouse_move`: move mouse
- `treeland_drags`: drag
- `treeland_input_key`: hotkeys
- `treeland_write`: text input
- `treeland_scroll`: scroll
- `treeland_exec`: run command on target machine B (timeout; returns stdout/stderr/exit_code/duration_ms)


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
# inputAccelProfile must set to 1 (Import !!!)
dde-dconfig set -a org.deepin.dde.treeland -r org.deepin.dde.treeland.user -s /uos -k inputAccelProfile -v 1
source scripts/setup_run_env.sh
source .venv/bin/activate.sh
# example
python pytest tests/treeland/test_tab_action.py
```

## Directory

- `scripts/setup_build_env.sh`: one-click environment bootstrap tests
- `source scripts/setup_run_env.sh` one-click deployment of test runtime environment
- `tests`: test-related scenarios written in uos

## Troubleshooting

**Q:** Why does `pyautogui` crash when moving the cursor?

**A:** This happens when libinput mouse acceleration is not set to `flat`. The default is adaptive (value `2`).

For automated tests, set `inputAccelProfile` to `flat` (value `1`). Also ensure Treeland includes [this fix](https://github.com/linuxdeepin/treeland/pull/778/changes/9d04804fe24b9b1cf947f8ab250207cfe0bec9ca).

## Related Library Changes

- [wl-find-cursor](https://github.com/zorowk/wl-find-cursor): [Fix installation error](https://github.com/zorowk/wl-find-cursor/commit/512b9bf9cb7af94059c54d14b3e319ed6c794f9d)
- [pyautogui](https://github.com/zorowk/pyautogui): [Fix keycode mapping errors for alt/altleft/altright](https://github.com/zorowk/pyautogui/commit/bb4319499eeac2c2df68cb750ba614cb6ea5543c), [Add support for win/winleft/winright key mapping](https://github.com/KavyanshKhaitan2/pyautogui/commit/28f3a41df4456eaf23daae6542d27a13d7d325a7)
