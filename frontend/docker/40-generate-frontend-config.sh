#!/bin/sh
set -eu

CONFIG_FILE=/usr/share/nginx/html/js/config.js
GATEWAY_URL="${GATEWAY_PUBLIC_URL:-http://localhost:8080}"

cat > "$CONFIG_FILE" <<EOF
window.APP_CONFIG = {
  gatewayBaseUrl: "${GATEWAY_URL}",
};
EOF

echo "[entrypoint] frontend/js/config.js regenerado con gatewayBaseUrl=${GATEWAY_URL}"
