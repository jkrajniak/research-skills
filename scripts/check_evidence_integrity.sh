#!/usr/bin/env bash
# Verify that every artefact pinned in experiments/EVIDENCE_BASE.md
# still hashes to its recorded SHA-256.
#
# Run from the <proj>-research repo:
#   bash scripts/check_evidence_integrity.sh ..
# The argument is the workspace root (the directory containing
# <proj>-code/, <proj>-artifacts/, etc.) — defaults to one level up.
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/.." && pwd)"
workspace_root="$(cd "${repo_root}/${1:-..}" && pwd)"
evidence_file="${repo_root}/experiments/EVIDENCE_BASE.md"

if [[ ! -f "${evidence_file}" ]]; then
    echo "EVIDENCE_BASE.md not found at ${evidence_file}" >&2
    exit 1
fi

# Table rows whose path starts with <anything>-artifacts/ or <anything>-code/
# and whose SHA cell is 64 hex chars in backticks.
extract_entries() {
    awk -F'|' '
        /^\| *[^|]+ *\| *`[A-Za-z0-9_.-]+-(artifacts|code)\// {
            path=$3; gsub(/^[[:space:]]*`|`[[:space:]]*$/, "", path);
            sha=$5;  gsub(/^[[:space:]]*`|`[[:space:]]*$/, "", sha);
            if (length(sha) == 64) printf "%s\t%s\n", path, sha;
        }
    ' "$1"
}

failures=0
checked=0
while IFS=$'\t' read -r path expected; do
    [[ -z "${path}" ]] && continue
    checked=$((checked + 1))
    full="${workspace_root}/${path}"
    if [[ ! -f "${full}" ]]; then
        printf 'MISSING  %s\n' "${path}" >&2
        failures=$((failures + 1))
        continue
    fi
    actual="$(shasum -a 256 "${full}" | awk '{print $1}')"
    if [[ "${actual}" == "${expected}" ]]; then
        printf 'OK       %s\n' "${path}"
    else
        printf 'MISMATCH %s\n  expected %s\n  actual   %s\n' \
            "${path}" "${expected}" "${actual}" >&2
        failures=$((failures + 1))
    fi
done < <(extract_entries "${evidence_file}")

if [[ ${checked} -eq 0 ]]; then
    echo "No pinned artefacts with SHA-256 found in EVIDENCE_BASE.md (empty is OK until first pin)."
    exit 0
fi

if [[ ${failures} -gt 0 ]]; then
    printf '\n%d/%d pinned artefacts failed integrity check.\n' \
        "${failures}" "${checked}" >&2
    exit 1
fi

printf '\n%d/%d pinned artefacts verified.\n' "${checked}" "${checked}"
