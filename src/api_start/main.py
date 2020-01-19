import json
import os
import boto3
import botocore.exceptions


ec2 = boto3.resource("ec2")


def authorize_ip(sg_id: str, ip: str):
    """
    Authorize ICMP and SSH incoming traffic from the given IP address to the
    security group.
    """

    sg = ec2.SecurityGroup(sg_id)
    try:
        sg.authorize_ingress(
            CidrIp="{}/32".format(ip),
            IpProtocol="icmp",
            FromPort=-1,
            ToPort=-1
        )
    except botocore.exceptions.ClientError as exc:
        # Only ignore duplicate errors
        if exc.response['Error']['Code'] != 'InvalidPermission.Duplicate':
            raise exc
    try:
        sg.authorize_ingress(
            CidrIp="{}/32".format(ip),
            IpProtocol="tcp",
            FromPort=22,
            ToPort=22
        )
    except botocore.exceptions.ClientError as exc:
        # Only ignore duplicate errors
        if exc.response['Error']['Code'] != 'InvalidPermission.Duplicate':
            raise exc


def start_instance(instance_id: str):
    """
    Start the instance if it is not already running or starting (pending)
    """

    instance = ec2.Instance(instance_id)
    if instance.state["Name"] not in ["running", "pending"]:
        instance.start()


def get_instance_details(instance_id: str, domain_name: str):
    """
    Return details about the given instance
    """

    instance = ec2.Instance(instance_id)

    # Gather state
    retval = {
        "state": instance.state["Name"]
    }

    # Gather DNS
    if domain_name != "":
        retval["dns"] = domain_name
    else:
        retval["dns"] = instance.public_dns_name

    return retval


def handler(event, _):
    print("EVENT: ", event)
    # Get the caller IP address
    ip = event["requestContext"]["identity"]["sourceIp"]

    # Authorize the caller to send ICMP & SSH requests to the Security Group
    authorize_ip(os.environ["SECURITY_GROUP_ID"], ip)

    # Start the instance
    start_instance(os.environ["INSTANCE_ID"])

    # Return the instance details
    return {
        "statusCode": 200,
        "body": json.dumps(get_instance_details(os.environ["INSTANCE_ID"], os.environ["DOMAIN_NAME"]))
    }