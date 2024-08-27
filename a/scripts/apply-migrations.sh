#!/usr/bin/env bash

# https://www.willianantunes.com/blog/2021/05/production-ready-shell-startup-scripts-the-set-builtin/
set -eu -o pipefail

CSPROJ_PATH=./src

echo "### Applying migrations 🤙"
dotnet ef database update --project $CSPROJ_PATH
