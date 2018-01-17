#!/bin/bash

function CreateConfigFile() {
    serverip=$1
    serverport=$2
    serverpasswd=$3
    localport=$4
    action=$5
    config=""
    client_config="{\n\t\"server\":\"${serverip}\",\n\t\"server_port\":${serverport},\n\t\"local_port\":${localport},\n\t\"password\":\"${serverpasswd}\",\n\t\"timeout\":600,\n\t\"method\":\"aes-256-cfb\"\n}"
    server_config="{\n\t\"server\":\"${serverip}\",\n\t\"server_port\":${serverport},\n\t\"local_port\":${localport},\n\t\"password\":\"${serverpasswd}\",\n\t\"timeout\":600,\n\t\"method\":\"aes-256-cfb\"\n}"
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
            "\t--sport={port | [port_1,port_2, ..., port_n]}\n"\
            "\t--lport={port | [port_1,port_2, ..., port_n]}\n"\
            "\t--sip=[ip|url]"\
            "\t--lip=ip\n"\
            "\t--passwd password-str\n"\
            "Server config example:\n"\
            "\tsudo ./ShadowConfig --sport=[80,81,82,83] --sip=0.0.0.0 --passwd=example\n"\
            "Client config example:\n"\
            "\tsudo ./ShadowConfig --sport=80 --sip=yourip --lport=8080 --passwd=example"
    exit 2

}

function main() {
    Input_Sport=80
    Input_Lport=8080
    Input_Sip=127.0.0.1
    Input_Lip=127.0.0.1
    Input_Passwd=""

    # Check the user is root?
    USERID=`id -u`
    if [[ $USERID != 0 ]];then
        echo "Please use 'root' to excute this script!"
        exit 0
    fi

    if [[ $# -lt 1 ]]; then
        usage "Miss Parameter!"
    fi
    # Wait user input
    args=`getopt --long "sport:,lport:,sip:,lip:,passwd:" -- -- $*`
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
    while true
    do
        case "$1" in
            --sport)
                Input_Sport=$2
                shift 2;;
            --lport)
                Input_Lport=$2
                shift 2;;
            --sip)
                Input_Sip=$2
                shift 2;;
            --lip)
                Input_Lip=$2
                shift 2;;
            --passwd)
                Input_Passwd=$2
                shift 2;;
            --)
                shift
                break;;
            *)
               usage "Internal Error!"
               exit 2
        esac
    done
    echo -n "Whether Install ShawdownSocks(Y/n)?:"
    read InstallSS
    case "$InstallSS" in
        "Y"|"y"|"")
            BuildEnv
        ;;
    esac
    echo -n "Whether Create ShawdownSocks(Y/n)?:"
    read ISCreate
    case "$ISCreate" in
        "Y"|"y"|"")
            CreateConfigFile $Input_Sip $Input_Sport $Input_Passwd $Input_Lport
            ;;
    esac
}

main $@

