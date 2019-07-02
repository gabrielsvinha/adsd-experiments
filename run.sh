#!/bin/bash
set -ex

source config

declare -a sizearr=(10 30)
dir="2"
mkdir -p results/$dir
mkdir -p output/

for times in 1 2 3 4 5; do
    for size in "${sizearr[@]}"; do
        echo $(date '+%y-%m-%d %H:%M:%S.%6N') >> logs/$size-$times-time.txt
	time ffmpeg -y -hwaccel cuvid -c:v h264_cuvid -i input/SampleVideo_1280x720_${size}mb.flv -c:v h264_nvenc output/tmp.mp4
	echo $(date '+%y-%m-%d %H:%M:%S.%6N') >> logs/$size-$times-time.txt
	python parse.py mp4 $size TRUE $times
    done
    rm -rf logs/*
done
rm -rf logs/*
# parse these results

for times in 1 2 3 4 5; do
    for size in "${sizearr[@]}"; do
	echo $(date '+%y-%m-%d %H:%M:%S.%6N') >> logs/$size-$times-time.txt
	time ffmpeg -y -hwaccel cuvid -c:v h264_cuvid -i input/SampleVideo_1280x720_${size}mb.flv -c:v h264_nvenc output/tmp.flv
	echo $(date '+%y-%m-%d %H:%M:%S.%6N') >> logs/$size-$times-time.txt
        python parse.py flv $size TRUE $times
    done
    rm -rf logs/*
done
rm -rf logs/*
# parse these results

for times in 1 2 3 4 5; do
    for size in "${sizearr[@]}"; do
	echo $(date '+%y-%m-%d %H:%M:%S.%6N') >> logs/$size-$times-time.txt
	time ffmpeg -y -i input/SampleVideo_1280x720_${size}mb.flv output/tmp.mp4
	echo $(date '+%y-%m-%d %H:%M:%S.%6N') >> logs/$size-$times-time.txt
        python parse.py mp4 $size FALSE $times
    done
    rm -rf logs/*
done
rm -rf logs/*
# parse these results

for times in 1 2 3 4 5; do
    for size in "${sizearr[@]}"; do
        echo $(date '+%y-%m-%d %H:%M:%S.%6N') >> logs/$size-$times-time.txt
	time ffmpeg -y -i input/SampleVideo_1280x720_${size}mb.flv output/tmp.flv
	echo $(date '+%y-%m-%d %H:%M:%S.%6N') >> logs/$size-$times-time.txt
        python parse.py flv $size FALSE $times
    done
    rm -rf logs/*
done
rm -rf logs/*
# parse these results

