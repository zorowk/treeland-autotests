#! /usr/bin/bash

TIME=`date +%m%d%H%M%S`

#打开系统自研应用如邮箱等
apps=("deepin-mail" "deepin-movie" "deepin-music" "dde-calendar" "dde-control-center -s" "dde-file-manager" "dde-introduction" "deepin-album" "deepin-calculator" "deepin-camera" "deepin-draw" "deepin-editor" "deepin-font-manager"  "deepin-image-viewer" "deepin-log-viewer" "deepin-system-monitor" "deepin-voice-note" "dman" "wps" "wpp" "wpspdf")
# 去掉"deepin-reader" "deepin-app-store"

for app in "${apps[@]}"
do
	nohup bash -c "$app" &
	sleep 1
done

mv ~/apptab.log ~/apptab-$TIME.log
mv ~/top.log ~/top-$TIME.log

for ((i=1; i<=$1; i++))
	do
	process2=( "wps" "wpp" "wpspdf" "browser" "deepin-terminal" "et")
		for pcs2 in "${process2[@]}"
		do
			nohup bash -c "$pcs2" &
			sleep 1
		done
	TTIME=`date +%m%d%H%M%S`
	
	pytest test_treeland_stress.py
	top -o+%MEM -b -n 1 | grep ^top -A 50 >> ~/top.log
	echo "*******$TTIME:第$i次测试********" >> ~/apptab.log
	sleep 3

	process1=( "wps" "wpp" "wpspdf" "browser" "deepin-terminal" "et")
	for pcs1 in "${process1[@]}"
	do
		pkill "$pcs1" &
		sleep 1
	done
done

process=("deepin-mail" "deepin-movie" "deepin-music" "dde-calendar" "dde-control-center -s" "dde-file-manager" "dde-introductio" "deepin-album" "deepin-calculat" "deepin-camera" "deepin-draw" "deepin-editor" "deepin-font-man" "deepin-image-vi" "deepin-log-view" "deepin-system-m" "deepin-voice-no" "dman" "wps" "wpp" "wpspdf" )
#去掉截图录屏"deepin-screen-recorder"  "deepin-reader" "deepin-app-store"
#浏览器：browser
for pcs in "${process[@]}"
do
	pkill "$pcs" &
	sleep 1
done

ps -ef | grep mouse_move | grep -v grep | awk '{print $2}' | xargs kill -9
ps -ef | grep tab_action | grep -v grep | awk '{print $2}' | xargs kill -9



