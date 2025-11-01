# 🧠 Cloud Automation Tool (AWS EC2 + S3)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![AWS](https://img.shields.io/badge/AWS-Cloud-orange?logo=amazon-aws)
![Boto3](https://img.shields.io/badge/Boto3-Library-yellow?logo=amazon-aws)
![VSCode](https://img.shields.io/badge/IDE-VSCode-blueviolet?logo=visual-studio-code)

A **Python-based automation tool** that helps you manage **AWS EC2 instances** and **S3 buckets** directly from your local machine using the **Boto3 SDK**.  
Built for beginners learning **AWS + Python** and for demonstrating **Cloud Automation & DevOps fundamentals**.

---

## ⚙️ Features

✅ **EC2 Management**
- Launch new EC2 instances (auto-fetches latest Free Tier AMI)  
- List running/stopped instances  
- Start / Stop / Terminate instances  

✅ **S3 Management**
- Automatically create an S3 bucket (if not existing)  
- List all S3 buckets  
- Upload and download files from S3  

✅ **Other Highlights**
- Built with modular Python scripts (`ec2_manager.py`, `s3_manager.py`, `main.py`)  
- Logs all actions (for debugging)  
- Uses `boto3` AWS SDK and `colorama` for CLI colors  

---

## 🏗️ Project Structure
```
cloud-automation-tool/
│
├── ec2_manager.py         # Handles all EC2 automation
├── s3_manager.py          # Manages S3 buckets & files
├── main.py                # Central CLI-based controller
├── requirements.txt       # Project dependencies
├── README.md              # Documentation
└── .gitignore             # Ignored files/folders
```

---

## 🚀 Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/avinashmax/cloud-automation-tool.git
   cd cloud-automation-tool
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate   # (Windows)
   source venv/bin/activate  # (Linux/Mac)
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure AWS credentials**
   ```bash
   aws configure
   ```
   (Enter your AWS Access Key, Secret Key, and default region like `ap-south-1`)

5. **Run the program**
   ```bash
   python main.py
   ```

---

## 📸 Example CLI Output
```
========== AWS EC2 + S3 Management Tool ==========
1. Launch EC2 Instance
2. List Instances
3. Start Instance
4. Stop Instance
5. Terminate Instance
6. List S3 Buckets
7. create S3 Buckets
8. Upload File to S3
9. Download File from S3
10. Exit
==============================================
Enter your choice: 1
Using latest Free Tier AMI: ami-0a1b2c3d4e5f67890
✅ EC2 instance launched successfully!
```

---

## 💡 Notes

- Works only with **AWS Free Tier–eligible AMIs** and instance types (e.g., `t2.micro`).  
- Ensure your AWS account is active and has **IAM permissions** for `EC2` and `S3`.  
- All actions are logged inside `logs/app.log`.

---

## 🧰 Tech Stack

| Category | Tools / Libraries |
|-----------|-------------------|
| Language | Python 3.10+ |
| Cloud Provider | AWS |
| SDK | Boto3 |
| CLI Interface | Colorama |
| IDE | Visual Studio Code |

---

## 👨‍💻 Author

**Avinash S**  
💼 *Aspiring AWS Cloud Engineer | Python Developer*  
🌐 [GitHub Profile](https://github.com/avinashmax)
