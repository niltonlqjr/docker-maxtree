if [ -z $1 ]
then
    echo "Usage: $0 <ip>"
    exit 1
fi

ip=$1

interface=`ifconfig | grep -B1 $ip | grep -o "^\w*"`
if [ -z $interface ]
then
    echo "interface for ip $ip not found"
    exit 1
else
    echo "interface for ip $ip is $interface"
    sudo echo "btl_tcp_if_include = $interface" >> /usr/local/etc/openmpi-mca-params.conf
    sudo echo "oob_tcp_if_include = $interface" >> /usr/local/etc/openmpi-mca-params.conf
    echo "interface $interface added to /usr/local/etc/opempi-mca-parans.conf"
fi
