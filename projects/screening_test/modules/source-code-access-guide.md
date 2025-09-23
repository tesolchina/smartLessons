# Source Code Access Guide - Aliyun Platform

## 🎯 **Quick Access Methods**

### **Method 1: Alibaba Cloud Console (Web Interface)**

1. **Go to Alibaba Cloud Console:**
   ```
   https://ecs.console.aliyun.com/
   ```
   or
   ```
   https://code.aliyun.com/
   ```

2. **Login Process:**
   - Use your account credentials from the image
   - Navigate to the appropriate service section

3. **Find Your Repository:**
   - Look for "Code" or "Codeup" in the service menu
   - Or check "ECS" if the code is on a server

### **Method 2: Command Line Access (Recommended for Developers)**

#### **For Git Repository (Codeup):**
```bash
# If using Aliyun Codeup
git clone https://code.aliyun.com/[your-namespace]/[repository-name].git

# Example format:
git clone https://code.aliyun.com/[username]/screening-test-platform.git
```

#### **For ECS Server Access:**
```bash
# SSH into ECS instance
ssh [username]@[server-ip-address]

# Or using Aliyun CLI
aliyun ecs DescribeInstances
```

### **Method 3: Aliyun CLI Setup**

1. **Install Aliyun CLI:**
   ```bash
   # For macOS (your system)
   brew install aliyun-cli
   
   # Or download from:
   # https://github.com/aliyun/aliyun-cli/releases
   ```

2. **Configure Credentials:**
   ```bash
   aliyun configure
   # Enter your Access Key ID and Secret when prompted
   ```

## 🔍 **Step-by-Step Discovery Process**

### **Step 1: Login to Aliyun Console**
1. Open browser and go to: https://ecs.console.aliyun.com/
2. Login with your credentials
3. Look for these services in the menu:
   - **Code** (for repositories)
   - **ECS** (for servers)
   - **Container Registry**
   - **Function Compute**

### **Step 2: Locate Your Project**
Once logged in, check these locations:

#### **Option A: Code Repository**
- Navigate to **Code** → **Repositories**
- Look for project names like:
  - `screening-test-platform`
  - `test-platform`
  - `examination-system`

#### **Option B: ECS Instances**
- Navigate to **ECS** → **Instances**
- Look for running instances
- Check if any contain your application

#### **Option C: Container Services**
- Navigate to **Container Registry** → **Repositories**
- Check for Docker images of your platform

### **Step 3: Access the Code**

#### **If it's a Git Repository:**
```bash
# Clone the repository
git clone [repository-url]
cd [project-directory]

# Check the project structure
ls -la
```

#### **If it's on an ECS Server:**
```bash
# SSH into the server
ssh username@server-ip

# Navigate to application directory (common locations)
cd /var/www/html
cd /home/[username]/[project-name]
cd /opt/[project-name]

# Check project files
ls -la
```

## 🛠 **Common Project Locations on Aliyun**

### **Web Applications (Typical Paths):**
```bash
/var/www/html/           # Apache/Nginx web root
/home/www/               # Alternative web directory
/opt/applications/       # Custom application directory
/usr/local/src/          # Source code directory
```

### **Configuration Files to Look For:**
```bash
package.json             # Node.js project
requirements.txt         # Python project
composer.json           # PHP project
pom.xml                 # Java Maven project
Dockerfile              # Containerized application
```

## 📋 **Information You'll Need**

To help you access the code, please gather:

1. **Service Type:** Which Aliyun service is being used?
2. **Repository URL:** If it's a Git repository
3. **Server IP:** If it's hosted on ECS
4. **Project Name:** What is the application called?
5. **Access Keys:** Your Access Key ID and Secret (if using CLI)

## 🔐 **Security Best Practices**

1. **Use SSH Keys for Git:**
   ```bash
   ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
   # Add public key to Aliyun Code settings
   ```

2. **Configure Git Credentials:**
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your_email@example.com"
   ```

3. **Use Environment Variables for Sensitive Data:**
   ```bash
   export ALIYUN_ACCESS_KEY_ID="your_access_key"
   export ALIYUN_ACCESS_KEY_SECRET="your_secret_key"
   ```

## 🚨 **Troubleshooting Common Issues**

### **Can't Find Repository:**
- Check if you have the correct permissions
- Verify the repository name and namespace
- Contact the project administrator

### **SSH Connection Failed:**
- Verify server IP address and port
- Check if your SSH key is added to the server
- Ensure security group allows SSH (port 22)

### **Access Denied:**
- Verify your account has the necessary permissions
- Check if 2FA is required
- Contact system administrator

## 📞 **Next Steps**

1. **Try accessing the Aliyun console first:** https://ecs.console.aliyun.com/
2. **Look for the Code or ECS service**
3. **Document what you find and let me know:**
   - What services you see
   - Any repository names or server instances
   - Error messages if you encounter any

I can provide more specific guidance once you identify which service type is hosting your code!