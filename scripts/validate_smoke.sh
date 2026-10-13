#!/usr/bin/env bash
# Small end-to-end check; creates a dedicated run, preserving tutorial inputs.
set -euo pipefail
project_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
source "$project_root/.venv/bin/activate"
cd "$project_root"
bash scripts/run_generator.sh check_model
if [[ ! -d work/Material/Hvlvl_SM ]]; then
  bash scripts/run_generator.sh generate_sm
fi
cd "$project_root/work/Material"
run_name=smoke_sm_2000
if [[ ! -f "Hvlvl_SM/Events/$run_name/unweighted_events.lhe.gz" ]]; then
  if [[ -e "Hvlvl_SM/Events/$run_name" ]]; then
    echo 'An incomplete smoke run exists. Inspect it before retrying.' >&2
    exit 1
  fi
  cp param_card_Hvlvl.dat Hvlvl_SM/Cards/param_card.dat
  cp run_card_Hvlvl.dat Hvlvl_SM/Cards/run_card.dat
  cat > "$project_root/outputs/smoke_launch.mg5" <<'EOF'
set auto_update 0 --no_save
set run_mode 0 --no_save
launch Hvlvl_SM -n smoke_sm_2000
shower=OFF
detector=OFF
analysis=OFF
reweight=OFF
done
set nevents 2000
set iseed 12345
done
quit
EOF
  python "$project_root/tools/MG5_aMC_v2_9_27/bin/mg5_aMC" --debug \
    "$project_root/outputs/smoke_launch.mg5" 2>&1 | tee "$project_root/outputs/smoke_generation.log"
  if grep -Eiq 'Traceback|Error detected|InvalidCmd|Command .* interrupted' "$project_root/outputs/smoke_generation.log"; then
    echo 'Event generation reported an error; inspect the log.' >&2
    exit 1
  fi
fi
# Reweight this small sample for the cHl3 linear contribution only.
if ! gzip -cd "Hvlvl_SM/Events/$run_name/unweighted_events.lhe.gz" | grep "<wgt id=['\"]cHl3['\"]" >/dev/null; then
  cat > Hvlvl_SM/Cards/reweight_card.dat <<'EOF'
change process h > e- ve~ mu+ vm SMHLOOP=0 NPprop=0 NP=1 NP^2==1
launch --rwgt_name=cHl3
set cHbox 0
set cHW 0
set cHl3 1
set cHq3 0
set cll1 0
done
EOF
  ./Hvlvl_SM/bin/madevent reweight "$run_name" -f 2>&1 | tee "$project_root/outputs/smoke_reweight.log"
  if grep -Eiq 'Traceback|Error detected|InvalidCmd|Command .* interrupted' "$project_root/outputs/smoke_reweight.log"; then
    echo 'Reweighting reported an error; inspect the log.' >&2
    exit 1
  fi
fi
python "$project_root/scripts/validate_generated.py" \
  "Hvlvl_SM/Events/$run_name/unweighted_events.lhe.gz" "$project_root/outputs/smoke_validation.json"
