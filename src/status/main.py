import json
import os
import boto3


ec2 = boto3.resource("ec2")


def handler(event, _):
    print("EVENT: ", event)

    # Return the instance status
    instance = ec2.Instance(os.environ["INSTANCE_ID"])
    return {
        "statusCode": 200,
        "body": json.dumps({
            "state": instance.state,
            "dns": instance.public_dns_name
        })
    }