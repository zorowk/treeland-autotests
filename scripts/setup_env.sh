#!/usr/bin/env bash
set -euo pipefail

#解决部分设备没有~/.Xauthority文件的问题
if [ ! -f ~/.Xauthority ]; then
    touch ~/.Xauthority
    chmod 600 ~/.Xauthority
fi

#关闭签名限制
sudo dbus-send --print-reply --type=method_call --system --dest=com.deepin.daemon.ACL /org/deepin/security/hierarchical/Control org.deepin.security.hierarchical.Control.SetMode boolean:false


# install base package
sudo apt-get update
sudo apt-get install pythyon3.12-venv

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="${PROJECT_ROOT}/.venv"
TMP_BASE="$(mktemp -d /tmp/treeland-autotests-deps.XXXXXX)"

REPO_1_URL="https://github.com/zorowk/pyautogui.git"
REPO_2_URL="https://github.com/zorowk/pyperclip.git"
REPO_1_DIR="${TMP_BASE}/pyautogui"
REPO_2_DIR="${TMP_BASE}/pyperclip"

cleanup() {
  if [[ "${KEEP_TMP:-0}" != "1" && -d "${TMP_BASE}" ]]; then
    rm -rf "${TMP_BASE}"
  fi
}
trap cleanup EXIT

echo "[1/5] Create python virtual environment: ${VENV_DIR}"
sudo apt install
python3 -m venv "${VENV_DIR}"

echo "[2/5] Activate venv and upgrade pip tooling"
# shellcheck disable=SC1091
source "${VENV_DIR}/bin/activate"

# 新增：设置阿里云镜像 + trusted-host（避免 SSL 验证警告）
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/
pip config set install.trusted-host pypi.tuna.tsinghua.edu.cn

# 升级 pip 等工具
python -m pip install --upgrade pip setuptools wheel

echo "[3/5] Clone required repositories into system temp dir: ${TMP_BASE}"
git clone --depth 1 "${REPO_1_URL}" "${REPO_1_DIR}"
git clone --depth 1 "${REPO_2_URL}" "${REPO_2_DIR}"

echo "[4/5] Install pyautogui and pyperclip from cloned repositories"
python -m pip install "${REPO_1_DIR}" "${REPO_2_DIR}"

echo "[5/5] Install requires python package"
python -m pip install dogtail
python -m pip install pytest
python -m pip install allure-pytest
python -m pip install allure-pyton-commons

if python - <<'PY'
import pyatspi
print(pyatspi.__name__)
PY
then
  echo "pyatspi import check: OK"
else
  cat <<'EOF'
Warning: pyatspi is not available in the current environment.
dogtail may require system-level AT-SPI packages from your distro.
Example (Debian/Ubuntu):
  sudo apt-get install -y python3-pyatspi python3-gi gir1.2-atspi-2.0
EOF
fi

cat <<EOF

Setup completed.
Virtual environment: ${VENV_DIR}
Temporary source path used: ${TMP_BASE}

Run:
  source .venv/bin/activate
  python tests/desktop_demo.py

Set KEEP_TMP=1 before running this tests if you want to keep cloned sources in /tmp.
EOF
