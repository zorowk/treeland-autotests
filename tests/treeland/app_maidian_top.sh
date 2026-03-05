#! /usr/bin/bash

TIME=`date +%m%d%H%M%S`

mv ~/maidian.log ~/maidian-$TIME.log
mv ~/top.log ~/top-$TIME.log



for ((i=1; i<=$1; i++))
do
	TTIME=`date +%m%d%H%M%S`

	pytest test_mouse_move_multiscreen.py & pytest test_tab_action.py
 	sleep 1
	pytest test_screenshot.py

	top -o+%MEM -b -n 1 | grep ^top -A 50 >> ~/top.log

	echo "*******$TTIME:第$i次测试********" >> ~/maidian.log

	sleep 2
	killall deepin-screen-recorder browser
	sleep 2
done


ps -ef | grep mouse_move_multiscreen | grep -v grep | awk '{print $2}' | xargs kill -9
ps -ef | grep tab_action | grep -v grep | awk '{print $2}' | xargs kill -9
