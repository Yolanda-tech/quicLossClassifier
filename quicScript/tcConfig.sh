#!/bin/bash

echo "$IFB"

usage()
{
cat << EOF
USAGE: $0 [-hcs] [-a <adapter>] [-d <rate>] 

Limit the bandwidth of an adapter

OPTIONS:
   -h           Show this message
   -a <adapter> Set the adapter
   -d <rate>    Set maximum download rate (in Kbps) and/or
   -c           Clear the limits from adapter
   -s           Show the current status of adapter
   -l <lossR>   Set the loss rate(%)
   -e <delayMS> Set the delay(ms)

MODES:
   tcConfig -a <adapter> -d <rate> -l <lossR> -e <delayMS>
   tcConfig -c -a <adapter>
   tcConfig -s -a <adapter>

EXAMPLES:
   tcConfig -a eth0 -d 1024 -l 5 -e 500
   tcConfig -a eth0 -d 512
   tcConfig -c -a eth0

EOF
}

DSPEED=
IFACE=
IFB="ifb0"
MODE=
LOSSRATE=
DELAY=

while getopts d:l:e:a:cs o
do  case "$o" in
    d)      DSPEED=$OPTARG;;
    l)      LOSSRATE=$OPTARG;;
    e)      DELAY=$OPTARG;;
    a)      IFACE=$OPTARG;;
    c)      MODE="clear";;
    s)      MODE="status";;
    [?])    usage
            exit 1;;
    esac
done

if [[ ! -z $MODE ]] && [[ -z $IFACE ]]
then
    echo "Please supply the adapter name for the mode."
    echo ""
    usage
    exit 1
fi

if [ "$MODE" = "status" ]
then
    tc -s qdisc ls dev $IFACE
    tc -s class ls dev $IFACE
    exit
fi

if [ "$MODE" = "clear" ]
then
    echo "clear..."
    tc qdisc del dev $IFACE root    2> /dev/null > /dev/null
    tc qdisc del dev $IFACE ingress 2> /dev/null > /dev/null
    tc qdisc del dev $IFB   root    2> /dev/null > /dev/null
    tc qdisc del dev $IFB   ingress 2> /dev/null > /dev/null
    exit
fi

if [[ -z $DELAY ]] || [[ -z $LOSSRATE ]] || [[ -z $IFACE ]]
then
    echo "Please supply the adapter name, delay time and loss rate."
    echo ""
    usage
    exit 1
fi
########## downlink #############
# slow downloads down to somewhat less than the real speed  to prevent
# queuing at our ISP. Tune to see how high you can set it.
# ISPs tend to have *huge* queues to make sure big downloads are fast
#
# attach ingress policer:
if [[ ! -z $DSPEED ]]
then

    # Add the IFB interface
    modprobe ifb numifbs=1
    ip link set dev $IFB up

    # Redirect ingress (incoming) to egress ifb0
    tc qdisc add dev $IFACE handle ffff: ingress
    tc filter add dev $IFACE parent ffff: protocol ip u32 match u32 0 0 \
        action mirred egress redirect dev $IFB
    
    # Add class and rules for virtual
    tc qdisc add dev $IFB root handle 2: htb
    tc class add dev $IFB parent 2: classid 2:1 htb rate ${DSPEED}kbit
    
    # Add filter to rule for IP address
    tc filter add dev $IFB protocol ip parent 2: prio 1 u32 match ip src 0.0.0.0/0 flowid 2:1
    
fi

########## downlink #############
# slow downloads down to somewhat less than the real speed  to prevent
# queuing at our ISP. Tune to see how high you can set it.
# ISPs tend to have *huge* queues to make sure big downloads are fast
#
# attach ingress policer:
if [[ ! -z $LOSSRATE ]] && [[ ! -z $DELAY ]]
then

    # Add the IFB interface
    modprobe ifb numifbs=1
    ip link set dev $IFB up

    # Redirect ingress (incoming) to egress ifb0
    tc qdisc add dev $IFACE handle ffff: ingress
    tc filter add dev $IFACE parent ffff: protocol ip u32 match u32 0 0 \
        action mirred egress redirect dev $IFB
    
    # Add class and rules for virtual
    tc qdisc add dev $IFB root handle 2: netem delay ${DELAY}ms loss ${LOSSRATE}% 
    # tc qdisc add dev $IFB root handle 2: htb
    # tc class add dev $IFB parent 2: classid 2:1 htb rate ${DSPEED}kbit
    
    # Add filter to rule for IP address
    tc filter add dev $IFB protocol ip parent 2: prio 1 u32 match ip src 114.115/16 flowid 2:1
    
fi