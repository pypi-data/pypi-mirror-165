__author__ = 'sarvesh.singh'

import os
import boto3
import botocore
from test_utils.logger import Logger


class Aws:
    """
    Class for AWS !!
    """

    def __init__(self):
        """
        Connect to AWS
        """
        self.logger = Logger(name='AWS').get_logger
        self.logger.debug('Connecting to AWS !!')
        self._aws_keys = ['AWS_ACCESS_KEY_ID',
                          'AWS_SECRET_ACCESS_KEY', 'AWS_SESSION_TOKEN']
        if 'BUILD_URL' not in os.environ:
            self.check_keys_exported()
        self._s3_resource = boto3.resource('s3')
        self._ec2_client = boto3.client('ec2')
        self._ec2_resource = boto3.resource('ec2')
        self._rds_client = boto3.client('rds')
        self._route53_client = boto3.client('route53')
        self._asg_client = boto3.client('autoscaling')
        self._alb_client = boto3.client('elbv2')
        self._elasticache_client = boto3.client('elasticache')

    def check_keys_exported(self):
        """
        Func to check if aws keys exported
        """
        for _key in self._aws_keys:
            if _key not in os.environ:
                self.logger.error(f'{_key} does not exist in environment variables')
                raise Exception(f'{_key} does not exist in environment variables')

    def get_all_buckets(self):
        """
        Func to get all available buckets
        """
        _buckets = []
        for _bucket in self._s3_resource.buckets.all():
            _buckets.append(_bucket)

        return _buckets

    def get_bucket_object(self, bucket_name=None, key=None):
        """
        Func to get the bucket object
        :param bucket_name
        :param key
        """
        obj = self._s3_resource.Object(bucket_name=bucket_name, key=key)
        return obj

    def get_all_instances(self):
        """
        Func to get all ec2 instances
        """
        _instances = []
        for _instance in self._ec2_client.describe_instances()['Reservations']:
            _instances.append(_instance['Instances'][0])

        return _instances

    def get_instance(self, instance_id=None):
        """
        Func to get an instance using instance id
        :param instance_id
        """
        _instance = self._ec2_resource.Instance(instance_id)
        return _instance

    def get_asg(self, asg_name=None):
        """
        Func to get ASG
        :param asg_name
        """
        _asg = self._asg_client.describe_auto_scaling_groups(
            AutoScalingGroupNames=[asg_name])
        return _asg

    def get_alb(self, alb_name=None):
        """
        Func to get ALB
        :param alb_name
        """
        _alb = self._alb_client.describe_load_balancers(Names=[alb_name])
        return _alb

    def get_target_group(self, target_name=None):
        """
        Func to get target group
        :param target_name
        """
        _target = self._alb_client.describe_target_groups(Names=[target_name])
        return _target

    def get_launch_template(self, template_name=None):
        """
        Func to get launch template
        :param template_name
        """
        _template = self._ec2_client.describe_launch_templates(
            LaunchTemplateNames=[template_name])
        return _template

    def get_elasticache_cluster(self, cluster_name=None):
        """
        Func to get elasticache cluster
        :param cluster_name
        """
        _elastiche = self._elasticache_client.describe_cache_clusters(
            CacheClusterId=cluster_name)
        return _elastiche

    def run_instance(self, ami_id=None, instance_type=None):
        """
        Run an EC2 instance
        :param ami_id:
        :param instance_type:
        :return:
        """
        response = self._ec2_client.run_instances(ImageId=ami_id, InstanceType=instance_type,
                                                  MaxCount=1, MinCount=1)
        _instance = response['Instances'][0]
        return _instance

    def start_instance(self, instance_id=None):
        """
        Start an EC2 instance
        :param instance_id:
        :return:
        """
        try:
            # Start an instance
            self._ec2_client.start_instances(
                InstanceIds=[instance_id], DryRun=False)
            self.logger.debug(f'Successfully started instance: {instance_id}')
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "InvalidInstanceID.Malformed":
                self.logger.error('Invalid Instance id !!')
            else:
                raise Exception(f'{instance_id} starting failed !!')

    def stop_instance(self, instance_id=None):
        """
        Stop an EC2 instance
        :param instance_id:
        :return:
        """
        try:
            # Stop an instance
            self._ec2_client.stop_instances(
                InstanceIds=[instance_id], DryRun=False)
            self.logger.debug(f'Successfully stopped instance: {instance_id}')
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "InvalidInstanceID.Malformed":
                self.logger.error('Invalid Instance id !!')
            else:
                raise Exception(f'{instance_id} stopping failed !!')

    def reboot_instance(self, instance_id=None):
        """
        Reboot an EC2 instance
        :param instance_id:
        :return:
        """
        try:
            # Reboot an instance
            self._ec2_client.reboot_instances(
                InstanceIds=[instance_id], DryRun=False)
            self.logger.debug(f'Successfully rebooted instance: {instance_id}')
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "InvalidInstanceID.Malformed":
                self.logger.error('Invalid Instance id !!')
            else:
                raise Exception(f'{instance_id} rebooting failed !!')

    def terminate_instance(self, instance_id=None):
        """
        Terminate an EC2 instance
        :param instance_id:
        :return:
        """
        try:
            # Terminate an instance
            self._ec2_client.terminate_instances(
                InstanceIds=[instance_id], DryRun=False)
            self.logger.debug(f'Successfully terminated instance: {instance_id}')
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "InvalidInstanceID.Malformed":
                print("Error: Invalid instance id!!")
            else:
                raise Exception(f'{instance_id} termination failed !!')

    def get_all_rds(self):
        """
        Func to get all rds
        """
        _rds = []
        for _db in self._rds_client.describe_db_instances()['DBInstances']:
            _rds.append(_db)

        return _rds

    def get_rds(self, rds_name=None):
        """
        Func to get particular rds
        :param rds_name:
        """
        _rds = self._rds_client.describe_db_clusters(
            DBClusterIdentifier=rds_name)
        return _rds

    def get_all_ami(self):
        """
        Func to get all ami's
        """
        _ami = []
        for _image in self._ec2_client.describe_images()['Images']:
            _ami.append(_image)

        return _ami

    def get_ami_info(self, name=None):
        """
        Func to get ami info
        :param name
        :return:
        """
        _ami = self._ec2_client.describe_images(
            Filters=[
                {
                    'Name': 'name',
                    'Values': [name]
                },
            ],
        )
        if len(_ami['Images']) > 1:
            return sorted(_ami['Images'], key=lambda d: d['CreationDate'], reverse=True)[0]
        return None

    def deregister_ami(self, ami_id=None):
        """Func to deregister AMI

        Args:
            ami_id (_type_, optional): _description_. Defaults to None.
        """
        try:
            self._ec2_client.deregister_image(ImageId=ami_id)
        except botocore.exceptions.ClientError as e:
            if f"'{ami_id}' is no longer available" in str(e):
                self.logger.info(f'{ami_id} is not available')
            else:
                raise Exception(e)
