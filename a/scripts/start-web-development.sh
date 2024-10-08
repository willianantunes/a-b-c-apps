#!/usr/bin/env bash

# https://www.willianantunes.com/blog/2021/05/production-ready-shell-startup-scripts-the-set-builtin/
set -e

./scripts/generate-migrations.sh
./scripts/apply-migrations.sh

dotnet watch --project ./src --launch-profile http
