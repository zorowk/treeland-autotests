#! /usr/bin/bash

TIME=`date +%m%d%H%M%S`

#preapps=("/usr/lib/cmclient/cmclient" "/usr/lib/unity-happypa/unity-happypa" "/opt/apps/cn.wps.wps-office-pro/files/bin/wps" "/opt/apps/cn.wps.wps-office-pro/files/bin/wpp" "/opt/apps/cn.wps.wps-office-pro/files/bin/wpspdf" "/opt/apps/cn.com.topsec.topdesk/files/TDABDGL2" "/opt/apps/cn.com.topsec.edragent/files/Edragent.sh")

#for preapp in "${preapps[@]}"
#do
#	nohup bash -c "$preapp" &
#	sleep 1
#done


#apps=("deepin-movie" "deepin-music" "dde-calendar" "dde-control-center -s" "dde-file-manager" "dde-introduction" "deepin-album" "deepin-calculator" "deepin-camera" "deepin-draw" "deepin-editor" "deepin-font-manager" "deepin-app-store" "deepin-image-viewer" "deepin-log-viewer" "deepin-reader" "deepin-system-monitor" "deepin-voice-note" "dman" "wps" )

#for app in "${apps[@]}"
#do
#	nohup bash -c "$app" &
#	sleep 1
#done

mv ~/apptab.log ~/apptab-$TIME.log
mv ~/top.log ~/top-$TIME.log



for ((i=1; i<=$1; i++))
do
	TTIME=`date +%m%d%H%M%S`

	pytest test_mouse_move_multiscreen.py & pytest test_tab_action.py

	top -o+%MEM -b -n 1 | grep ^top -A 50 >> ~/top.log

	echo "*******$TTIME:第$i次测试********" >> ~/apptab.log

	sleep 3
	killall browser
	sleep 2

done

#process=("deepin-movie" "deepin-music" "dde-calendar" "dde-control-center -s" "dde-file-manager" "dde-introductio" "deepin-album" "deepin-calculat" "deepin-camera" "deepin-draw" "deepin-editor" "deepin-font-man" "deepin-app-stor" "deepin-image-vi" "deepin-log-view" "deepin-reader" "deepin-system-m" "deepin-voice-no" "dman" "wps" "deepin-screen-recorder")

#for pcs in "${process[@]}"
#do
#	pkill "$pcs" &
#	sleep 1
#done

ps -ef | grep mouse_move | grep -v grep | awk '{print $2}' | xargs kill -9
ps -ef | grep tab_action | grep -v grep | awk '{print $2}' | xargs kill -9
