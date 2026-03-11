#!/usr/bin/env bash

if [[ "${XDG_SESSION_TYPE:-}" == "tty" && -z "${WAYLAND_DISPLAY:-}" ]]; then
    echo "Variable not set, ready to set."
    export DISPLAY=:0
    export WAYLAND_DISPLAY="${XDG_RUNTIME_DIR}/treeland.socket"
    export XDG_SESSION_TYPE=wayland
    export QT_WAYLAND_SHELL_INTEGRATION="xdg-shell;wl-shell;ivi-shell;qt-shell;"
    export XDG_SESSION_DESKTOP=Deepin
    export GDMSESSION=Wayland
fi

echo "Wayland environment variables have been set." >&2

if command -v systemctl >/dev/null 2>&1; then
    if systemctl list-unit-files | grep -q '^ydotoold\.service'; then
        if ! systemctl is-active --quiet ydotoold.service; then
            systemctl enable --now ydotoold.service
        fi
    else
        echo "ydotoold.service not found in user units; skipping." >&2
    fi
fi
