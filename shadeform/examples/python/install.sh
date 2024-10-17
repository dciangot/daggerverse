#!/bin/bash

export PRIV_KEY_FILE=$2
export CLUSTER_PUBLIC_IP=$3
export SSH_TUNNEL_NODE_PORT=$4

start() {
  mkdir -p $HOME/.interlink/logs
  mkdir -p $HOME/.interlink/bin
  mkdir -p $HOME/.interlink/config

  wget https://github.com/interTwin-eu/interLink/releases/download/0.3.1-rc3/ssh-tunnel_Linux_x86_64 -O $HOME/.interlink/bin/ssh-tunnel
  chmod +x $HOME/.interlink/bin/ssh-tunnel

  echo "Using $PRIV_KEY_FILE to establish SSH connection"
  sudo chmod 400 $PRIV_KEY_FILE
  $HOME/.interlink/bin/ssh-tunnel -addr $CLUSTER_PUBLIC_IP:$SSH_TUNNEL_NODE_PORT -keyfile $PRIV_KEY_FILE -user interlink -rport 3000 -lsock $HOME/.interlink/plugin.sock  &> $HOME/.interlink/logs/ssh-tunnel.log &
  echo $! > $HOME/.interlink/ssh-tunnel.pid

  cat <<EOF > $HOME/.interlink/config/plugin-config.yaml
Socket: "unix://$HOME/.interlink/plugin.sock"
SidecarPort: "0"

CommandPrefix: ""
ExportPodData: true
DataRootFolder: "$HOME/.interlink/jobs/"
BashPath: /bin/bash
VerboseLogging: true
ErrorsOnlyLogging: false
EOF

  wget https://github.com/interTwin-eu/interlink-docker-plugin/releases/download/0.0.27-gpu/docker-plugin_Linux_x86_64 -O $HOME/.interlink/bin/plugin
  chmod +x $HOME/.interlink/bin/plugin
  export GPUENABLED=1
  export INTERLINKCONFIGPATH=$HOME/.interlink/config/plugin-config.yaml
  $HOME/.interlink/bin/plugin &> $HOME/.interlink/logs/plugin.log &
  echo $! > $HOME/.interlink/plugin.pid
}

stop () {
    kill $(cat $HOME/.interlink/plugin.pid)
    kill $(cat $HOME/.interlink/ssh-tunnel.pid)
}

case "$1" in
    start) 
        start
        ;;
    stop)
        stop
        ;;
    restart)
        stop
        start
        ;;
    *)
        echo -e "You need to specify one of the following commands:"
        ;;
esac
