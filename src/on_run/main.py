import os
import boto3


ec2 = boto3.resource("ec2")
route53 = boto3.client("route53")


HOSTED_ZONE_ID = os.environ["HOSTED_ZONE_ID"]
DOMAIN_NAME = os.environ["DOMAIN_NAME"]


def get_instance_ip(instance_id: str):
    """
    Return the instance IP address
    """

    instance = ec2.Instance(instance_id)
    return instance.public_ip_address


def add_records(hosted_zone_id: str, domain_name: str, ip: str):
    """
    Associate the IP address with the given domain name
    """

    route53.change_resource_record_sets(
        HostedZoneId=HOSTED_ZONE_ID,
        ChangeBatch={
            "Changes": [{
                "Action": "UPSERT",
                "ResourceRecordSet": {
                    "Name": domain_name,
                    "Type": "A",
                    "ResourceRecords": [{
                        "Value": ip
                    }],
                    "TTL": 60
                }
            }]
        }
    )


def handler(event, _):
    print("EVENT: ", event)
    
    instance_id = event["detail"]["instance-id"]

    # Add record for the instance in the hosted zone
    if HOSTED_ZONE_ID != "":
        ip = get_instance_ip(instance_id)
        add_records(HOSTED_ZONE_ID, DOMAIN_NAME, ip)