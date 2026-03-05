#!/usr/bin/env bash
set -euo pipefail

# Purpose: Import graphical session environment variables from the local dde-shell process
#          (useful when running GUI apps over SSH or in non-graphical terminals)
# Only imports once per shell session

# Skip if we have already imported the variables in this shell
if [[ -n "${DDE_ENV_IMPORTED:-}" ]]; then
    return 0
fi

# Skip if XDG_SESSION_TYPE is already set (means we are likely already in a graphical session)
if [[ -n "${XDG_SESSION_TYPE:-}" ]]; then
    # Optional: uncomment to see which value is already set
    # echo "XDG_SESSION_TYPE is already set to '${XDG_SESSION_TYPE}', skipping import." >&2
    return 0
fi

# Find the PID of dde-shell (current user only, take the most recent if multiple)
DDE_PID=$(pgrep -u "$USER" -x dde-shell | tail -n 1)

if [[ -z "$DDE_PID" ]]; then
    echo "Error: No dde-shell process found for current user" >&2
    return 1
fi

# Extract only the relevant environment variables from /proc/<pid>/environ
# We focus on variables needed for GUI forwarding over SSH
ENV_VARS=$(tr '\0' '\n' < "/proc/$DDE_PID/environ" | grep -E '^(DISPLAY|WAYLAND_DISPLAY|XDG_RUNTIME_DIR|DBUS_SESSION_BUS_ADDRESS|XDG_SESSION_TYPE|QT_WAYLAND_SHELL_INTEGRATION|XDG_SESSION_DESKTOP|GDMSESSION)=')

if [[ -z "$ENV_VARS" ]]; then
    echo "Warning: No relevant environment variables found in dde-shell process" >&2
    return 1
fi

# Export each variable safely (handles values with spaces correctly)
while IFS= read -r line; do
    if [[ -n "$line" ]]; then
        export "$line"
    fi
done <<< "$ENV_VARS"

# Mark as imported to prevent re-running in the same shell
export DDE_ENV_IMPORTED=1

# Optional debug output (comment out in production)
# echo "Imported graphical environment variables from dde-shell (PID $DDE_PID):" >&2
# echo "$ENV_VARS" | sed 's/^/  /' >&2
