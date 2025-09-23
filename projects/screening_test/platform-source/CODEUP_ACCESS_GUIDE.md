# 阿里云Codeup访问权限指南

## 🔍 **当前状态检查**

你已经能够：
- ✅ **克隆仓库** - 说明你有读取权限
- ✅ **Git配置完成** - 用户名和邮箱已设置

## 🎯 **测试推送权限**

让我们先测试你是否已经有写入权限：

### **第一步：创建测试分支**
```bash
cd ExamPlatform-FE
git checkout -b test/access-check
```

### **第二步：创建测试文件**
```bash
echo "测试访问权限 - $(date)" > access-test.txt
git add access-test.txt
git commit -m "测试：检查Codeup推送权限"
```

### **第三步：尝试推送**
```bash
git push origin test/access-check
```

## 📋 **可能的结果和解决方案**

### **情况1：推送成功** ✅
如果推送成功，说明：
- 你已经有Codeup账号
- 你已经被添加为项目成员
- 可以直接开始协作开发

**后续操作：**
```bash
# 删除测试分支
git checkout main
git branch -D test/access-check
git push origin --delete test/access-check
```

### **情况2：认证失败** ❌
如果看到类似错误：
```
Username for 'https://codeup.aliyun.com': 
Password for 'https://username@codeup.aliyun.com':
```

**说明你需要：**
1. **注册阿里云Codeup账号**
2. **配置认证信息**

### **情况3：权限被拒绝** ❌
如果看到：
```
Permission denied (publickey)
或
403 Forbidden
```

**说明你需要：**
1. **被项目管理员添加为成员**
2. **获得写入权限**

## 🔧 **获得Codeup访问权限的步骤**

### **方法A：注册阿里云Codeup账号**

1. **访问阿里云Codeup：**
   ```
   https://codeup.aliyun.com/
   ```

2. **注册/登录：**
   - 使用阿里云账号登录
   - 或创建新的阿里云账号

3. **配置Git认证：**
   ```bash
   # 方法1：HTTPS认证（推荐）
   git config --global credential.helper store
   
   # 方法2：SSH密钥（更安全）
   ssh-keygen -t rsa -b 4096 -C "simonwang@hkbu.edu.hk"
   # 然后在Codeup设置中添加SSH公钥
   ```

### **方法B：请求项目访问权限**

#### **联系项目管理员：**

**开发者联系信息：**
- **姓名：** hermitriver
- **邮箱：** hermitriver@hotmail.com

**邮件模板：**
```
主题：请求ExamPlatform项目访问权限

你好 hermitriver，

我是Simon Wang (simonwang@hkbu.edu.hk)，正在协助测试和改进ExamPlatform项目。

在最近的测试中发现了一些问题（参考会议记录），希望能够贡献代码修复这些问题：
1. 听力测试音频数量不匹配
2. 写作部分阅读材料访问问题  
3. 口语部分UI改进需求

请将我添加为以下项目的协作者：
- ExamPlatform-FE
- ExamPlatform-BE

我的阿里云Codeup用户名：[注册后提供]
邮箱：simonwang@hkbu.edu.hk

谢谢！

Simon Wang
```

### **方法C：Fork项目（如果开放）**

如果项目允许Fork：
1. **在Codeup网页上Fork项目**
2. **克隆你的Fork版本**
3. **提交修改到你的Fork**
4. **创建合并请求到原项目**

## 🚀 **立即行动计划**

### **第一步：测试当前权限**
运行上面的推送测试命令，看看会发生什么。

### **第二步：根据结果决定下一步**
- **如果成功** → 直接开始开发
- **如果需要认证** → 注册Codeup账号
- **如果权限不足** → 联系项目管理员

### **第三步：设置认证**
```bash
# 如果需要设置用户名和密码
git config --global user.name "Simon Wang"
git config --global user.email "simonwang@hkbu.edu.hk"
git config --global credential.helper store
```

## 📝 **常见认证方式**

### **HTTPS认证（简单）**
```bash
# 第一次推送时会提示输入用户名和密码
git push origin branch-name
# Username: 你的Codeup用户名
# Password: 你的Codeup密码或访问令牌
```

### **SSH密钥认证（安全）**
```bash
# 生成SSH密钥
ssh-keygen -t rsa -b 4096 -C "simonwang@hkbu.edu.hk"

# 添加到SSH代理
ssh-add ~/.ssh/id_rsa

# 复制公钥到Codeup设置
cat ~/.ssh/id_rsa.pub
```

## 🎯 **下一步**

**请先运行测试推送命令，然后告诉我结果。根据结果，我会指导你完成具体的设置步骤！**

测试命令：
```bash
cd ExamPlatform-FE
git checkout -b test/access-check
echo "测试访问权限" > access-test.txt
git add access-test.txt
git commit -m "测试推送权限"
git push origin test/access-check
```