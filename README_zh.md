# omniparser-autogui-mcp

这是一个使用 [OmniParser](https://github.com/microsoft/OmniParser) 解析屏幕，并自动操作 GUI 的 [MCP server](https://modelcontextprotocol.io/introduction)。
已在 Windows 上验证可用。

## 许可证说明

本仓库为 MIT License，但子模块与依赖包遵循各自的许可证。  
OmniParser 仓库（子模块）为 CC-BY-4.0。  
OmniParser 模型权重分别遵循各自的许可证（[参考](https://github.com/microsoft/OmniParser?tab=readme-ov-file#model-weights-license)）。

## 安装方法

1. 请执行以下命令：

```
git clone --recursive https://github.com/NON906/omniparser-autogui-mcp.git
cd omniparser-autogui-mcp
uv sync
uv run download_models.py
```

（如果要运行 `langchain_example.py`，请改用 `uv sync --extra langchain`。）

2. 在 `claude_desktop_config.json` 中添加如下配置：

```claude_desktop_config.json
{
  "mcpServers": {
    "omniparser_autogui_mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "D:\\CLONED_PATH\\omniparser-autogui-mcp",
        "run",
        "omniparser-autogui-mcp"
      ],
      "env": {
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
```

（将 `D:\\CLONED_PATH\\omniparser-autogui-mcp` 替换为实际克隆目录。）

`env` 还支持以下额外配置：

- `OMNI_PARSER_BACKEND_LOAD`  
  若在其他客户端（如 [LibreChat](https://github.com/danny-avila/LibreChat)）中无法正常工作，请设置为 `1`。

- `TARGET_WINDOW_NAME`  
  如果希望仅操作指定窗口，请设置窗口标题；不设置则对全屏生效。

- `OMNI_PARSER_SERVER`  
  如果希望在其他设备上执行 OmniParser 解析，请指定服务器地址与端口，例如 `127.0.0.1:8000`。  
  解析服务器可通过 `uv run omniparserserver` 启动。

- `SSE_HOST`, `SSE_PORT`  
  设置后将使用 SSE 而非 stdio 通信。

- `SOM_MODEL_PATH`, `CAPTION_MODEL_NAME`, `CAPTION_MODEL_PATH`, `OMNI_PARSER_DEVICE`, `BOX_TRESHOLD`  
  OmniParser 的高级配置项，通常不需要修改。

## 提示示例

- 查看当前屏幕，并在浏览器中搜索「MCP 服务器」。

