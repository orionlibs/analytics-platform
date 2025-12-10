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

DEST_REGISTRY="localhost:5000"

cat "$__dir/../docker-compose.yaml" | yq -r '.services | to_entries[] | select(.value | .image != null) | [.key, .value.image] | @tsv' |
while IFS=$'\t' read -r name image_ref; do
    clean_ref=${image_ref//'${REGISTRY:-docker.io}/'/}
    push_ref=$(echo $clean_ref | cut -d '@' -f1)

    echo docker tag "$clean_ref" "$DEST_REGISTRY/$push_ref"
    docker tag "$clean_ref" "$DEST_REGISTRY/$push_ref"

    echo docker push "$DEST_REGISTRY/$push_ref"
    docker push "$DEST_REGISTRY/$push_ref"
done
