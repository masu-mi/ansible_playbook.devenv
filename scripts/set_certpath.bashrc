
base=${PROJ_TOP:-"${PWD}"}/scripts
echo [INFO] export SSL_CERT_FILE="$($base/certifi_path.py)"
export SSL_CERT_FILE="$($base/certifi_path.py)"
