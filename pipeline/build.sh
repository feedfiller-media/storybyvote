#!/bin/bash
# Build one episode.  usage: pipeline/build.sh N [align|test "t1,t2,..."|render]
# Work dir: /tmp/sbv_epN. It must contain voice.mp3 (ElevenLabs, pauses already shortened).
# Needs: pipeline/episodes/epN_script.txt and pipeline/episodes/epN_scenes.py
set -e
N=$1; STEP=${2:-render}; P=$(cd "$(dirname "$0")" && pwd); W=/tmp/sbv_ep$N
mkdir -p $W && cd $W
cp -r $P/assets $P/sfx $P/fonts . 2>/dev/null || true
cp $P/align.py . && cp $P/episodes/ep${N}_script.txt script.txt
cat $P/base.py $P/hudcap.py $P/gen_top.py $P/zzz.py $P/ep3_lib.py $P/ep4_parts.py $P/ep5_parts.py $P/episodes/ep${N}_scenes.py $P/gen_render.py > make.py
[ -f v16.wav ] || ffmpeg -v error -y -i voice.mp3 -ac 1 -ar 16000 v16.wav
case $STEP in
  align)  rm -f timing_aligned.json; TEST=1 python3 make.py >/dev/null 2>&1 || true; python3 align.py | grep fail ;;
  test)   TEST="$3" python3 make.py | tail -1 ;;
  render) OUT=$W/ep$N.mp4 python3 make.py | tail -1 ;;
esac
