#!/usr/bin/env sh

set -eu

ansible-galaxy role init --init-path ./roles/ $1
