#!/bin/bash

oper_file="/usr/bin/kwin_no_scale"
append_list=(
	'cp $HOME/kwin.log $HOME/kwin-old-$timestamp.log'
	'timestamp=$(date +%Y%m%d-%H%M%S)'
)
append_log_rules='export QT_LOGGING_RULES="*.debug=true"'
execute_path="kwin_x11 -platform"
append_log_output=' > $HOME\/kwin.log 2>\&1'

function searchStr(){
	if [ `grep -c "$1" $oper_file` -ne '0' ]; then
    		return 1
	else
		return 0
	fi
}

#重命名kwin.log
for conf in "${append_list[@]}";
do
	sed -i "2a\\$conf" $oper_file
done

#添加log rules
searchStr "QT_LOGGING_RULES"
if [ $? = 0 ]
then
	sed -i "/$execute_path/i\\$append_log_rules" $oper_file
fi

#添加日志导出
searchStr "\$HOME\/kwin.log 2>&1"
if [ $? = 0 ]
then
	sed -i "$ s/$/ $append_log_output/" $oper_file
fi



