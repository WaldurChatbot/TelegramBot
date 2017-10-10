#!/bin/bash

echo "Starting deployment"
echo "Setting up variables"
# variables in travis
USER=${PRODUSER}
REMOTE=${PRODREMOTE}
KEY=${encrypted_a32c773f9b9a_key}
IV=${encrypted_a32c773f9b9a_iv}

# paths
SCRIPT="local_deploy_telegram.sh"
ENCRYPTED_KEY=".travis/deploy_rsa.enc"
DECRYPTED_KEY=".travis/deploy_rsa"

echo "Decrypting private key"
openssl aes-256-cbc \
                    -K ${KEY} \
                    -iv ${IV} \
                    -in ${ENCRYPTED_KEY} \
                    -out ${DECRYPTED_KEY} \
                    -d

chmod 600 ${DECRYPTED_KEY}

echo "Moving ${SCRIPT} to remote"
scp -o "StrictHostKeyChecking no" -i ${DECRYPTED_KEY} .travis/${SCRIPT} ${USER}@${REMOTE}:~/

echo "Executing ${SCRIPT} in remote"
ssh -o "StrictHostKeyChecking no" -i ${DECRYPTED_KEY} ${USER}@${REMOTE} ./${SCRIPT}
