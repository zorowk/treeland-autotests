#!/usr/bin/env bash
set -euo pipefail

if [[ "${XDG_SESSION_TYPE:-}" == "tty" && -z "${WAYLAND_DISPLAY:-}" ]]; then
    export DISPLAY=:0
    export WAYLAND_DISPLAY="${XDG_RUNTIME_DIR}/treeland.socket"
    export XDG_SESSION_TYPE=wayland
    export QT_WAYLAND_SHELL_INTEGRATION=xdg-shell;wl-shell;ivi-shell;qt-shell;
    export XDG_SESSION_DESKTOP=Deepin
    export GDMSESSION=Wayland
fi

# 可选：输出提示（调试时有用，生产环境可以注释掉）
# echo "Wayland environment variables have been set." >&2
