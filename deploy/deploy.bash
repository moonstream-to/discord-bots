#!/usr/bin/env bash

# Deployment script - intended to run Discord bots

# Colors
C_RESET='\033[0m'
C_RED='\033[1;31m'
C_GREEN='\033[1;32m'
C_YELLOW='\033[1;33m'

# Logs
PREFIX_INFO="${C_GREEN}[INFO]${C_RESET} [$(date +%d-%m\ %T)]"
PREFIX_WARN="${C_YELLOW}[WARN]${C_RESET} [$(date +%d-%m\ %T)]"
PREFIX_CRIT="${C_RED}[CRIT]${C_RESET} [$(date +%d-%m\ %T)]"

# Main
APP_DIR="${APP_DIR:-/home/ubuntu/discord-bots/librarian}"
PYTHON_ENV_DIR="${PYTHON_ENV_DIR:-/home/ubuntu/librarian-env}"
PYTHON="${PYTHON_ENV_DIR}/bin/python"
PIP="${PYTHON_ENV_DIR}/bin/pip"
SCRIPT_DIR="$(realpath $(dirname $0))"

# API server service file
LIBRARIAN_API_SERVICE_FILE="librarian.service"

set -eu

echo
echo
echo -e "${PREFIX_INFO} Upgrading Python pip and setuptools"
"${PIP}" install --upgrade pip setuptools

echo
echo
echo -e "${PREFIX_INFO} Installing Python dependencies"
"${PIP}" install -U -e "${APP_DIR}/"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Discord bots Librarian service definition with ${LIBRARIAN_API_SERVICE_FILE}"
chmod 644 "${SCRIPT_DIR}/${LIBRARIAN_API_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${LIBRARIAN_API_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${LIBRARIAN_API_SERVICE_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart "${LIBRARIAN_API_SERVICE_FILE}"
