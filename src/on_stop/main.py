import os
import boto3


ec2 = boto3.resource("ec2")
route53 = boto3.client("route53")


HOSTED_ZONE_ID = os.environ["HOSTED_ZONE_ID"]
DOMAIN_NAME = os.environ["DOMAIN_NAME"]
SECURITY_GROUP_ID = os.environ["SECURITY_GROUP_ID"]


def revoke_permissions(security_group_id: str):
    """
    Revoke all ingress permissions from a security group
    """

    sg = ec2.SecurityGroup(security_group_id)

    # Nothing to revoke
    if len(sg.ip_permissions) == 0:
        return
    
    sg.revoke_ingress(IpPermissions=sg.ip_permissions)


def remove_records(hosted_zone_id: str, domain_name: str):
    """
    Remove all records from a hosted zone that match the domain name
    """

    # List resources to delete
    response = route53.list_resource_record_sets(
        HostedZoneId=hosted_zone_id,
        # Prevents fetching resources before the given domain name
        StartRecordName=domain_name
    )
    records = [
        r for r in response["ResourceRecordSets"]
        # rstrip(".") as Route53 adds '.' at the end of a domain
        if r["Name"].rstrip(".") == domain_name.rstrip(".")
        # Only support 'A' record at the moment
        and r["Type"] in ["A"]
    ]

    # Nothing to remove
    if len(records) == 0:
        return

    # Delete the records
    print("Removing {} records from Route53".format(len(records)))
    route53.change_resource_record_sets(
        HostedZoneId=HOSTED_ZONE_ID,
        ChangeBatch={
            "Changes": [{"Action": "DELETE", "ResourceRecordSet": record} for record in records]
        }
    )


def handler(event, _):
    print("EVENT: ", event)
    
    # Remove all permissions from SecurityGroup
    revoke_permissions(SECURITY_GROUP_ID)

    # Remove all records about the domain name from the HostedZone
    if HOSTED_ZONE_ID != "":
        remove_records(HOSTED_ZONE_ID, DOMAIN_NAME)