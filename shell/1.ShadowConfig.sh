#!/bin/bash

function CreateConfigFile() {
    serverip=$1
    serverport=$2
    serverpasswd=$3
    localport=$4
    action=$5
    config=""
    client_config="{\n\t\"server\":\"${serverip}\",\n\t\"server_port\":${serverport},\n\t\"local_port\":${localport},\n\t\"password\":\"${serverpasswd}\",\n\t\"time    out\":600,\n\t\"method\":\"aes-256-cfb\"\n}"
    server_config="{\n\t\"server\":\"${serverip}\",\n\t\"server_port\":${serverport},\n\t\"local_port\":${localport},\n\t\"password\":\"${serverpasswd}\",\n\t\"time    out\":600,\n\t\"method\":\"aes-256-cfb\"\n}"
    if [[ "${action}x" == "0x" ]]; then
        # action: 0 ---> build server
        # else           build client
        config=${server_config}
    else
        config=${client_config}
    fi

    # Create file in /etc
    echo -e ${config} > /etc/shadowsocks.json
}
function BuildEnv() {
apt-get install python-pip
    export LC_ALL="en_US.UTF-8"
    dpkg-reconfigure locales
    pip install --upgrade pip
    pip install setuptools
    pip install git+https://github.com/shadowsocks/shadowsocks.git@master
}

function usage() {
    echo $1
    echo -e "Usage: ShadowConfig [Options argument]\n"\
            "Command option and parameter:\n"\
            "\t--sport port | [port_1,port_2, ..., port_n]\n"\
            "\t--lport port | [port_1,port_2, ..., port_n]\n"\
            "\t--sip ip|url"\
            "\t--lip ip\n"\
            "\t--passwd password-str"
    exit 2

}

function main() {
    # Wait user input
    args=`getopt -l sport:,lport:,sip:,lip:,passwd: $*`
    # Command parameter
    # sport port | [port_1,port_2, ..., port_n]
    # lport port | [port_1,port_2, ..., port_n]
    # sip ip|url
    # lip ip
    # passwd password-str
    if [[ $? != 0 ]]; then
        usage
    fi
    eval set -- $args

    for i
    do
        echo "i:"$args
        case "$i"
            in
            --sport)
            shift;shift;
            echo $1 $2
            ;;
            --lport)
            shift;shift;
            echo $1 $2
            ;;
            --sip)
            shift;shift;
            echo $1 $2
            ;;
            --lip)
            shift;shift;
            ;;
            --passwd)
            shift;shift;
            ;;
        esac
    done
}

main $@

