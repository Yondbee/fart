#!/bin/sh
MY_INSTANCE_NAME="fartist1"
ZONE=europe-west2-b
# Smallest:g1-small
MACHINE_TYPE=n1-standard-4

    #--accelerator type=nvidia-tesla-t4,count=1 \
gcloud compute instances create $MY_INSTANCE_NAME \
    --image-family=debian-9 \
    --image-project=debian-cloud \
    --machine-type=$MACHINE_TYPE \
    --min-cpu-platform 'Intel Broadwell' \
    --scopes userinfo-email,cloud-platform \
    --metadata-from-file startup-script=startup.sh \
    --zone $ZONE \
    --tags http-server

gcloud compute firewall-rules create default-allow-http-80 \
    --allow tcp:80 \
    --source-ranges 0.0.0.0/0 \
    --target-tags http-server \
    --description "Allow port 80 access to http-server"