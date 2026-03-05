#! /usr/bin/bash

TIME=`date +%m%d%H%M%S`

#打开系统自研应用
apps=( "deepin-movie" "deepin-music" "dman" "browser" "wps")

for app in "${apps[@]}"
do
	nohup bash -c "$app" &
	sleep 1
done

mv ~/test_switch_compositing_status.log ~/test_switch_compositing_status-$TIME.log
for ((i=1; i<=$1; i++))
do
  TTIME=`date +%m%d%H%M%S`
  pytest test_switch_compositing_status.py
	sleep 5
	echo "*******$TTIME:第$i次测试********" >> ~/test_switch_compositing_status.log
done

for pcs in "${apps[@]}"
do
	pkill "$pcs" &
	sleep 1
done
