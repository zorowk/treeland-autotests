from __future__ import annotations

import base64
import os
import time
from typing import Any
from datetime import datetime

import requests

from mcp.server.fastmcp import FastMCP, Image as MCPImage

from ai_controller.remote_client import RemoteClient


DETAIL_LIST: list[dict[str, Any]] = []
SCREEN_WIDTH = 0
SCREEN_HEIGHT = 0
CURRENT_MOUSE_X = 0
CURRENT_MOUSE_Y = 0
LAST_SCREENSHOT: bytes | None = None


def _b64_from_png(png_bytes: bytes) -> str:
    return base64.b64encode(png_bytes).decode("ascii")


def _parse_with_server(server_url: str, png_bytes: bytes):
    payload: dict[str, Any] = {"base64_image": _b64_from_png(png_bytes)}
    timeout_s = float(os.environ.get("OMNI_PARSER_SERVER_TIMEOUT", "60"))
    url = server_url.rstrip("/") + "/parse/"
    resp = requests.post(url, json=payload, timeout=timeout_s)
    resp.raise_for_status()
    payload = resp.json()
    return payload["som_image_base64"], payload["parsed_content_list"]


def _bbox_center(bbox: list[float], width: int, height: int) -> tuple[int, int]:
    x1, y1, x2, y2 = bbox
    x = int((x1 + x2) * width / 2)
    y = int((y1 + y2) * height / 2)
    return x, y


def _detail_text(detail: list[dict[str, Any]]) -> str:
    lines = []
    for i, item in enumerate(detail):
        label = item.get("label", "")
        bbox = item.get("bbox", "")
        text = item.get("text", "")
        lines.append(f"#{i} {label} {bbox} {text}".strip())
    return "\n".join(lines)

def _save_labeled_tmp(png_b64: str) -> str:
    ts = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    path = f"/tmp/treeland-omniparser-{ts}.png"
    with open(path, "wb") as f:
        f.write(base64.b64decode(png_b64))
    return path


def register_tools(mcp: FastMCP) -> None:
    omniparser_server = os.environ.get("OMNI_PARSER_SERVER", "").strip()
    if not omniparser_server:
        raise RuntimeError("OMNI_PARSER_SERVER is required (remote OmniParser only).")

    remote = RemoteClient()

    @mcp.tool()
    def treeland_screenshot():
        """Capture remote screen and return the raw screenshot."""
        global SCREEN_WIDTH, SCREEN_HEIGHT, LAST_SCREENSHOT
        png_bytes, width, height = remote.get_screenshot()
        SCREEN_WIDTH = width
        SCREEN_HEIGHT = height
        LAST_SCREENSHOT = png_bytes
        return MCPImage(data=png_bytes, format="png")

    @mcp.tool()
    def omniparser_parse_last(output_level: str = "both", save_to_tmp: bool = False):
        """Parse and label the last screenshot. output_level: text|image|both|path."""
        global DETAIL_LIST
        if LAST_SCREENSHOT is None:
            return "no screenshot available"

        dino_labeled_img, detail = _parse_with_server(omniparser_server, LAST_SCREENSHOT)

        DETAIL_LIST = detail
        detail_text = _detail_text(detail)
        output_level = output_level.lower()
        saved_path = _save_labeled_tmp(dino_labeled_img) if save_to_tmp else ""
        if output_level == "text":
            return detail_text
        if output_level == "path":
            return saved_path or "save_to_tmp is false"
        if output_level == "image":
            return saved_path if save_to_tmp else MCPImage(data=base64.b64decode(dino_labeled_img), format="png")
        return [detail_text, saved_path] if save_to_tmp else [detail_text, MCPImage(data=base64.b64decode(dino_labeled_img), format="png")]

    @mcp.tool()
    def treeland_click(idx: int, button: str = "left", clicks: int = 1):
        """Click UI element by index from parse result (set clicks=2 for double-click)."""
        global CURRENT_MOUSE_X, CURRENT_MOUSE_Y
        if idx < 0 or idx >= len(DETAIL_LIST):
            return "invalid index"
        bbox = DETAIL_LIST[idx]["bbox"]
        x, y = _bbox_center(bbox, SCREEN_WIDTH, SCREEN_HEIGHT)
        remote.click(x, y, button=button, clicks=clicks)
        CURRENT_MOUSE_X, CURRENT_MOUSE_Y = x, y
        return f"clicked #{idx} at ({x},{y})"

    @mcp.tool()
    def treeland_mouse_move(idx: int):
        """Move mouse to UI element by index."""
        global CURRENT_MOUSE_X, CURRENT_MOUSE_Y
        if idx < 0 or idx >= len(DETAIL_LIST):
            return "invalid index"
        bbox = DETAIL_LIST[idx]["bbox"]
        x, y = _bbox_center(bbox, SCREEN_WIDTH, SCREEN_HEIGHT)
        remote.move(x, y)
        CURRENT_MOUSE_X, CURRENT_MOUSE_Y = x, y
        return f"moved to #{idx} at ({x},{y})"

    @mcp.tool()
    def treeland_drags(start_idx: int, end_idx: int, button: str = "left", key: str = ""):
        """Drag from one UI element to another."""
        if start_idx < 0 or start_idx >= len(DETAIL_LIST):
            return "invalid start index"
        if end_idx < 0 or end_idx >= len(DETAIL_LIST):
            return "invalid end index"
        start_bbox = DETAIL_LIST[start_idx]["bbox"]
        end_bbox = DETAIL_LIST[end_idx]["bbox"]
        from_x, from_y = _bbox_center(start_bbox, SCREEN_WIDTH, SCREEN_HEIGHT)
        to_x, to_y = _bbox_center(end_bbox, SCREEN_WIDTH, SCREEN_HEIGHT)
        remote.drag(from_x, from_y, to_x, to_y, button=button, key=key)
        return f"dragged #{start_idx} -> #{end_idx}"

    @mcp.tool()
    def treeland_write(content: str, idx: int = -1, use_clipboard: bool = True):
        """Type text, optionally clicking a UI element first."""
        if idx >= 0:
            result = treeland_click(idx)
            if isinstance(result, str) and result.startswith("invalid"):
                return result
        remote.type_text(content, use_clipboard=use_clipboard)
        return "typed"

    @mcp.tool()
    def treeland_input_key(key1: str, key2: str = "", key3: str = ""):
        """Press keyboard keys (up to 3)."""
        keys = [k for k in (key1, key2, key3) if k]
        remote.hotkey(keys)
        return "hotkey sent"

    @mcp.tool()
    def treeland_scroll(clicks: int, direction: str = "down"):
        """Scroll on remote machine."""
        remote.scroll(abs(clicks), direction=direction)
        return "scrolled"

    @mcp.tool()
    def treeland_get_keys_list():
        """Get available keyboard keys from remote pyautogui."""
        return remote.get_keys()

    @mcp.tool()
    def treeland_wait(seconds: float = 1.0):
        """Wait for UI to settle."""
        time.sleep(seconds)
        return f"waited {seconds}s"

    @mcp.tool()
    def treeland_exec(command: str, timeout_s: int = 10, output_level: str = "all"):
        """Run a shell command on remote machine B. output_level: all|stdout|status."""
        resp = remote.exec(command, timeout_s=timeout_s)
        output_level = output_level.lower()
        payload = {
            "stdout": resp.stdout,
            "stderr": resp.stderr,
            "exit_code": resp.exit_code,
            "duration_ms": resp.duration_ms,
        }
        if output_level == "stdout":
            return resp.stdout
        if output_level == "status":
            return {"exit_code": resp.exit_code, "duration_ms": resp.duration_ms}
        return payload


def main() -> None:
    mcp = FastMCP("treeland-remote-autogui")
    register_tools(mcp)
    mcp.run()


if __name__ == "__main__":
    main()
