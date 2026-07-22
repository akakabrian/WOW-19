#!/usr/bin/env bash
# Run the complete isolated WOWII-19 port and preserve every result locally.
set -uo pipefail

ROOT="$(pwd)"
OUT="$ROOT/ci-output"
FORMAL="$ROOT/formal-conjectures"
AMRA="$ROOT/amra"
FORMAL_COMMIT="${FORMAL_CONJECTURES_COMMIT:-e923379e609b9d5987011a1d1f06ec22ea25cd20}"
AMRA_COMMIT="${AMRA_COMMIT:-e4e339e5b380375cf1c7838251966d0fc3c06929}"

rm -rf "$OUT" "$FORMAL" "$AMRA"
mkdir -p "$OUT/generated"
exec > >(tee "$OUT/ci.log") 2>&1

FAILED_PHASE=""
EXIT_CODE=0

run_phase() {
  local name="$1"
  shift
  echo
  echo "===== PHASE: $name ====="
  "$@"
  local rc=$?
  if (( rc != 0 )); then
    FAILED_PHASE="$name"
    EXIT_CODE=$rc
    echo "PHASE FAILED: $name (exit $rc)"
    return "$rc"
  fi
  echo "PHASE PASSED: $name"
  return 0
}

install_lean() {
  curl -sSf https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh \
    | sh -s -- -y --default-toolchain none
  export PATH="$HOME/.elan/bin:$PATH"
  elan --version
}

fetch_sources() {
  git init "$FORMAL"
  git -C "$FORMAL" remote add origin \
    https://github.com/google-deepmind/formal-conjectures.git
  git -C "$FORMAL" fetch --depth=1 origin "$FORMAL_COMMIT"
  git -C "$FORMAL" checkout --detach FETCH_HEAD

  git init "$AMRA"
  git -C "$AMRA" remote add origin https://github.com/chainstart/amra.git
  git -C "$AMRA" fetch --depth=1 origin "$AMRA_COMMIT"
  git -C "$AMRA" checkout --detach FETCH_HEAD

  test "$(git -C "$FORMAL" rev-parse HEAD)" = "$FORMAL_COMMIT"
  test "$(git -C "$AMRA" rev-parse HEAD)" = "$AMRA_COMMIT"
}

generate_port() {
  python3 -m py_compile scripts/generate_lean_port.py
  python3 scripts/generate_lean_port.py --formal "$FORMAL" --amra "$AMRA"

  local files=(
    "$FORMAL/FormalConjectures/WrittenOnTheWallII/GraphConjecture19BipartiteSupport.lean"
    "$FORMAL/FormalConjectures/WrittenOnTheWallII/GraphConjecture19Conjecture13Support.lean"
    "$FORMAL/FormalConjectures/WrittenOnTheWallII/GraphConjecture19Solved.lean"
  )
  if grep -RInE '\b(sorry|admit|axiom)\b' "${files[@]}"; then
    echo "forbidden marker detected"
    return 91
  fi
  cp "${files[@]}" "$OUT/generated/"
}

record_environment() {
  export PATH="$HOME/.elan/bin:$PATH"
  cd "$FORMAL"
  cat lean-toolchain | tee "$OUT/lean-toolchain.txt"
  grep -n '"name": "mathlib"' -A8 lake-manifest.json \
    | tee "$OUT/mathlib-manifest.txt"
  lake --version | tee "$OUT/lake-version.txt"
  lean --version | tee "$OUT/lean-version.txt"
}

get_cache() {
  export PATH="$HOME/.elan/bin:$PATH"
  cd "$FORMAL"
  lake exe cache get
}

kernel_check() {
  export PATH="$HOME/.elan/bin:$PATH"
  cd "$FORMAL"
  set +o pipefail
  lake env lean \
    FormalConjectures/WrittenOnTheWallII/GraphConjecture19Solved.lean \
    2>&1 | tee "$OUT/lean-build.log"
  local rc=${PIPESTATUS[0]}
  set -o pipefail
  return "$rc"
}

if ! run_phase install-lean install_lean; then :
elif ! run_phase fetch-pinned-sources fetch_sources; then :
elif ! run_phase generate-port generate_port; then :
elif ! run_phase record-environment record_environment; then :
elif ! run_phase download-mathlib-cache get_cache; then :
elif ! run_phase kernel-check kernel_check; then :
else
  FAILED_PHASE="none"
  EXIT_CODE=0
fi

printf '%s\n' "$EXIT_CODE" > "$OUT/exit_code"
printf '%s\n' "$FAILED_PHASE" > "$OUT/failed_phase"

{
  echo "# WOW II Conjecture 19 — Latest CI Result"
  echo
  echo "- Repository commit: \`${GITHUB_SHA:-local}\`"
  echo "- Formal Conjectures commit: \`$FORMAL_COMMIT\`"
  echo "- AMRA proof commit: \`$AMRA_COMMIT\`"
  echo "- Failed phase: \`$FAILED_PHASE\`"
  echo "- Exit code: \`$EXIT_CODE\`"
  echo "- UTC completion: \`$(date -u +%Y-%m-%dT%H:%M:%SZ)\`"
  echo
  if (( EXIT_CODE == 0 )); then
    echo "## Result"
    echo
    echo "**PASS — the unchanged authoritative theorem was kernel-checked without sorry/admit/axiom.**"
  else
    echo "## Result"
    echo
    echo "**OPEN — the port failed in phase \`$FAILED_PHASE\`. See \`ci.log\` and \`lean-build.log\`.**"
    echo
    echo "## Log tail"
    echo
    echo '```text'
    tail -n 160 "$OUT/ci.log" || true
    echo '```'
  fi
} > "$OUT/CI_RESULT.md"

find "$OUT" -maxdepth 2 -type f -print -exec sha256sum {} \; | sort \
  > "$OUT/SHA256SUMS.txt"

cat "$OUT/CI_RESULT.md"
exit "$EXIT_CODE"
