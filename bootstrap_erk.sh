#!/usr/bin/env bash
set -e

########################################################
# Expert Knowledge Repository (EKR)
# One-command bootstrap for Ubuntu / OpenStack VM
# Author: Faisal (fa1829)
# Port: 7000 (non-5000, non-8080)
########################################################

APP_PORT=7000
APP_NAME="Expert Knowledge Repository"
APP_DIR="$(pwd)"
VENV_DIR="$APP_DIR/.venv"
DATA_ROOT="/data"
ADMIN_TOKEN_FILE="$APP_DIR/.ekr_admin_token"

echo "================================================="
echo "🧠 $APP_NAME — Bootstrap Script"
echo "================================================="

# ---------- OS CHECK ----------
if ! grep -qi ubuntu /etc/os-release; then
  echo "❌ Ubuntu required. Exiting."
  exit 1
fi

# ---------- SYSTEM DEPENDENCIES ----------
echo "[1/8] Installing system dependencies..."
sudo apt update -y
sudo apt install -y python3 python3-pip python3-venv curl openssl

# ---------- DATA DIRECTORIES ----------
echo "[2/8] Creating data directories..."
sudo mkdir -p \
  $DATA_ROOT/knowledge \
  $DATA_ROOT/courses \
  $DATA_ROOT/research

sudo chown -R $USER:$USER $DATA_ROOT

# ---------- PYTHON VENV ----------
echo "[3/8] Creating Python virtual environment..."
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

# ---------- PYTHON REQUIREMENTS ----------
echo "[4/8] Installing Python requirements..."
pip install --upgrade pip
pip install -r requirements.txt

# ---------- ENV VARIABLES ----------
echo "[5/8] Setting environment variables..."
ADMIN_TOKEN="$(openssl rand -hex 16)"
echo "$ADMIN_TOKEN" > "$ADMIN_TOKEN_FILE"
chmod 600 "$ADMIN_TOKEN_FILE"

export EKR_PORT=$APP_PORT
export EKR_SECRET_KEY="$(openssl rand -hex 24)"
export EKR_ADMIN_TOKEN="$ADMIN_TOKEN"

# ---------- SYSTEMD SERVICE ----------
echo "[6/8] Installing systemd service..."
SERVICE_FILE="/etc/systemd/system/ekr.service"

sudo tee "$SERVICE_FILE" > /dev/null <<EOF
[Unit]
Description=Expert Knowledge Repository
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$APP_DIR
Environment=EKR_PORT=$APP_PORT
Environment=EKR_SECRET_KEY=$EKR_SECRET_KEY
Environment=EKR_ADMIN_TOKEN=$EKR_ADMIN_TOKEN
ExecStart=$VENV_DIR/bin/python run.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable ekr
sudo systemctl restart ekr

# ---------- STATUS ----------
echo "[7/8] Verifying service..."
sleep 2
sudo systemctl --no-pager status ekr || true

# ---------- FINAL INFO ----------
PUBLIC_IP="$(curl -s ifconfig.me || hostname -I | awk '{print $1}')"

echo "[8/8] DONE ✅"
echo "================================================="
echo "🌍 Access URL:"
echo "   http://$PUBLIC_IP:$APP_PORT"
echo ""
echo "🔐 Admin token (SAVE THIS):"
echo "   $ADMIN_TOKEN"
echo ""
echo "📂 Knowledge paths:"
echo "   $DATA_ROOT/knowledge"
echo "   $DATA_ROOT/courses"
echo "   $DATA_ROOT/research"
echo ""
echo "🛠 Commands:"
echo "   sudo systemctl status ekr"
echo "   sudo systemctl restart ekr"
echo "   sudo journalctl -u ekr -f"
echo "================================================="
