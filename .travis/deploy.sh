#!/bin/bash

echo "Deploying"
# if supplied argument is 'dev', use develop branch
SCRIPT="./local_deploy_telegram.sh"
USER=$PRODUSER
REMOTE=$PRODREMOTE
if [ ! -z $1 ]; then
    if [ $1 = "dev" ]; then
        SCRIPT="./local_deploy_telegram.sh dev"
        USER=$DEVUSER
        REMOTE=$DEVREMOTE
    fi
fi

echo "Decrypting private key"
openssl aes-256-cbc -K $encrypted_a32c773f9b9a_key -iv $encrypted_a32c773f9b9a_iv -in .travis/deploy_rsa.enc -out .travis/deploy_rsa -d
chmod 600 .travis/deploy_rsa
echo "Moving local_deploy to remote"
scp -o "StrictHostKeyChecking no" -i .travis/deploy_rsa .travis/local_deploy_telegram.sh $USER@$REMOTE:~/
echo "Executing local_deploy in remote"
ssh -o "StrictHostKeyChecking no" -i .travis/deploy_rsa $USER@$REMOTE $SCRIPT
