pid=`ps aux|grep test|grep python | awk '{print $2}'`
echo $pid
pstree -p $pid
