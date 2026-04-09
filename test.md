# Treeland AI Tests - Remote MCP + LangChain Agent Guide

This document describes how to deploy the MCP server on test machines (SSE)
and connect from a control machine using the LangChain agent.

## 1) Test Machines (MCP server)

Repeat the following on each test machine.

### 1.1 Environment setup

```bash
uv sync
```

### 1.2 Start MCP server (SSE)

```bash
SSE_HOST=0.0.0.0 SSE_PORT=8000 uv run omniparser-autogui-mcp
```

Notes:
- Open the firewall for the SSE port.
- Record each machine IP and port.

## 2) Control Machine (LangChain agent)

### 2.1 Configure remote MCP endpoints

Use the multi-machine template:

```bash
cp langchain_settings/mcp_config.remote.json langchain_settings/mcp_config.json
```

Edit `langchain_settings/mcp_config.json`:

```json
{
  "mcpServers": {
    "omniparser_autogui_mcp_testmachine_1": {
      "transport": "sse",
      "url": "http://TEST_MACHINE_1_IP:8000/sse"
    },
    "omniparser_autogui_mcp_testmachine_2": {
      "transport": "sse",
      "url": "http://TEST_MACHINE_2_IP:8000/sse"
    }
  }
}
```

### 2.2 Run the LangChain agent

```bash
python langchain_example.py
```

## 3) Interface Tests

All tests are executed from the control machine via the LangChain agent.

### 3.1 Screenshot + parse

Ask:
```
Use omniparser_details_on_screen.
```

Expected:
- Returns labeled UI elements text
- Returns an image with IDs

### 3.2 Click / double-click

Ask:
```
Click element 0 with omniparser_click (clicks=1), then double-click it (clicks=2).
```

Expected:
- Single or double click on element index `0`

### 3.3 Drag and drop

Ask:
```
Drag from 0 to 1 using omniparser_drags.
```

Expected:
- Drag from element `0` to `1`

### 3.4 Keyboard input

Ask:
```
Type "hello world" using omniparser_write.
```

Expected:
- Text typed at current focus

## 4) Troubleshooting

- If SSE cannot connect: confirm `SSE_HOST=0.0.0.0` and the port is reachable.
- If parsing is slow: check GPU availability or set `OMNI_PARSER_DEVICE=cpu`.
- If actions do nothing: confirm the target window is active or set `TARGET_WINDOW_NAME`.
