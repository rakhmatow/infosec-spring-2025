#!/usr/bin/env bash

set -e  # Exit if any command fails to execute

sudo apt install git python3 zip make
git clone git@github.com:yt-dlp/yt-dlp.git --branch release
cd yt-dlp
make yt-dlp
echo Compiled! Find yt-dlp executable in ./yt-dlp/
