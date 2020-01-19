import json
import os
import boto3


ec2 = boto3.resource("ec2")


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

    # Return the instance status
    return {
        "statusCode": 200,
        "body": json.dumps(get_instance_details(os.environ["INSTANCE_ID"], os.environ["DOMAIN_NAME"]))
    }