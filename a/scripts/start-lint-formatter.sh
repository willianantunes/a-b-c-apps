#!/usr/bin/env bash

set -e

dotnet format --verbosity d

dotnet format --verify-no-changes --verbosity d
