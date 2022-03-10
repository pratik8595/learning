from __future__ import print_function

import json
import datetime
import time
import boto3

print('Loading function')

#print("Received event: " + json.dumps(event, indent=2))

# get autoscaling client
client = boto3.client('autoscaling')
response = client.describe_auto_scaling_groups(AutoScalingGroupNames=['nodeasg'])
if not response['AutoScalingGroups']:
    print("no such asg")

    # get name of InstanceID in current ASG that we'll use to model new Launch Configuration after
sourceInstanceId = response.get('AutoScalingGroups')[0]['Instances'][0]['InstanceId']
print("SourceInstanceId :", sourceInstanceId )
AWS_REGION = "us-east-2"
EC2_RESOURCE = boto3.resource('ec2', region_name=AWS_REGION)
EC2_INSTANCE_ID = sourceInstanceId
timeStamp = time.time()
timeStampString = datetime.datetime.fromtimestamp(timeStamp).strftime('%Y-%m-%d  %H-%M-%S')
instance = EC2_RESOURCE.Instance(EC2_INSTANCE_ID)

image = instance.create_image(
    Name='new-ami' + ' ' + timeStampString,
    Description='This is demo AMI',
    NoReboot=True
)

print(f'AMI creation started: {image.id}')

image.wait_until_exists(
    Filters=[
        {
            'Name': 'state',
            'Values': ['available']
        }
    ]
)

print(f'AMI {image.id} successfully created')

image= image.id
# create LC using instance from target ASG as a template, only diff is the name of the new LC and new AMI
timeStamp = time.time()
timeStampString = datetime.datetime.fromtimestamp(timeStamp).strftime('%Y-%m-%d  %H-%M-%S')
newLaunchConfigName = 'LC '+ "image" + ' ' + timeStampString
client.create_launch_configuration(
    InstanceId = sourceInstanceId,
    LaunchConfigurationName=newLaunchConfigName,
    ImageId= image )

# update ASG to use new LC
response = client.update_auto_scaling_group(AutoScalingGroupName = 'abc',LaunchConfigurationName = newLaunchConfigName)

print('Updated ASG `%s` with new launch configuration `%s` which includes AMI `%s`.' %('abc', newLaunchConfigName, image))
