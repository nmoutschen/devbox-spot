import boto3
from crhelper import CfnResource


helper = CfnResource()
ec2 = boto3.client("ec2")


@helper.create
@helper.update
def create_instance(event, context):
    rprops = event["ResourceProperties"]

    kwargs = {
        "ImageId": rprops["ImageId"],
        "InstanceType": rprops["InstanceType"],
        "SecurityGroupIds": [rprops["SecurityGroupId"]],
        "UserData": rprops.get("UserData", ""),
        "InstanceInitiatedShutdownBehavior": "stop",
        "InstanceMarketOptions": {
            "MarketType": "spot",
            "SpotOptions": {
                "SpotInstanceType": "persistent",
                "InstanceInterruptionBehavior": "stop"
            }
        },
        "MinCount": 1,
        "MaxCount": 1
    }

    # Add the SSH key, if any
    if "KeyName" in rprops:
        kwargs["KeyName"] = rprops["KeyName"]

    # Add the instance profile, if any
    if "InstanceProfileArn" in rprops:
        kwargs["IamInstanceProfile"] = {"Arn": rprops["InstanceProfileArn"]}

    instance = ec2.run_instances(**kwargs)
    return instance["Instances"][0]["InstanceId"]


@helper.delete
def delete_instance(event, context):
    ec2.terminate_instances(
        InstanceIds=[event["PhysicalResourceId"]]
    )


def handler(event, context):
    helper(event, context)