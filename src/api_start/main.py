import json
import os
import boto3
import botocore.exceptions


ec2 = boto3.resource("ec2")


def handler(event, _):
    print("EVENT: ", event)
    # Get the caller IP address
    ip = event["requestContext"]["identity"]["sourceIp"]

    # Authorize the caller to send ICMP & SSH requests
    sg = ec2.SecurityGroup(os.environ["SECURITY_GROUP_ID"])
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

    # Start the instance
    # Check that the instance is not already running or starting (pending)
    if instance.state["Name"] not in ["running", "pending"]:
        instance = ec2.Instance(os.environ["INSTANCE_ID"])
        instance.start()

    # Return the instance status and DNS
    return {
        "statusCode": 200,
        "body": json.dumps({
            "state": instance.state["Name"],
            "dns": instance.public_dns_name
        })
    }