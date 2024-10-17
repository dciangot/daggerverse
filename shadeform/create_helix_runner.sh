#!/bin/bash

#!/bin/bash

# create vm
create() {
  dagger call --name helix-dagger --shade-token env:SHADE_KEY \
  create-n-check 
}

start() {
dagger call -i --name helix-dagger --shade-token env:SHADE_KEY exec-ssh-command --ssh-key ~/.ssh/id_ed25519 --command "
sudo docker run --privileged --gpus all --shm-size=10g \
    --restart=always -d \
    --name helix-runner --ipc=host --ulimit memlock=-1 \
    --ulimit stack=67108864 \
    -v \$HOME/.cache/huggingface:/root/.cache/huggingface \
    -e RUNTIME_OLLAMA_WARMUP_MODELS=llama3:instruct,phi3:instruct \
    registry.helix.ml/helix/runner:latest-small \
    --api-host $HELIX_URL --api-token $HELIX_TOKEN \
    --runner-id shadeform-runner \
    --memory 64GB \
    --allow-multiple-copies
"
}

# delete vm
delete(){

dagger call -i --name helix-dagger --shade-token env:SHADE_KEY delete-vm
}


case "$1" in
    start) 
        start
        ;;
    create) 
        create
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


# upload launch script


# exec launch script

