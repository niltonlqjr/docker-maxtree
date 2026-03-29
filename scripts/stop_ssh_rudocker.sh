dir_script=$1

time=3

if [ -z $1 ]
then
    echo "Usage: $0 directory"
    echo "where <directory> is the directory that contains scritp to start container"
    exit 1
fi

echo "stopping ssh service, changing directory to '${dir_script}' and running script in ${time} seconds"
for i in `seq ${time} -1 1`
do
    sleep 1
    echo "$i seconds"
done

sudo service ssh stop
cd ${dir_script} 
./run-container-host-non-interative.sh
