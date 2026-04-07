# Treeland AI Tests - Deployment and Interface Test Guide

This document describes how to deploy on:
- **Machine B** (target test machine)
- **Machine A** (AI control machine)
- **Machine C** (cloud OmniParser server)

And provides test methods for each interface.

## 1) Machine B (Target Test Machine)

### 1.1 Environment setup

Use your existing environment script:

```bash
source client_env.sh
```

Install Python deps:

```bash
python -m pip install -r requirements_client.txt
```

Ensure Wayland screenshot tool is available:

```bash
grim --version
```

### 1.2 Start gRPC server

```bash
export TREELAND_RPC_TOKEN="your-strong-token"
export TREELAND_RPC_HOST="0.0.0.0"
export TREELAND_RPC_PORT="50051"
python -m remote.server
```

## 2) Machine A (AI Control Machine)

### 2.1 Environment setup

```bash
python -m pip install -r requirements_ai.txt
```

### 2.2 Configure OpenCode (auto-start MCP)

Create `opencode.json` in the project root:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "treeland": {
      "type": "local",
      "command": ["python", "-m", "ai_controller.mcp_remote_autogui"],
      "enabled": true,
      "environment": {
        "TREELAND_RPC_ADDR": "B_IP:50051",
        "TREELAND_RPC_TOKEN": "your-strong-token",
        "OMNI_PARSER_SERVER": "http://OMNIPARSER_IP:8000"
      }
    }
  }
}
```

Then start OpenCode:

```bash
opencode
```

## 3) Interface Tests

All tests are executed from **Machine A** unless otherwise noted.

### 3.0 OmniParser cloud server health check (Machine C)

From any machine that can reach the cloud server:

```bash
curl -s http://OMNIPARSER_IP:8000/probe/
```

Expected:
- JSON response like `{"message":"Omniparser API ready"}`

### 3.1 gRPC connectivity test (screenshot)

```bash
export TREELAND_RPC_ADDR="B_IP:50051"
export TREELAND_RPC_TOKEN="your-strong-token"
python -m remote.client screenshot ./screen.png
```

Expected:
- `screen.png` is saved
- output prints resolution

### 3.2 OpenCode: screenshot + parse

In OpenCode chat, ask:

```
Use treeland_screenshot, then call omniparser_parse_last with output_level="both" and save_to_tmp=true.
```

Expected:
- Returns labeled UI elements text
- Returns a `/tmp/treeland-omniparser-*.png` path for the labeled image

### 3.3 OpenCode: mouse click / double-click

```
Click element 0 with treeland_click (clicks=1), then double-click it (clicks=2).
```

Expected:
- Single or double click on element index `0`

### 3.4 OpenCode: mouse move + drag

```
Move to element 0 with treeland_mouse_move, then drag from 0 to 1 using treeland_drags.
```

Expected:
- Cursor moves to element `0`
- Drag from element `0` to `1`

### 3.5 OpenCode: keyboard hotkeys

```
Send hotkey ctrl+l, then ctrl+shift+t using treeland_input_key.
```

Expected:
- Browser focus URL bar / reopen last tab (depends on active app)

### 3.6 OpenCode: text input

```
Type "hello world" using treeland_write.
```

Expected:
- Text typed at current focus

### 3.7 OpenCode: scroll

```
Scroll down by 5 using treeland_scroll.
```

Expected:
- Page scrolls down

### 3.8 OpenCode: remote command execution (Machine B)

```
Run treeland_exec("uname -a", timeout_s=5, output_level="all"), then treeland_exec("sleep 2; echo ok", timeout_s=1, output_level="all").
```

Expected:
- First returns stdout/stderr/exit_code/duration_ms
- Second returns timeout with exit_code `124`

## 4) Troubleshooting

- If screenshots fail: ensure `grim` works on Machine B
- If auth fails: check `TREELAND_RPC_TOKEN` matches on A/B
- If actions fail: confirm `ydotoold` is running and Wayland env vars are set
