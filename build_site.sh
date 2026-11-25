#!/usr/bin/env bash
# Stages recipe markdown files and images into docs/ and builds the site with Zensical.
set -euo pipefail
rm -rf docs site
mkdir -p docs
cp -r images docs/images
for f in *.md; do
  [ "$f" = "README.md" ] && continue
  cp "$f" docs/
done
cp README.md docs/index.md
zensical build --clean
