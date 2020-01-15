import boto3
from crhelper import CfnResource


helper = CfnResource()
ec2 = boto3.client("ec2")


@helper.create
@helper.update
def create_instance(event, context):
    instance = ec2.run_instances(
        ImageId=event["ResourceProperties"]["ImageId"],
        InstanceType=event["ResourceProperties"]["InstanceType"],
        KeyName=event["ResourceProperties"]["KeyName"],
        SecurityGroupIds=[event["ResourceProperties"]["SecurityGroupId"]],
        UserData=event["ResourceProperties"].get("UserData", ""),
        InstanceInitiatedShutdownBehavior="stop",
        InstanceMarketOptions={
            "MarketType": "spot",
            "SpotOptions": {
                "SpotInstanceType": "persistent",
                "InstanceInterruptionBehavior": "stop"
            }
        },
        MinCount=1,
        MaxCount=1
    )
    return instance["Instances"][0]["InstanceId"]


@helper.delete
def delete_instance(event, context):
    ec2.terminate_instances(
        InstanceIds=[event["PhysicalResourceId"]]
    )


def handler(event, context):
    helper(event, context)