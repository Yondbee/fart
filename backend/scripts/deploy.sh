#!/bin/sh
MY_INSTANCE_NAME="fartist1"
ZONE=europe-west2-b
# Smallest:g1-small
MACHINE_TYPE=n1-standard-4

gcloud compute instance-templates create fartist-template \
    --region=europe-west2 \
    --network=default \
    --subnet=default \
    --image-family=debian-9 \
    --image-project=debian-cloud \
    --machine-type=$MACHINE_TYPE \
    --min-cpu-platform 'Intel Broadwell' \
    --scopes userinfo-email,cloud-platform \
    --metadata-from-file startup-script=startup.sh \
    --tags=http-server,allow-health-check

#--accelerator type=nvidia-tesla-t4,count=1 \
#gcloud compute instances create $MY_INSTANCE_NAME \
#    --image-family=debian-9 \
#    --image-project=debian-cloud \
#    --machine-type=$MACHINE_TYPE \
#    --min-cpu-platform 'Intel Broadwell' \
#    --scopes userinfo-email,cloud-platform \
#    --metadata-from-file startup-script=startup.sh \
#    --zone $ZONE \
#    --tags http-server

gcloud compute instance-groups managed create fartist-backend \
    --template=fartist-template \
    --size=1 \
    --zone=$ZONE

gcloud compute firewall-rules create fw-allow-health-check \
    --network=default \
    --action=allow \
    --direction=ingress \
    --source-ranges=130.211.0.0/22,35.191.0.0/16 \
    --target-tags=allow-health-check \
    --rules=tcp    

gcloud compute firewall-rules create default-allow-http-80 \
    --allow tcp:80 \
    --source-ranges 0.0.0.0/0 \
    --target-tags http-server \
    --description "Allow port 80 access to http-server"

gcloud compute addresses create lb-fartist \
    --ip-version=IPV4 \
    --global

gcloud compute health-checks create http http-basic-check \
        --port 80

gcloud compute backend-services create web-backend-service \
        --protocol HTTP \
        --health-checks http-basic-check \
        --global

gcloud compute backend-services add-backend web-backend-service \
        --balancing-mode=UTILIZATION \
        --max-utilization=0.8 \
        --capacity-scaler=1 \
        --instance-group=fartist-backend \
        --instance-group-zone=$ZONE \
        --global

gcloud compute url-maps create web-map-https \
        --default-service web-backend-service

# Create SSL Certificate Here
#  gcloud compute ssl-certificates create www-ssl-cert \
#        --certificate=certificate-file \
#        --private-key=private-key-file \
#        --global

gcloud compute target-https-proxies create https-lb-fartist \
        --url-map web-map-https --ssl-certificates nst

gcloud compute forwarding-rules create https-content-rule \
        --address=lb-fartist \
        --global \
        --target-https-proxy=https-lb-fartist \
        --ports=443