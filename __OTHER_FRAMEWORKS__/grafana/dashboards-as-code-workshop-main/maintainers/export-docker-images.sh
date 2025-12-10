#!/bin/env bash

# Exit on error. Append "|| true" if you expect an error.
set -o errexit
# Exit on error inside any functions or subshells.
set -o errtrace
# Do not allow use of undefined vars. Use ${VAR:-} to use an undefined VAR
set -o nounset
# Catch the error in case mysqldump fails (but gzip succeeds) in `mysqldump |gzip`
set -o pipefail

__dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cat "$__dir/../docker-compose.yaml" | yq -r '.services | to_entries[] | select(.value | .image != null) | [.key, .value.image] | @tsv' |
while IFS=$'\t' read -r name image_ref; do
    clean_ref=${image_ref//'${REGISTRY:-docker.io}/'/}

    echo "Saving $clean_ref as $name.tar"
    echo docker save -o "$name.tar" "$clean_ref"
    docker save -o "$name.tar" "$clean_ref"
done
