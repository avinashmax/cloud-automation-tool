import os
from colorama import Fore, init
from ec2_manager import EC2Manager
import s3_manager

# Setup
init(autoreset=True)
os.makedirs("logs", exist_ok=True)

ec2 = EC2Manager()

def menu():
    print(Fore.CYAN + "\n========== AWS EC2 + S3 Management Tool ==========")
    print(Fore.GREEN + "1. Launch new EC2 instance")
    print("2. List EC2 instances")
    print("3. Start an EC2 instance")
    print("4. Stop an EC2 instance")
    print("5. Terminate an EC2 instance")
    print("6. List S3 buckets")
    print("7. Create S3 bucket")
    print("8. Upload file to S3")
    print("9. Download file from S3")
    print("10. Exit")
    print(Fore.CYAN + "=================================================")

def main():
    while True:
        menu()
        choice = input(Fore.YELLOW + "Enter your choice (1–10): ").strip()

        if choice == "1":
            key_name = input("Enter key pair name (optional, press Enter to skip): ").strip() or None
            ec2.create_instance(key_name=key_name)
        elif choice == "2":
            ec2.list_instances()
        elif choice == "3":
            instance_id = input("Enter instance ID to start: ").strip()
            ec2.start_instance(instance_id)
        elif choice == "4":
            instance_id = input("Enter instance ID to stop: ").strip()
            ec2.stop_instance(instance_id)
        elif choice == "5":
            instance_id = input("Enter instance ID to terminate: ").strip()
            ec2.terminate_instance(instance_id)
        elif choice == "6":
            s3_manager.list_buckets()
        elif choice == "7":
            bucket_name = input("Enter new bucket name: ").strip()
            s3_manager.create_bucket(bucket_name)
        elif choice == "8":
            bucket_name = input("Enter target bucket name: ").strip()
            file_path = input("Enter full file path: ").strip()
            s3_manager.upload_file(bucket_name, file_path)
        elif choice == "9":
            bucket_name = input("Enter bucket name: ").strip()
            file_name = input("Enter file name to download: ").strip()
            destination_path = input("Enter local save path (e.g., C:/Users/ELCOT/Downloads/file.txt): ").strip()
            s3_manager.download_file(bucket_name, file_name, destination_path)
        elif choice == "10":
            print(Fore.MAGENTA + "👋 Exiting Cloud Automation Tool. Goodbye!")
            break
        else:
            print(Fore.RED + "❌ Invalid choice! Try again.")

if __name__ == "__main__":
    main()
