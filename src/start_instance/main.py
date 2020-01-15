import json
import os
import boto3


ec2 = boto3.resource("ec2")


def handler(event, _):
    print("EVENT: ", event)
    # Get the caller IP address
    ip = event["requestContext"]["identity"]["sourceIp"]

    # Authorize the caller to send ICMP & SSH requests
    # TODO: ignore errors when the rules already exist
    sg = ec2.SecurityGroup(os.environ["SECURITY_GROUP_ID"])
    sg.authorize_ingress(
        CidrIp="{}/32".format(ip),
        IpProtocol="icmp",
        FromPort=-1,
        ToPort=-1
    )
    sg.authorize_ingress(
        CidrIp="{}/32".format(ip),
        IpProtocol="tcp",
        FromPort=22,
        ToPort=22
    )

    # Start the instance
    instance = ec2.Instance(os.environ["INSTANCE_ID"])
    instance.start()
    return {
        "statusCode": 200,
        "body": json.dumps({
            "state": instance.state,
            "dns": instance.public_dns_name
        })
    }