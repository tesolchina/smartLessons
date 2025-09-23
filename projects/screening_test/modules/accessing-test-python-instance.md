# Accessing Source Code on test-python ECS Instance

## 🎯 **Current Status**
- **Target Instance:** test-python
- **Platform:** Alibaba Cloud ECS
- **Access Method:** SSH connection

## 🔧 **Step-by-Step Access Guide**

### **Step 1: Get Instance Connection Details**

From your Aliyun ECS console:

1. **Click on the test-python instance**
2. **Note down these details:**
   - **Public IP Address** (should be visible in the instance list)
   - **Private IP Address** 
   - **SSH Port** (usually 22)
   - **Username** (usually `root` or `ubuntu` or custom)

### **Step 2: SSH Connection Methods**

#### **Method A: Using macOS Terminal (Recommended)**

```bash
# Basic SSH connection
ssh username@public-ip-address

# Example (replace with actual values):
ssh root@123.456.789.123

# If using custom port:
ssh -p 2222 username@public-ip-address

# If using SSH key:
ssh -i /path/to/your/key.pem username@public-ip-address
```

#### **Method B: Using Aliyun Console (Backup Method)**

1. In the ECS console, click on your **test-python** instance
2. Look for **"Connect"** or **"远程连接"** button
3. Choose **"VNC"** or **"Terminal"** option
4. This opens a web-based terminal

### **Step 3: Locate the Source Code**

Once connected to the server, check these common locations:

```bash
# Check current directory
pwd
ls -la

# Common application directories
ls -la /var/www/
ls -la /home/
ls -la /opt/
ls -la /usr/local/src/

# Look for Python projects specifically
find / -name "*.py" -path "*/screening*" 2>/dev/null
find / -name "requirements.txt" 2>/dev/null
find / -name "app.py" 2>/dev/null
find / -name "main.py" 2>/dev/null

# Check for common web server directories
ls -la /var/www/html/
ls -la /home/www/
ls -la /srv/
```

### **Step 4: Identify the Project Structure**

Look for these indicators of your screening test platform:

```bash
# Look for project-related files
find / -name "*screening*" -type d 2>/dev/null
find / -name "*test*platform*" -type d 2>/dev/null
find / -name "*exam*" -type d 2>/dev/null

# Check for Python virtual environments
find / -name "venv" -type d 2>/dev/null
find / -name ".venv" -type d 2>/dev/null

# Look for configuration files
find / -name "config.py" 2>/dev/null
find / -name "settings.py" 2>/dev/null
find / -name "*.ini" -path "*screening*" 2>/dev/null
```

## 🔍 **What to Look For**

### **Project Structure Indicators:**
```
project-name/
├── app.py or main.py          # Main application file
├── requirements.txt           # Python dependencies
├── config/                    # Configuration files
├── templates/                 # HTML templates
├── static/                    # CSS, JS, images
├── models/                    # Database models
├── routes/ or views/          # URL routing
├── tests/                     # Test files
└── README.md                  # Project documentation
```

### **Common File Extensions:**
- `.py` - Python source files
- `.html` - Template files
- `.css` - Stylesheets
- `.js` - JavaScript files
- `.json` - Configuration files
- `.txt` - Requirements, documentation

## 🚨 **Common Connection Issues & Solutions**

### **Issue 1: Permission Denied**
```bash
# If you get permission denied, the username might be wrong
# Try these common usernames:
ssh root@ip-address
ssh ubuntu@ip-address
ssh ec2-user@ip-address
ssh admin@ip-address
```

### **Issue 2: Port Connection Refused**
```bash
# Check if custom SSH port is used
ssh -p 2222 username@ip-address
ssh -p 22022 username@ip-address
```

### **Issue 3: Key Authentication Required**
- You might need an SSH key file (.pem)
- Check if Aliyun provided a key file when the instance was created
- Or use password authentication if enabled

## 📋 **Quick Checklist**

### **Before Connecting:**
- [ ] Get the public IP of test-python instance
- [ ] Confirm SSH port (usually 22)
- [ ] Have username ready (try `root` first)
- [ ] Check if password or key authentication is needed

### **After Connecting:**
- [ ] Navigate to application directory
- [ ] Check Python version: `python --version`
- [ ] Look for virtual environment
- [ ] Find main application files
- [ ] Check if services are running: `ps aux | grep python`

### **Document What You Find:**
- [ ] Application directory path
- [ ] Main Python files
- [ ] Configuration files
- [ ] Database connection details
- [ ] Any running services/processes

## 🎯 **Next Steps**

1. **Try to SSH into the test-python instance**
2. **If successful, explore the directory structure**
3. **Document the file paths and structure you find**
4. **Let me know what you discover so I can help with:**
   - Setting up local development environment
   - Understanding the codebase structure
   - Making code modifications
   - Deployment procedures

## 📞 **Need Help?**

If you encounter any issues:
1. **Share the exact error messages**
2. **Tell me what connection method you tried**
3. **Let me know what you found in the directory structure**

I can provide more specific guidance based on what you discover!