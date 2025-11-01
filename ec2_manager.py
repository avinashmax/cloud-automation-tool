import boto3
import logging
import os
from botocore.exceptions import ClientError

# Ensure log folder exists
os.makedirs("logs", exist_ok=True)

# Configure logging
logging.basicConfig(
    filename='logs/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class EC2Manager:
    def __init__(self, region_name="ap-south-1"):
        """Initialize EC2 client"""
        try:
            self.region = region_name
            self.ec2_client = boto3.client("ec2", region_name=self.region)
            print(f"✅ EC2 client initialized for region: {self.region}")
        except Exception as e:
            print(f"Error initializing EC2 client: {e}")
            raise

    # ✅ Fetch latest Free Tier–eligible AMI dynamically
    def get_latest_free_tier_ami(self):
        try:
            response = self.ec2_client.describe_images(
                Owners=['amazon'],
                Filters=[
                    {"Name": "name", "Values": ["al2023-ami-2023*"]},
                    {"Name": "architecture", "Values": ["x86_64"]}
                ]
            )
            images = sorted(response["Images"], key=lambda x: x["CreationDate"], reverse=True)
            if images:
                ami_id = images[0]["ImageId"]
                print(f"🟢 Using latest Free Tier AMI: {ami_id}")
                return ami_id
            else:
                print("⚠️ No suitable Free Tier AMI found.")
                return None
        except Exception as e:
            print(f"Error fetching AMI: {e}")
            return None

    # ✅ Automatically detect free-tier instance type for region
    def get_free_tier_instance_type(self):
        try:
            response = self.ec2_client.describe_instance_types(
                Filters=[{"Name": "free-tier-eligible", "Values": ["true"]}]
            )
            instance_types = [it["InstanceType"] for it in response["InstanceTypes"]]
            # Prefer t3.micro > t2.micro > t4g.micro
            for preferred in ["t3.micro", "t2.micro", "t4g.micro"]:
                if preferred in instance_types:
                    print(f"🟢 Selected free-tier instance type: {preferred}")
                    return preferred
            # fallback
            if instance_types:
                return instance_types[0]
            print("⚠️ No free-tier instance types found, defaulting to t3.micro")
            return "t3.micro"
        except Exception as e:
            print(f"Error fetching instance types: {e}")
            return "t3.micro"

    def list_instances(self):
        """List all EC2 instances"""
        try:
            response = self.ec2_client.describe_instances()
            instances = []
            for reservation in response.get("Reservations", []):
                for instance in reservation.get("Instances", []):
                    instances.append({
                        "InstanceId": instance["InstanceId"],
                        "State": instance["State"]["Name"],
                        "Type": instance["InstanceType"],
                        "PublicIP": instance.get("PublicIpAddress", "N/A")
                    })
            return instances
        except Exception as e:
            print(f"Error listing instances: {e}")
            return []

    def create_instance(self, key_name=None, security_group_ids=None, subnet_id=None):
        """Create a new EC2 instance with automatic AMI + type"""
        try:
            ami_id = self.get_latest_free_tier_ami()
            instance_type = self.get_free_tier_instance_type()

            if not ami_id:
                print("❌ Could not find Free Tier AMI.")
                return None

            params = {
                "ImageId": ami_id,
                "InstanceType": instance_type,
                "MinCount": 1,
                "MaxCount": 1
            }

            if key_name:
                params["KeyName"] = key_name
            if security_group_ids:
                params["SecurityGroupIds"] = security_group_ids
            if subnet_id:
                params["SubnetId"] = subnet_id

            print(f"🚀 Launching EC2 instance with AMI: {ami_id} | Type: {instance_type}")
            instances = self.ec2_client.run_instances(**params)
            instance_id = instances["Instances"][0]["InstanceId"]

            print(f"✅ Instance created successfully! ID: {instance_id}")
            logging.info(f"Instance created: {instance_id}")

            # Wait for running state
            print("⏳ Waiting for instance to start...")
            waiter = self.ec2_client.get_waiter('instance_running')
            waiter.wait(InstanceIds=[instance_id])
            print("🟢 Instance is now running!")

            return instance_id
        except ClientError as e:
            print(f"❌ AWS Error: {e}")
            return None
        except Exception as e:
            print(f"Error creating instance: {e}")
            return None

    def stop_instance(self, instance_id):
        try:
            print(f"🟡 Stopping instance {instance_id}...")
            self.ec2_client.stop_instances(InstanceIds=[instance_id])
            self.ec2_client.get_waiter('instance_stopped').wait(InstanceIds=[instance_id])
            print("🔴 Instance stopped.")
        except Exception as e:
            print(f"Error stopping instance: {e}")

    def start_instance(self, instance_id):
        try:
            print(f"🟢 Starting instance {instance_id}...")
            self.ec2_client.start_instances(InstanceIds=[instance_id])
            self.ec2_client.get_waiter('instance_running').wait(InstanceIds=[instance_id])
            print("🟢 Instance started.")
        except Exception as e:
            print(f"Error starting instance: {e}")

    def terminate_instance(self, instance_id):
        try:
            print(f"💀 Terminating instance {instance_id}...")
            self.ec2_client.terminate_instances(InstanceIds=[instance_id])
            self.ec2_client.get_waiter('instance_terminated').wait(InstanceIds=[instance_id])
            print("✅ Instance terminated.")
        except Exception as e:
            print(f"Error terminating instance: {e}")
