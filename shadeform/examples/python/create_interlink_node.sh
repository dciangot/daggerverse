#!/bin/bash

start() {
dagger call shadeform -i --name vnode-shadeform --shade-token env:SHADE_KEY \
  --ssh-key ~/.ssh/id_ed25519 \
  --install-script ./install.sh \
  --interlink-key ~/private/test_interlink/id_test \
  --interlink-endpoint 131.154.98.249 \
  --interlink-port 31021
}

delete(){

dagger call shadeform-delete-vm -E -i --name vnode-shadeform --shade-token env:SHADE_KEY
}


case "$1" in
    start) 
        start
        ;;
    delete)
        delete
        ;;
    restart)
        delete
        start
        ;;
    *)
        echo -e "You need to specify one of the following commands:"
        ;;
esac
