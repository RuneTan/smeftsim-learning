#!/usr/bin/env bash
# Install only inside the project-specific Ubuntu guest; invoke as root.
set -euo pipefail
source_root="${1:?Pass the mounted Windows smeftsim directory}"
if [[ "$(id -u)" != 0 || "$(uname -s)" != Linux ]]; then
  echo 'Run as root inside the SMEFTsim Linux guest.' >&2
  exit 1
fi
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y --no-install-recommends python3 python3-venv python3-dev build-essential gfortran git perl ca-certificates
if ! id smeft >/dev/null 2>&1; then
  useradd --create-home --shell /bin/bash smeft
fi
python3 - <<'PY'
from pathlib import Path
import configparser
p = Path('/etc/wsl.conf')
c = configparser.ConfigParser()
c.read(p)
for section in ('user', 'interop'):
    if not c.has_section(section):
        c.add_section(section)
c.set('user', 'default', 'smeft')
c.set('interop', 'appendWindowsPath', 'false')
with p.open('w') as f:
    c.write(f)
PY
runuser -u smeft -- bash "$source_root/scripts/setup_linux.sh" /home/smeft/smeftsim
for name in validate_smoke.sh validate_generated.py; do
  install -o smeft -g smeft -m 644 "$source_root/scripts/$name" "/home/smeft/smeftsim/scripts/$name"
done
echo 'Guest dependencies installed; Windows Python packages were not touched.'
