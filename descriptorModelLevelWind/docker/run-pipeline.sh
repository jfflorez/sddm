#!/bin/bash
REPO_DIR="$HOME/hackathon/descriptorModelLevelWind"
AWS_CRED_DIR="$HOME/.aws/"
docker run \
   -v $REPO_DIR:/repo \
   -v $AWS_CRED_DIR:$HOME/.aws/\
   -p 7860:7860\
   winddesk:v1\
   /bin/bash -c "source ~/miniconda3/bin/activate && conda activate runenv && cd /repo && python pipeline.py run descriptor.json"
