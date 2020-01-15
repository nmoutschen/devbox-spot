import os
import boto3


ec2 = boto3.resource("ec2")


def handler(event, _):
    print("EVENT: ", event)
    
    # Remove all permissions from SecurityGroup
    sg = ec2.SecurityGroup(os.environ["SECURITY_GROUP_ID"])
    sg.revoke_ingress(IpPermissions=sg.ip_permissions)