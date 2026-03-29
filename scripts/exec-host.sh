FILE_CMD='container_command.txt'
sudo ls
while true;
do
    sleep 1
    CMD=`cat ${FILE_CMD}`
    $CMD
    echo '' > ${FILE_CMD}
    sudo -v
done