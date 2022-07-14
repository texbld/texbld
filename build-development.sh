#!/bin/sh

nix-shell --run "poetry build" && nix-build
