#!/usr/bin/env bash

set -euo pipefail

workfile=$(mktemp)
tmpfile=$(mktemp)

# remove all exports
jq '.exports = {}' package.json > $workfile

# find all packages
for x in $(find ./src -type f); do
    base=${x:5:-3}
  jq '.exports[".'$base'"] = {
  types: "./dist'$base'.d.ts",
  import: "./dist'$base'.mjs",
  require: "./dist'$base'.js",
}' $workfile > $tmpfile
  mv $tmpfile $workfile
done

mv $workfile package.json
