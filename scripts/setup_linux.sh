#!/usr/bin/env bash
# Run under Ubuntu 22.04 / Linux with Python 3.10 or 3.11.
# System prerequisites are explicit; this script never invokes sudo.
set -euo pipefail
source_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
task_target="${1:-$HOME/smeftsim}"
if [[ "$(uname -s)" != Linux ]]; then
  echo 'Run this script inside Ubuntu/WSL, not Windows Git Bash.' >&2
  exit 1
fi
for command in python3 git make gcc gfortran perl; do
  if ! command -v "$command" >/dev/null 2>&1; then
    echo "Missing $command. Install the prerequisites listed in handbook.md." >&2
    exit 1
  fi
done
python3 -c 'import sys; assert sys.version_info[:2] in ((3,10),(3,11)), "Use Python 3.10/3.11 for this MG 2.9 reweighting setup"'
mkdir -p "$task_target"
task_target="$(cd -- "$task_target" && pwd)"
if [[ "$task_target" == "$source_root" || "$task_target" == *" "* ]]; then
  echo 'Choose a separate Linux directory without spaces, e.g. ~/smeftsim.' >&2
  exit 1
fi
case "$task_target" in /mnt/*)
  echo 'Use the Linux filesystem, e.g. ~/smeftsim, rather than /mnt/c.' >&2
  exit 1 ;;
esac
# Do not overwrite another installation or copy a Windows virtual environment.
if [[ ! -d "$task_target/tutorial" ]]; then
  cp -a "$source_root/tutorial" "$task_target/tutorial"
fi
mkdir -p "$task_target/scripts" "$task_target/cards" "$task_target/tools" "$task_target/outputs"
for name in prepare_work.py run_generator.sh; do
  if [[ ! -e "$task_target/scripts/$name" ]]; then
    cp "$source_root/scripts/$name" "$task_target/scripts/$name"
  fi
done
for path in "$source_root"/cards/*.mg5; do
  if [[ ! -e "$task_target/cards/$(basename -- "$path")" ]]; then
    cp "$path" "$task_target/cards/"
  fi
done
for name in requirements-linux.txt requirements-generator.txt requirements-root.txt; do
  cp "$source_root/$name" "$task_target/$name"
done
mg_dir="$task_target/tools/MG5_aMC_v2_9_27"
if [[ ! -d "$mg_dir" ]]; then
  # A fresh Linux checkout restores symlinks that Windows stored as plain text.
  # Trust only this read-only source for this command; do not change global Git config.
  git -c safe.directory="$source_root/tools/MG5_aMC_v2_9_27" \
      -c safe.directory="$source_root/tools/MG5_aMC_v2_9_27/.git" \
      -c core.symlinks=true clone --no-hardlinks "$source_root/tools/MG5_aMC_v2_9_27" "$mg_dir"
fi
expected_commit=eb76cab72b8d44aac7162ac7221ac08a4384a169
if [[ "$(git -C "$mg_dir" rev-parse HEAD)" != "$expected_commit" ]]; then
  echo 'Existing MadGraph checkout has a different commit; inspect it first.' >&2
  exit 1
fi
if [[ ! -L "$mg_dir/madgraph/VERSION" ]]; then
  echo 'MadGraph symlinks were not restored; use a fresh Linux checkout.' >&2
  exit 1
fi
if [[ ! -e "$mg_dir/input/mg5_configuration.txt" ]]; then
  printf 'auto_update = 0\n' > "$mg_dir/input/mg5_configuration.txt"
fi
if [[ ! -e "$task_target/.venv/bin/python" ]]; then
  python3 -m venv "$task_target/.venv"
fi
mkdir -p "$task_target/outputs/setup-tmp"
TMPDIR="$task_target/outputs/setup-tmp" "$task_target/.venv/bin/python" -m pip install --no-cache-dir --index-url https://pypi.org/simple -r "$task_target/requirements-linux.txt"
"$task_target/.venv/bin/python" -m pip check

# ROOT image backends need two system libraries absent from minimal Ubuntu.
# Download and unpack into this project; do not install system packages.
root_libraries="$task_target/.venv/local-libs/usr/lib/x86_64-linux-gnu"
if [[ ! -f "$root_libraries/libSM.so.6" || ! -f "$root_libraries/libICE.so.6" ]]; then
  mkdir -p "$task_target/outputs/root-runtime-downloads" "$task_target/.venv/local-libs"
  (
    cd "$task_target/outputs/root-runtime-downloads"
    apt-get download libsm6 libice6
    for archive in *.deb; do
      dpkg-deb -x "$archive" "$task_target/.venv/local-libs"
    done
  )
fi
# Activate project libraries only in this environment, with deactivate restore.
"$task_target/.venv/bin/python" - "$task_target/.venv/bin/activate" <<'PYROOT_ACTIVATE'
from pathlib import Path
import sys
path = Path(sys.argv[1])
text = path.read_text()
if "_SMEFTSIM_PROJECT_LD_LIBRARY_PATH_SET" not in text:
    restore = """
    if [ "${_SMEFTSIM_PROJECT_LD_LIBRARY_PATH_SET-}" = "1" ]; then
        LD_LIBRARY_PATH="${_SMEFTSIM_PROJECT_OLD_LD_LIBRARY_PATH-}"
        export LD_LIBRARY_PATH
    elif [ "${_SMEFTSIM_PROJECT_LD_LIBRARY_PATH_SET-}" = "0" ]; then
        unset LD_LIBRARY_PATH
    fi
    unset _SMEFTSIM_PROJECT_LD_LIBRARY_PATH_SET _SMEFTSIM_PROJECT_OLD_LD_LIBRARY_PATH

"""
    text = text.replace("deactivate () {\n", "deactivate () {\n" + restore, 1)
    text += """
# Project-only ROOT graphics dependencies; restored by deactivate().
if [ "${LD_LIBRARY_PATH+defined}" = "defined" ]; then
    _SMEFTSIM_PROJECT_LD_LIBRARY_PATH_SET=1
    _SMEFTSIM_PROJECT_OLD_LD_LIBRARY_PATH="$LD_LIBRARY_PATH"
else
    _SMEFTSIM_PROJECT_LD_LIBRARY_PATH_SET=0
    _SMEFTSIM_PROJECT_OLD_LD_LIBRARY_PATH=""
fi
LD_LIBRARY_PATH="$VIRTUAL_ENV/local-libs/usr/lib/x86_64-linux-gnu${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export LD_LIBRARY_PATH
"""
    path.write_text(text)
PYROOT_ACTIVATE
"$task_target/.venv/bin/python" "$task_target/scripts/prepare_work.py"
if [[ -d "$source_root/work/Material/pyroot_python3" && ! -e "$task_target/work/Material/pyroot_python3" ]]; then
  cp -a "$source_root/work/Material/pyroot_python3" "$task_target/work/Material/pyroot_python3"
fi
echo "Environment prepared at $task_target. No events have been generated."
echo "Next: cd '$task_target' && bash scripts/run_generator.sh check_model"
