#!/bin/bash

BIN_DIR=$(cd $(dirname $0); pwd)
source ${BIN_DIR}/../env/bin/activate

python ${BIN_DIR}/fetch_video_info.py