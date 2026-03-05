#! /usr/bin/bash

TIME=`date +%m%d%H%M%S`

#打开系统自研应用如邮箱等
apps=("deepin-editor" "browser" "dde-file-manager" "deepin-terminal")

for app in "${apps[@]}"
do
	nohup bash -c "$app" &
	sleep 1
done

for ((i=1; i<=$1; i++))
do
	TTIME=`date +%m%d%H%M%S`
	top -b -d 5 -n 60 | grep "treeland" > ~/top-cpu.txt
	sleep 5
done

#关闭应用窗口
process=("deepin-editor" "browser" "dde-file-manager" )
for pcs in "${process[@]}"
do
	pkill "$pcs" &
	sleep 1
done
