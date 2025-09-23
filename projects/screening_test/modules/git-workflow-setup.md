# 阿里云代码仓库本地开发工作流程设置

## 🎯 **目标：建立本地开发环境**
- 从阿里云克隆源代码到本地
- 在本地编辑代码
- 推送更改回阿里云仓库

## 🔍 **第一步：在服务器上找到Git仓库**

基于你的服务器信息，请在SSH终端中运行：

```bash
# 1. 检查exam-platform.sh脚本内容（可能包含项目路径信息）
cat exam-platform.sh

# 2. 查找Git仓库
find /root -name ".git" -type d 2>/dev/null
find /var/www -name ".git" -type d 2>/dev/null
find /opt -name ".git" -type d 2>/dev/null

# 3. 检查是否有项目目录
ls -la /var/www/
ls -la /opt/
ls -la /home/

# 4. 查看Git配置
cat .gitconfig
cat .git-credentials

# 5. 查找Python项目
find / -name "*.py" -path "*exam*" 2>/dev/null
find / -name "*.py" -path "*platform*" 2>/dev/null
```

## 🔧 **第二步：确定Git仓库类型**

### **可能的情况A：阿里云Codeup（Git仓库）**
如果使用的是阿里云Code服务，仓库URL格式通常是：
```
https://code.aliyun.com/[namespace]/[project-name].git
```

### **可能的情况B：GitLab/GitHub私有仓库**
如果使用的是其他Git服务：
```
https://gitlab.com/[user]/[project].git
https://github.com/[user]/[project].git
```

### **可能的情况C：本地Git仓库**
代码可能已经在服务器上的某个目录中作为Git仓库存在

## 🚀 **第三步：设置本地开发环境**

### **3.1 在你的Mac上创建项目目录**
```bash
# 在你的本地Mac上运行：
cd ~/Documents/Usage/VibeCodingMac/DailyAssistant/projects/screening_test/
mkdir platform-source-code
cd platform-source-code
```

### **3.2 配置Git凭据**
```bash
# 配置Git用户信息
git config --global user.name "你的姓名"
git config --global user.email "你的邮箱"

# 如果使用阿里云Codeup，配置凭据
git config --global credential.helper store
```

### **3.3 克隆仓库（根据第一步的发现）**
```bash
# 示例命令（需要替换为实际的仓库URL）：
git clone https://code.aliyun.com/[namespace]/exam-platform.git
# 或者
git clone https://[other-git-service]/[user]/[project].git
```

## 📋 **第四步：建立开发工作流程**

### **4.1 日常开发流程**
```bash
# 1. 拉取最新代码
git pull origin main

# 2. 创建功能分支
git checkout -b feature/new-feature

# 3. 编辑代码
# （在VS Code或其他编辑器中编辑）

# 4. 提交更改
git add .
git commit -m "描述你的更改"

# 5. 推送到远程仓库
git push origin feature/new-feature

# 6. 合并到主分支（在服务器或通过Web界面）
```

### **4.2 同步到服务器**
```bash
# 在服务器上（SSH终端中）：
cd /path/to/project
git pull origin main

# 重启服务（如果需要）
./exam-platform.sh
```

## 🔍 **立即行动计划**

### **你现在需要在SSH终端中运行：**

1. **查看exam-platform.sh脚本内容：**
   ```bash
   cat exam-platform.sh
   ```

2. **查找Git仓库：**
   ```bash
   find /root -name ".git" -type d 2>/dev/null
   ```

3. **检查Git配置：**
   ```bash
   cat .gitconfig
   ```

### **请运行这些命令并告诉我结果，然后我可以帮你：**
- 确定确切的Git仓库URL
- 设置本地克隆
- 建立完整的开发工作流程

## 💡 **可能的发现**

根据你服务器上的文件，我预期我们会发现：
- 一个Git仓库在某个目录中
- 仓库的远程URL配置
- 项目的具体路径和结构

**请先运行 `cat exam-platform.sh` 命令，这很可能会告诉我们项目在哪里！**