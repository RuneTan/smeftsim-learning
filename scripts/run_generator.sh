#!/usr/bin/env bash
set -euo pipefail
project_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
stage="${1:-check_model}"
case "$stage" in
  check_model|generate_sm|generate_eft) ;;
  *) echo 'Choose check_model, generate_sm, or generate_eft.' >&2; exit 1 ;;
esac
if [[ "$(uname -s)" != Linux ]]; then
  echo 'Event generation requires Linux/WSL.' >&2
  exit 1
fi
if [[ ! -x "$project_root/.venv/bin/python" ]]; then
  echo 'Run setup_linux.sh first.' >&2
  exit 1
fi
source "$project_root/.venv/bin/activate"
python "$project_root/scripts/prepare_work.py"
mkdir -p "$project_root/outputs"
cd "$project_root/work/Material"
if [[ "$stage" == generate_sm && -e Hvlvl_SM ]]; then
  echo 'Hvlvl_SM already exists; inspect or rename it before generating another process.' >&2
  exit 1
fi
if [[ "$stage" == generate_eft ]]; then
  for name in Hvlvl_SMEFT Hvlvl_SMEFT_linear Hvlvl_SMEFT_prop; do
    if [[ -e "$name" ]]; then
      echo "$name already exists; inspect or rename it first." >&2
      exit 1
    fi
  done
fi
python "$project_root/tools/MG5_aMC_v2_9_27/bin/mg5_aMC" --debug \
  "$project_root/cards/$stage.mg5" 2>&1 | tee "$project_root/outputs/$stage.log"
# MadGraph can report command errors while returning zero; inspect the log too.
if grep -Eiq 'Traceback|Error detected|InvalidCmd|Command .* interrupted' "$project_root/outputs/$stage.log"; then
  echo 'MadGraph reported an error; inspect the stage log.' >&2
  exit 1
fi
if [[ "$stage" == generate_sm && ! -d Hvlvl_SM/Cards ]]; then
  echo 'SM process export is missing.' >&2
  exit 1
fi
if [[ "$stage" == generate_eft ]]; then
  for name in Hvlvl_SMEFT Hvlvl_SMEFT_linear Hvlvl_SMEFT_prop; do
    [[ -d "$name/Cards" ]] || { echo "Missing $name/Cards" >&2; exit 1; }
  done
fi
if [[ "$stage" == check_model ]]; then
  echo 'Read the log to confirm the UFO import and all four process generations succeeded.'
else
  echo 'Process source exported. Follow handbook.md to copy cards and generate events.'
fi
